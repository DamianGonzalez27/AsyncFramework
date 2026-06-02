# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
# -------------------------

"""Puerto para conexiones a Redis."""

from abc import abstractmethod
from typing import Any, Optional

from src.ports.base_port import BasePort


class RedisPort(BasePort):
    def __init__(self) -> None:
        super().__init__("redis")

    @abstractmethod
    def connect(self, host: str, port: int, db: int = 0, password: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
