from typing import Optional
from src.adapters.async_redis_adapter import AsyncRedisAdapter
from logger_tracker import logg_debug, logg_error


class IdempotencyStore:
    def __init__(
        self,
        redis: AsyncRedisAdapter,
        ttl: int = 86400,
    ):
        self.redis = redis
        self.ttl = ttl

    async def is_processed(self, event_id: str) -> bool:
        key = f"idempotency:{event_id}"
        return await self.redis.exists(key)

    async def mark_processed(self, event_id: str, ttl: Optional[int] = None) -> None:
        key = f"idempotency:{event_id}"
        await self.redis.set(key, "1", expire=ttl or self.ttl)
        logg_debug(f"Idempotency key set: {key}")

    async def try_acquire(self, event_id: str, ttl: Optional[int] = None) -> bool:
        key = f"idempotency:{event_id}"
        acquired = await self.redis.setnx(key, "1", expire=ttl or self.ttl)
        if acquired:
            logg_debug(f"Idempotency lock acquired: {key}")
        else:
            logg_debug(f"Idempotency lock exists (skipped): {key}")
        return acquired

    async def get_state(self, aggregate_id: str) -> Optional[str]:
        key = f"state:{aggregate_id}"
        return await self.redis.get(key)

    async def set_state(
        self,
        aggregate_id: str,
        state: str,
        ttl: Optional[int] = None,
    ) -> None:
        key = f"state:{aggregate_id}"
        await self.redis.set(key, state, expire=ttl or self.ttl)
        logg_debug(f"State updated for {aggregate_id}")
