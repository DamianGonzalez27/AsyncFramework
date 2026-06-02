# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
#
# Este software y su código fuente han sido desarrollados por Erick Damian Gonzalez Aranda.
# -------------------------

"""Puerto para conexiones a RabbitMQ."""

from abc import abstractmethod
from typing import Any, Dict, Optional, Iterable

from src.ports.base_port import BasePort


class RabbitMQPort(BasePort):
    def __init__(self) -> None:
        super().__init__("rabbitmq")

    @abstractmethod
    def connect(self, host: str, port: int, username: str, password: str) -> None:
        pass

    @abstractmethod
    def declare_queue(self, queue_name: str, durable: bool = True) -> None:
        pass

    @abstractmethod
    def publish(self, queue_name: str, payload: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def consume(self, queue_name: str, callback: Any) -> None:
        pass

    @abstractmethod
    def ack(self, delivery_tag: Any) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
