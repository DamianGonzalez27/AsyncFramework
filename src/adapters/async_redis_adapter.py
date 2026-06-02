from typing import Any, Optional
from logger_tracker import logg_info, logg_error, logg_debug


class AsyncRedisAdapter:
    def __init__(
        self,
        url: str = "redis://localhost:6379/0",
        password: Optional[str] = None,
        decode_responses: bool = True,
    ):
        self.url = url
        self.password = password
        self.decode_responses = decode_responses
        self.client = None

    async def connect(self) -> None:
        try:
            from redis import asyncio as aioredis

            self.client = aioredis.from_url(
                self.url,
                password=self.password,
                decode_responses=self.decode_responses,
            )
            await self.client.ping()
            logg_info(f"✓ Async Redis connected: {self.url}")
        except Exception as e:
            logg_error(f"✗ Failed to connect to Async Redis: {e}")
            raise

    async def get(self, key: str) -> Any:
        try:
            if not self.client:
                raise RuntimeError("Not connected to Redis")
            value = await self.client.get(key)
            return value
        except Exception as e:
            logg_error(f"Failed to get key {key}: {e}")
            raise

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        try:
            if not self.client:
                raise RuntimeError("Not connected to Redis")
            if expire:
                await self.client.setex(key, expire, value)
            else:
                await self.client.set(key, value)
        except Exception as e:
            logg_error(f"Failed to set key {key}: {e}")
            raise

    async def setnx(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        try:
            if not self.client:
                raise RuntimeError("Not connected to Redis")
            result = await self.client.setnx(key, value)
            if result and expire:
                await self.client.expire(key, expire)
            return bool(result)
        except Exception as e:
            logg_error(f"Failed to setnx key {key}: {e}")
            raise

    async def delete(self, key: str) -> None:
        try:
            if not self.client:
                raise RuntimeError("Not connected to Redis")
            await self.client.delete(key)
        except Exception as e:
            logg_error(f"Failed to delete key {key}: {e}")
            raise

    async def exists(self, key: str) -> bool:
        try:
            if not self.client:
                raise RuntimeError("Not connected to Redis")
            return bool(await self.client.exists(key))
        except Exception as e:
            logg_error(f"Failed to check existence of key {key}: {e}")
            raise

    async def expire(self, key: str, seconds: int) -> None:
        try:
            if not self.client:
                raise RuntimeError("Not connected to Redis")
            await self.client.expire(key, seconds)
        except Exception as e:
            logg_error(f"Failed to set expire for key {key}: {e}")
            raise

    async def close(self) -> None:
        try:
            if self.client:
                await self.client.close()
                logg_info("✓ Async Redis connection closed")
        except Exception as e:
            logg_error(f"Error closing Async Redis connection: {e}")
