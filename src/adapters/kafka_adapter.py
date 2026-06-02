# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
# -------------------------

"""Adaptador para Kafka.

Implementa la conexión y operaciones con Kafka mediante kafka-python.
"""

from typing import Iterable, Dict, Any, Optional
from logger_tracker import logg_info, logg_error, logg_debug


class KafkaAdapter:
    """Adaptador concreto para conexiones a Kafka."""

    def __init__(
        self,
        bootstrap_servers: Iterable[str] = None,
        client_id: str = "kerverus-client",
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

    def connect(self) -> None:
        """Establece conexión con Kafka."""
        try:
            from kafka import KafkaProducer, KafkaConsumer
            import json

            producer_config = {
                "bootstrap_servers": self.bootstrap_servers,
                "client_id": self.client_id,
                "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
            }

            if self.security_protocol != "PLAINTEXT":
                producer_config["security_protocol"] = self.security_protocol
                if self.sasl_mechanism:
                    producer_config["sasl_mechanism"] = self.sasl_mechanism
                    producer_config["sasl_plain_username"] = self.sasl_username
                    producer_config["sasl_plain_password"] = self.sasl_password

            self.producer = KafkaProducer(**producer_config)
            logg_info(f"✓ Kafka connected: {self.bootstrap_servers}")
        except Exception as e:
            logg_error(f"✗ Failed to connect to Kafka: {e}")
            raise

    def publish(self, topic: str, payload: Dict[str, Any]) -> None:
        """Publica un mensaje a un topic."""
        try:
            if not self.producer:
                raise RuntimeError("Not connected to Kafka")
            self.producer.send(topic, value=payload)
            self.producer.flush()
            logg_debug(f"Message published to topic: {topic}")
        except Exception as e:
            logg_error(f"Failed to publish message to {topic}: {e}")
            raise

    def subscribe(self, topic: str, group_id: str) -> None:
        """Se suscribe a un topic."""
        try:
            from kafka import KafkaConsumer
            import json

            consumer_config = {
                "bootstrap_servers": self.bootstrap_servers,
                "group_id": group_id,
                "value_deserializer": lambda m: json.loads(m.decode("utf-8")),
            }

            if self.security_protocol != "PLAINTEXT":
                consumer_config["security_protocol"] = self.security_protocol
                if self.sasl_mechanism:
                    consumer_config["sasl_mechanism"] = self.sasl_mechanism
                    consumer_config["sasl_plain_username"] = self.sasl_username
                    consumer_config["sasl_plain_password"] = self.sasl_password

            self.consumer = KafkaConsumer(topic, **consumer_config)
            logg_info(f"✓ Subscribed to topic: {topic}")
        except Exception as e:
            logg_error(f"Failed to subscribe to topic {topic}: {e}")
            raise

    def poll(self, timeout_ms: int = 1000) -> Dict[str, Any]:
        """Obtiene mensajes del topic suscrito."""
        try:
            if not self.consumer:
                raise RuntimeError("Not subscribed to any topic")
            messages = self.consumer.poll(timeout_ms=timeout_ms)
            logg_debug("Polling messages from Kafka")
            return messages
        except Exception as e:
            logg_error(f"Failed to poll messages: {e}")
            raise

    def commit(self) -> None:
        """Confirma el offset actual."""
        try:
            if self.consumer:
                self.consumer.commit()
                logg_debug("Offset committed")
        except Exception as e:
            logg_error(f"Failed to commit offset: {e}")

    def close(self) -> None:
        """Cierra la conexión con Kafka."""
        try:
            if self.producer:
                self.producer.close()
            if self.consumer:
                self.consumer.close()
            logg_info("✓ Kafka connection closed")
        except Exception as e:
            logg_error(f"Error closing Kafka connection: {e}")
