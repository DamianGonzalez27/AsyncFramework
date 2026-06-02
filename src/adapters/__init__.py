"""Adaptadores del proyecto.

Este paquete contiene implementaciones de adaptadores que cumplen los
contratos definidos en `src.ports` para sistemas externos:

- RabbitMQAdapter: conexión y operaciones con RabbitMQ (síncrono)
- KafkaAdapter: conexión y operaciones con Apache Kafka (síncrono)
- RedisAdapter: conexión y operaciones con Redis (síncrono)
- ElasticsearchAdapter: conexión y operaciones con Elasticsearch
- AwsClientFactory: fábrica de clientes boto3 para AWS
- AsyncRabbitMQAdapter: conexión y operaciones con RabbitMQ (asíncrono, aio-pika)
- AsyncKafkaAdapter: conexión y operaciones con Apache Kafka (asíncrono, aiokafka)
- AsyncRedisAdapter: conexión y operaciones con Redis (asíncrono, redis.asyncio)
"""

from src.adapters.rabbitmq_adapter import RabbitMQAdapter
from src.adapters.kafka_adapter import KafkaAdapter
from src.adapters.redis_adapter import RedisAdapter
from src.adapters.elasticsearch_adapter import ElasticsearchAdapter
from src.adapters.aws_client_factory import AwsClientFactory
from src.adapters.async_rabbitmq_adapter import AsyncRabbitMQAdapter
from src.adapters.async_kafka_adapter import AsyncKafkaAdapter
from src.adapters.async_redis_adapter import AsyncRedisAdapter

__all__ = [
    "RabbitMQAdapter",
    "KafkaAdapter",
    "RedisAdapter",
    "ElasticsearchAdapter",
    "AwsClientFactory",
    "AsyncRabbitMQAdapter",
    "AsyncKafkaAdapter",
    "AsyncRedisAdapter",
]
