import json
from typing import Any, Dict, Iterable, Optional, Callable
from logger_tracker import logg_info, logg_error, logg_debug


class AsyncKafkaAdapter:
    def __init__(
        self,
        bootstrap_servers: Iterable[str] = None,
        client_id: str = "kerverus-worker",
        security_protocol: str = "PLAINTEXT",
        sasl_mechanism: Optional[str] = None,
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
    ):
        self.bootstrap_servers = bootstrap_servers or ["localhost:9092"]
        self.client_id = client_id
        self.security_protocol = security_protocol
        self.sasl_mechanism = sasl_mechanism
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password
        self.producer = None
        self.consumer = None

    async def connect_producer(self) -> None:
        try:
            from aiokafka import AIOKafkaProducer

            producer_config = {
                "bootstrap_servers": self.bootstrap_servers,
                "client_id": self.client_id,
                "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
                "acks": "all",
            }

            if self.security_protocol != "PLAINTEXT":
                producer_config["security_protocol"] = self.security_protocol
                if self.sasl_mechanism:
                    producer_config["sasl_mechanism"] = self.sasl_mechanism
                    producer_config["sasl_plain_username"] = self.sasl_username
                    producer_config["sasl_plain_password"] = self.sasl_password

            self.producer = AIOKafkaProducer(**producer_config)
            await self.producer.start()
            logg_info(f"✓ Async Kafka producer connected: {self.bootstrap_servers}")
        except Exception as e:
            logg_error(f"✗ Failed to connect Async Kafka producer: {e}")
            raise

    async def connect_consumer(
        self,
        topic: str,
        group_id: str,
        auto_offset_reset: str = "earliest",
    ) -> None:
        try:
            from aiokafka import AIOKafkaConsumer

            consumer_config = {
                "bootstrap_servers": self.bootstrap_servers,
                "group_id": group_id,
                "value_deserializer": lambda m: json.loads(m.decode("utf-8")),
                "auto_offset_reset": auto_offset_reset,
                "enable_auto_commit": False,
            }

            if self.security_protocol != "PLAINTEXT":
                consumer_config["security_protocol"] = self.security_protocol
                if self.sasl_mechanism:
                    consumer_config["sasl_mechanism"] = self.sasl_mechanism
                    consumer_config["sasl_plain_username"] = self.sasl_username
                    consumer_config["sasl_plain_password"] = self.sasl_password

            self.consumer = AIOKafkaConsumer(topic, **consumer_config)
            await self.consumer.start()
            logg_info(f"✓ Async Kafka consumer subscribed to: {topic}")
        except Exception as e:
            logg_error(f"Failed to subscribe to topic {topic}: {e}")
            raise

    async def publish(
        self,
        topic: str,
        payload: Dict[str, Any],
        key: Optional[str] = None,
    ) -> None:
        try:
            if not self.producer:
                raise RuntimeError("Async Kafka producer not connected")
            key_bytes = key.encode("utf-8") if key else None
            await self.producer.send(
                topic,
                value=payload,
                key=key_bytes,
            )
            logg_debug(f"Message published to topic: {topic} (key={key})")
        except Exception as e:
            logg_error(f"Failed to publish message to {topic}: {e}")
            raise

    async def publish_with_ack(
        self,
        topic: str,
        payload: Dict[str, Any],
        key: Optional[str] = None,
    ) -> Any:
        try:
            if not self.producer:
                raise RuntimeError("Async Kafka producer not connected")
            key_bytes = key.encode("utf-8") if key else None
            result = await self.producer.send(
                topic,
                value=payload,
                key=key_bytes,
            )
            metadata = await result
            logg_debug(
                f"Message published to {topic} "
                f"[partition={metadata.partition}, offset={metadata.offset}]"
            )
            return metadata
        except Exception as e:
            logg_error(f"Failed to publish message to {topic}: {e}")
            raise

    async def poll(self, timeout_ms: int = 1000) -> Dict[str, Any]:
        try:
            if not self.consumer:
                raise RuntimeError("Async Kafka consumer not connected")
            messages = await self.consumer.getmany(timeout_ms=timeout_ms)
            return messages
        except Exception as e:
            logg_error(f"Failed to poll messages: {e}")
            raise

    async def commit(self) -> None:
        try:
            if self.consumer:
                await self.consumer.commit()
        except Exception as e:
            logg_error(f"Failed to commit offset: {e}")

    async def close(self) -> None:
        try:
            if self.producer:
                await self.producer.stop()
            if self.consumer:
                await self.consumer.stop()
            logg_info("✓ Async Kafka connection closed")
        except Exception as e:
            logg_error(f"Error closing Async Kafka connection: {e}")
