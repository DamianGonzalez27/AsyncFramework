"""
Worker asíncrono para procesamiento de eventos fuera de la cola.

Implementa los patrones:
- Transactional Outbox
- Idempotencia basada en Redis
- Correlación de eventos (correlation_id)
- Dead Letter Queue con reintentos
- Publicación asíncrona a Kafka
- Concurrencia controlada vía aio-pika + asyncio
- Health checks y observabilidad
"""
