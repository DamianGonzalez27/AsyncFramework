# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
# -------------------------

"""Puerto para conexiones PostgreSQL."""

from abc import abstractmethod
from typing import Any, Dict, Optional

from src.ports.database_port import DatabasePort


class PostgresPort(DatabasePort):
    def __init__(self) -> None:
        super().__init__("postgres")

    @abstractmethod
    def connect(self, database_url: str) -> Any:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        pass

    @abstractmethod
    def fetch_one(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        pass

    @abstractmethod
    def fetch_all(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        pass
