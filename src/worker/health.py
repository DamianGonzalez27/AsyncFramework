import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from src.adapters.async_rabbitmq_adapter import AsyncRabbitMQAdapter
from src.adapters.async_kafka_adapter import AsyncKafkaAdapter
from src.adapters.async_redis_adapter import AsyncRedisAdapter
from sqlalchemy import text
from sqlalchemy.orm import scoped_session
from logger_tracker import logg_info, logg_error


@dataclass
class HealthCheckResult:
    status: str = "healthy"
    checks: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class HealthChecker:
    def __init__(
        self,
        session_factory: scoped_session,
        rabbit: AsyncRabbitMQAdapter,
        kafka: AsyncKafkaAdapter,
        redis: AsyncRedisAdapter,
    ):
        self.session_factory = session_factory
        self.rabbit = rabbit
        self.kafka = kafka
        self.redis = redis

    async def check_all(self) -> HealthCheckResult:
        checks = {}

        checks["database"] = await self._check_database()
        checks["rabbitmq"] = await self._check_rabbitmq()
        checks["kafka"] = await self._check_kafka()
        checks["redis"] = await self._check_redis()

        all_healthy = all(
            c.get("healthy", False) for c in checks.values()
        )

        return HealthCheckResult(
            status="healthy" if all_healthy else "degraded",
            checks=checks,
        )

    async def _check_database(self) -> Dict[str, Any]:
        try:
            def _ping():
                session = self.session_factory()
                try:
                    session.execute(text("SELECT 1"))
                    session.commit()
                    return True
                finally:
                    session.close()

            result = await asyncio.to_thread(_ping)
            return {"healthy": result, "message": "Database reachable"}
        except Exception as e:
            logg_error(f"Database health check failed: {e}")
            return {"healthy": False, "message": str(e)}

    async def _check_rabbitmq(self) -> Dict[str, Any]:
        try:
            connected = (
                self.rabbit.connection is not None
                and not self.rabbit.connection.is_closed
            )
            return {
                "healthy": connected,
                "message": "RabbitMQ connected" if connected else "RabbitMQ not connected",
            }
        except Exception as e:
            logg_error(f"RabbitMQ health check failed: {e}")
            return {"healthy": False, "message": str(e)}

    async def _check_kafka(self) -> Dict[str, Any]:
        try:
            connected = self.kafka.producer is not None
            return {
                "healthy": connected,
                "message": "Kafka producer connected" if connected else "Kafka not connected",
            }
        except Exception as e:
            logg_error(f"Kafka health check failed: {e}")
            return {"healthy": False, "message": str(e)}

    async def _check_redis(self) -> Dict[str, Any]:
        try:
            await self.redis.client.ping()
            return {"healthy": True, "message": "Redis reachable"}
        except Exception as e:
            logg_error(f"Redis health check failed: {e}")
            return {"healthy": False, "message": str(e)}
