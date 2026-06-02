import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional
from logger_tracker import logg_info, logg_error, logg_debug

from src.adapters.async_rabbitmq_adapter import AsyncRabbitMQAdapter
from src.config import (
    OUTBOX_DLQ,
    OUTBOX_DLX,
    WORKER_RABBITMQ_MAX_RETRIES,
)


class RabbitConsumer:
    def __init__(
        self,
        rabbit: AsyncRabbitMQAdapter,
        queue_name: str,
        message_handler: Callable,
        prefetch_count: int = 20,
        max_retries: int = WORKER_RABBITMQ_MAX_RETRIES,
    ):
        self.rabbit = rabbit
        self.queue_name = queue_name
        self.message_handler = message_handler
        self.prefetch_count = prefetch_count
        self.max_retries = max_retries
        self._running = False

    async def start(self) -> None:
        self._running = True
        logg_info(f"RabbitConsumer started for queue: {self.queue_name}")

        await self._setup_infrastructure()

        queue = await self.rabbit.channel.get_queue(self.queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                if not self._running:
                    break
                await self._process_message(message)

    async def stop(self) -> None:
        self._running = False
        logg_info(f"RabbitConsumer stopped for queue: {self.queue_name}")

    async def _setup_infrastructure(self) -> None:
        dlx = await self.rabbit.declare_exchange(
            exchange_name=OUTBOX_DLX,
            exchange_type="direct",
            durable=True,
        )
        await self.rabbit.declare_queue(
            queue_name=OUTBOX_DLQ,
            durable=True,
        )
        await self.rabbit.bind_queue(
            queue_name=OUTBOX_DLQ,
            exchange_name=OUTBOX_DLX,
            routing_key=OUTBOX_DLQ,
        )

    async def _process_message(self, message: Any) -> None:
        delivery_tag = message.delivery_tag
        headers = message.headers or {}
        retry_count = int(headers.get("x-retry-count", 0))
        event_id = headers.get("event_id", "unknown")

        logg_debug(f"Processing message {event_id} (retry {retry_count})")

        try:
            body = json.loads(message.body.decode())
            await self.message_handler(body, headers)
            await self.rabbit.ack(message)
            logg_debug(f"Message {event_id} processed and acked")

        except Exception as e:
            logg_error(f"Error processing message {event_id}: {e}")

            if retry_count >= self.max_retries:
                logg_info(
                    f"Message {event_id} exceeded max retries, sending to DLQ"
                )
                await self._send_to_dlq(
                    message.body,
                    headers,
                    error=str(e),
                )
                await self.rabbit.ack(message)
            else:
                await self._requeue_with_retry(
                    message.body,
                    headers,
                    retry_count + 1,
                )
                await self.rabbit.ack(message)

    async def _send_to_dlq(
        self,
        body: bytes,
        headers: Dict[str, str],
        error: str,
    ) -> None:
        import aio_pika

        payload = {
            "original_body": json.loads(body.decode()),
            "error": error,
            "failed_at": datetime.now(timezone.utc).isoformat(),
        }
        dlq_headers = {
            **headers,
            "x-error": error,
            "x-failed-at": datetime.now(timezone.utc).isoformat(),
        }
        dlq_message = aio_pika.Message(
            body=json.dumps(payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            headers=dlq_headers,
        )
        exchange = await self.rabbit.channel.get_exchange(OUTBOX_DLX)
        await exchange.publish(dlq_message, routing_key=OUTBOX_DLQ)
        logg_info(f"Message sent to DLQ: {OUTBOX_DLQ}")

    async def _requeue_with_retry(
        self,
        body: bytes,
        headers: Dict[str, str],
        new_retry_count: int,
    ) -> None:
        import aio_pika

        retry_headers = {
            **headers,
            "x-retry-count": str(new_retry_count),
            "x-last-retry-at": datetime.now(timezone.utc).isoformat(),
        }
        retry_message = aio_pika.Message(
            body=body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            headers=retry_headers,
        )
        await self.rabbit.channel.default_exchange.publish(
            retry_message,
            routing_key=self.queue_name,
        )
        logg_debug(f"Message requeued (retry {new_retry_count})")
