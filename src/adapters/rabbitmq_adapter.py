# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
# -------------------------

"""Adaptador para RabbitMQ.

Implementa la conexión y operaciones con RabbitMQ mediante pika.
"""

import pika
from typing import Callable, Optional, Dict, Any
from logger_tracker import logg_info, logg_error, logg_debug


class RabbitMQAdapter:
    """Adaptador concreto para conexiones a RabbitMQ."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
        vhost: str = "/",
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.vhost = vhost
        self.connection = None
        self.channel = None

    def connect(self) -> None:
        """Establece conexión con RabbitMQ."""
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhost,
                credentials=credentials,
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            logg_info(f"✓ RabbitMQ connected: {self.host}:{self.port}")
        except Exception as e:
            logg_error(f"✗ Failed to connect to RabbitMQ: {e}")
            raise

    def declare_queue(self, queue_name: str, durable: bool = True) -> None:
        """Declara una cola en RabbitMQ."""
        try:
            if not self.channel:
                raise RuntimeError("Not connected to RabbitMQ")
            self.channel.queue_declare(queue=queue_name, durable=durable)
            logg_debug(f"Queue declared: {queue_name}")
        except Exception as e:
            logg_error(f"Failed to declare queue {queue_name}: {e}")
            raise

    def publish(self, queue_name: str, payload: Dict[str, Any]) -> None:
        """Publica un mensaje a una cola."""
        try:
            if not self.channel:
                raise RuntimeError("Not connected to RabbitMQ")
            import json
            message = json.dumps(payload)
            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=message,
            )
            logg_debug(f"Message published to {queue_name}")
        except Exception as e:
            logg_error(f"Failed to publish message: {e}")
            raise

    def consume(self, queue_name: str, callback: Callable) -> None:
        """Consume mensajes de una cola."""
        try:
            if not self.channel:
                raise RuntimeError("Not connected to RabbitMQ")
            self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
            logg_info(f"Consuming from queue: {queue_name}")
            self.channel.start_consuming()
        except Exception as e:
            logg_error(f"Failed to consume from queue: {e}")
            raise

    def ack(self, delivery_tag: Any) -> None:
        """Reconoce un mensaje consumido."""
        try:
            if self.channel:
                self.channel.basic_ack(delivery_tag=delivery_tag)
        except Exception as e:
            logg_error(f"Failed to ack message: {e}")

    def close(self) -> None:
        """Cierra la conexión con RabbitMQ."""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                logg_info("✓ RabbitMQ connection closed")
        except Exception as e:
            logg_error(f"Error closing RabbitMQ connection: {e}")
