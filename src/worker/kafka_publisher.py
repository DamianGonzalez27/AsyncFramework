from datetime import datetime, timezone
from typing import Any, Dict, Optional
from logger_tracker import logg_info, logg_error, logg_debug

from src.adapters.async_kafka_adapter import AsyncKafkaAdapter
from src.config import KAFKA_EVENTS_TOPIC, KAFKA_ERROR_TOPIC


class KafkaEventPublisher:
    def __init__(
        self,
        kafka: AsyncKafkaAdapter,
        events_topic: str = KAFKA_EVENTS_TOPIC,
        error_topic: str = KAFKA_ERROR_TOPIC,
    ):
        self.kafka = kafka
        self.events_topic = events_topic
        self.error_topic = error_topic

    async def publish_event(
        self,
        event_type: str,
        aggregate_type: str,
        aggregate_id: str,
        correlation_id: str,
        payload: Dict[str, Any],
        event_id: Optional[str] = None,
    ) -> None:
        import uuid

        event = {
            "event_id": event_id or str(uuid.uuid4()),
            "event_type": event_type,
            "aggregate_type": aggregate_type,
            "aggregate_id": aggregate_id,
            "correlation_id": correlation_id,
            "data": payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "kerverus-worker",
        }

        try:
            await self.kafka.publish(
                topic=self.events_topic,
                payload=event,
                key=correlation_id,
            )
            logg_debug(
                f"Kafka event published: {event_type} "
                f"[correlation_id={correlation_id}]"
            )
        except Exception as e:
            logg_error(
                f"Failed to publish event {event_type} to Kafka: {e}"
            )
            await self._publish_error(event, str(e))

    async def publish_error_event(
        self,
        original_event: Dict[str, Any],
        error: str,
    ) -> None:
        error_event = {
            **original_event,
            "error": error,
            "event_type": f"{original_event.get('event_type', 'unknown')}.error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "kerverus-worker",
        }
        await self._publish_error(original_event, error)

    async def _publish_error(
        self,
        original_event: Dict[str, Any],
        error: str,
    ) -> None:
        try:
            error_payload = {
                "original_event": original_event,
                "error": error,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            correlation_id = original_event.get("correlation_id", "unknown")
            await self.kafka.publish(
                topic=self.error_topic,
                payload=error_payload,
                key=correlation_id,
            )
            logg_info(f"Error event published to {self.error_topic}")
        except Exception as e:
            logg_error(
                f"Failed to publish error event to Kafka: {e}"
            )
