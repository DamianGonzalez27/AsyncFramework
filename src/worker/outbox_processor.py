import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from sqlalchemy.orm import scoped_session
from sqlalchemy import select, update
from logger_tracker import logg_info, logg_error, logg_debug

from src.modules.clients.models.database.outbox import OutboxMessage, OutboxStatus
from src.adapters.async_rabbitmq_adapter import AsyncRabbitMQAdapter
from src.adapters.async_kafka_adapter import AsyncKafkaAdapter
from src.config import (
    OUTBOX_QUEUE,
    KAFKA_EVENTS_TOPIC,
    WORKER_OUTBOX_POLL_INTERVAL,
)


class OutboxProcessor:
    def __init__(
        self,
        session_factory: scoped_session,
        rabbit: AsyncRabbitMQAdapter,
        kafka: AsyncKafkaAdapter,
        poll_interval: int = WORKER_OUTBOX_POLL_INTERVAL,
    ):
        self.session_factory = session_factory
        self.rabbit = rabbit
        self.kafka = kafka
        self.poll_interval = poll_interval
        self._running = False

    async def start(self) -> None:
        self._running = True
        logg_info("OutboxProcessor started")
        while self._running:
            try:
                await self._process_batch()
            except Exception as e:
                logg_error(f"OutboxProcessor error: {e}")
            await asyncio.sleep(self.poll_interval)

    async def stop(self) -> None:
        self._running = False
        logg_info("OutboxProcessor stopped")

    async def _process_batch(self) -> None:
        messages = await self._fetch_pending()
        if not messages:
            return

        logg_info(f"Outbox: processing {len(messages)} pending messages")
        for msg in messages:
            await self._publish_message(msg)

    async def _fetch_pending(self) -> list[OutboxMessage]:
        def _query():
            session = self.session_factory()
            try:
                stmt = (
                    select(OutboxMessage)
                    .where(OutboxMessage.status == OutboxStatus.PENDING)
                    .order_by(OutboxMessage.created_at.asc())
                    .limit(50)
                )
                result = session.execute(stmt)
                return list(result.scalars().all())
            finally:
                session.close()

        return await asyncio.to_thread(_query)

    async def _publish_message(self, msg: OutboxMessage) -> None:
        payload = msg.payload
        correlation_id = msg.correlation_id
        event_id = msg.event_id

        try:
            if msg.destination in ("rabbitmq", "all"):
                await self.rabbit.publish(
                    queue_name=OUTBOX_QUEUE,
                    payload=payload,
                    correlation_id=correlation_id,
                    headers={"event_id": event_id, "event_type": msg.event_type},
                )

            if msg.destination in ("kafka", "all"):
                await self.kafka.publish(
                    topic=KAFKA_EVENTS_TOPIC,
                    payload={
                        **payload,
                        "event_id": event_id,
                        "event_type": msg.event_type,
                        "aggregate_type": msg.aggregate_type,
                        "aggregate_id": msg.aggregate_id,
                        "correlation_id": correlation_id,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    },
                    key=correlation_id,
                )

            await self._mark_sent(msg.id)
            logg_debug(f"Outbox message {event_id} published")

        except Exception as e:
            logg_error(f"Failed to publish outbox message {event_id}: {e}")
            await self._mark_failed(msg.id, str(e))

    async def _mark_sent(self, msg_id: str) -> None:
        def _update():
            session = self.session_factory()
            try:
                stmt = (
                    update(OutboxMessage)
                    .where(OutboxMessage.id == msg_id)
                    .values(
                        status=OutboxStatus.SENT,
                        sent_at=datetime.now(timezone.utc),
                    )
                )
                session.execute(stmt)
                session.commit()
            finally:
                session.close()

        await asyncio.to_thread(_update)

    async def _mark_failed(self, msg_id: str, error: str) -> None:
        def _update():
            session = self.session_factory()
            try:
                stmt = (
                    update(OutboxMessage)
                    .where(OutboxMessage.id == msg_id)
                    .values(
                        status=OutboxStatus.FAILED,
                        last_error=error[:500],
                    )
                )
                session.execute(stmt)
                session.commit()
            finally:
                session.close()

        await asyncio.to_thread(_update)
