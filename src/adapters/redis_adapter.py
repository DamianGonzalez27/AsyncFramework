# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
# -------------------------

"""Adaptador para Redis.

Implementa la conexión y operaciones con Redis mediante redis-py.
"""

from typing import Any, Optional
from logger_tracker import logg_info, logg_error, logg_debug


class RedisAdapter:
    """Adaptador concreto para conexiones a Redis."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        decode_responses: bool = True,
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self.client = None

    def connect(self) -> None:
        """Establece conexión con Redis."""
        try:
            import redis

            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=self.decode_responses,
            )
            self.client.ping()
            logg_info(f"✓ Redis connected: {self.host}:{self.port}")
        except Exception as e:
            logg_error(f"✗ Failed to connect to Redis: {e}")
            raise

    def get(self, key: str) -> Any:
        """Obtiene un valor de Redis."""
        try:
            if not self.client:
                raise RuntimeError("Not connected to Redis")
            value = self.client.get(key)
            logg_debug(f"Retrieved key: {key}")
            return value
        except Exception as e:
            logg_error(f"Failed to get key {key}: {e}")
            raise

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        """Establece un valor en Redis."""
        try:
            if not self.client:
                raise RuntimeError("Not connected to Redis")
            if expire:
                self.client.setex(key, expire, value)
            else:
                self.client.set(key, value)
            logg_debug(f"Set key: {key}")
        except Exception as e:
            logg_error(f"Failed to set key {key}: {e}")
            raise

    def delete(self, key: str) -> None:
        """Elimina un valor de Redis."""
        try:
            if not self.client:
                raise RuntimeError("Not connected to Redis")
            self.client.delete(key)
            logg_debug(f"Deleted key: {key}")
        except Exception as e:
            logg_error(f"Failed to delete key {key}: {e}")
            raise

    def exists(self, key: str) -> bool:
        """Verifica si una clave existe en Redis."""
        try:
            if not self.client:
                raise RuntimeError("Not connected to Redis")
            return bool(self.client.exists(key))
        except Exception as e:
            logg_error(f"Failed to check existence of key {key}: {e}")
            raise

    def close(self) -> None:
        """Cierra la conexión con Redis."""
        try:
            if self.client:
                self.client.close()
                logg_info("✓ Redis connection closed")
        except Exception as e:
            logg_error(f"Error closing Redis connection: {e}")
