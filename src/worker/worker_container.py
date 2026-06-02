import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.utils import get_database_url
from src.config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    RABBITMQ_VHOST,
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_SECURITY_PROTOCOL,
    KAFKA_SASL_MECHANISM,
    KAFKA_SASL_USERNAME,
    KAFKA_SASL_PASSWORD,
    REDIS_URL,
    REDIS_PASSWORD,
    WORKER_RABBITMQ_PREFETCH,
    WORKER_IDEMPOTENCY_TTL,
    OUTBOX_QUEUE,
    KAFKA_CONSUMER_GROUP,
)
from src.adapters.async_rabbitmq_adapter import AsyncRabbitMQAdapter
from src.adapters.async_kafka_adapter import AsyncKafkaAdapter
from src.adapters.async_redis_adapter import AsyncRedisAdapter
from src.worker.idempotency import IdempotencyStore
from src.worker.outbox_processor import OutboxProcessor
from src.worker.rabbit_consumer import RabbitConsumer
from src.worker.kafka_publisher import KafkaEventPublisher
from src.worker.health import HealthChecker


class WorkerContainer:
    def __init__(self):
        self.engine = create_engine(
            get_database_url(),
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        self.session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
            )
        )

        self.rabbit = AsyncRabbitMQAdapter(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            username=RABBITMQ_USER,
            password=RABBITMQ_PASSWORD,
            vhost=RABBITMQ_VHOST,
            prefetch_count=WORKER_RABBITMQ_PREFETCH,
        )

        kafka_servers = (
            KAFKA_BOOTSTRAP_SERVERS.split(",")
            if isinstance(KAFKA_BOOTSTRAP_SERVERS, str)
            else KAFKA_BOOTSTRAP_SERVERS
        )
        self.kafka = AsyncKafkaAdapter(
            bootstrap_servers=kafka_servers,
            client_id="kerverus-worker",
            security_protocol=KAFKA_SECURITY_PROTOCOL,
            sasl_mechanism=KAFKA_SASL_MECHANISM or None,
            sasl_username=KAFKA_SASL_USERNAME or None,
            sasl_password=KAFKA_SASL_PASSWORD or None,
        )

        self.redis = AsyncRedisAdapter(
            url=REDIS_URL,
            password=REDIS_PASSWORD,
        )

        self.idempotency = IdempotencyStore(
            redis=self.redis,
            ttl=WORKER_IDEMPOTENCY_TTL,
        )

        self.kafka_publisher = KafkaEventPublisher(
            kafka=self.kafka,
        )

        self.health_checker = HealthChecker(
            session_factory=self.session_factory,
            rabbit=self.rabbit,
            kafka=self.kafka,
            redis=self.redis,
        )

    async def connect_all(self) -> None:
        await self.rabbit.connect()
        await self.kafka.connect_producer()
        await self.redis.connect()

    async def disconnect_all(self) -> None:
        await self.rabbit.close()
        await self.kafka.close()
        await self.redis.close()
        self.session_factory.close_all()
        self.engine.dispose()

    async def create_outbox_processor(self) -> OutboxProcessor:
        return OutboxProcessor(
            session_factory=self.session_factory,
            rabbit=self.rabbit,
            kafka=self.kafka,
        )

    async def create_rabbit_consumer(
        self,
        message_handler,
        queue_name: str = OUTBOX_QUEUE,
    ) -> RabbitConsumer:
        return RabbitConsumer(
            rabbit=self.rabbit,
            queue_name=queue_name,
            message_handler=message_handler,
            prefetch_count=WORKER_RABBITMQ_PREFETCH,
        )
