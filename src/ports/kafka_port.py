# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
# -------------------------

"""Puerto para conexiones a Kafka."""

from abc import abstractmethod
from typing import Any, Dict, Iterable

from src.ports.base_port import BasePort


class KafkaPort(BasePort):
    def __init__(self) -> None:
        super().__init__("kafka")

    @abstractmethod
    def connect(self, bootstrap_servers: Iterable[str], client_id: str = "") -> None:
        pass

    @abstractmethod
    def publish(self, topic: str, payload: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def subscribe(self, topic: str, group_id: str) -> None:
        pass

    @abstractmethod
    def poll(self, timeout_ms: int = 1000) -> Any:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
