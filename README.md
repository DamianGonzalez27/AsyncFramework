# Kerverus Async Framework

Framework **100% asíncrono** para procesamiento de eventos basado en arquitectura hexagonal y monolito modular. Reacciona exclusivamente a eventos de **RabbitMQ** y **Kafka** — no expone API REST.

## Arquitectura

El proyecto implementa **Arquitectura Hexagonal (Ports & Adapters)** combinada con **Monolito Modular**:

```
src/
├── ports/          # Contratos abstractos (interfaces)
├── adapters/       # Implementaciones concretas (RabbitMQ, Kafka, Redis, etc.)
├── modules/        # Módulos de dominio con servicios, handlers y modelos
│   └── handlers/   # Handlers que procesan eventos del dominio
├── worker/         # Worker asíncrono (outbox, idempotencia, DLQ, health check)
└── scripts/        # Punto de entrada del worker
```

### Flujo de procesamiento

```
RabbitMQ ──► RabbitConsumer ──► handle_message()
                                    │
                          ┌─────────┴──────────┐
                          ▼                    ▼
                  KafkaPublisher        EventDispatcher
                  (trazabilidad)              │
                                     ┌───────┴───────┐
                                     ▼               ▼
                              AccountHandler   ClientHandler
                              RepoHandler      PaymentHandler
                              ApplicationHandler ProductHandler
                                     │
                                     ▼
                              Domain Services
                              (reglas de negocio)
```

## Módulos de Dominio

Cada módulo en `src/modules/` representa un conjunto de reglas de negocio y contiene:

```
module/
├── handlers/      # Procesan eventos del dominio (ej: account.created)
├── services/      # Lógica de negocio pura
├── repositories/  # Acceso a datos
└── models/        # Modelos Pydantic y SQLAlchemy
```

### Módulos incluidos

| Módulo | Handlers | Servicios |
|--------|----------|-----------|
| **clients** | `client.created`, `client.updated` | `ClientService` |
| **users** | `account.*`, `user.client.*`, `repo.created`, `application.*` | `AccountService`, `ClientService`, `RepoService`, `ApplicationService` |
| **payments** | `payment.processed`, `payment.refunded` | `PaymentService` |
| **products** | `product.created`, `product.updated` | `ProductService` |

### Ejemplo: Handler de dominio

```python
# src/modules/users/handlers/account_handler.py

class AccountHandler:
    @staticmethod
    async def handle_created(payload: Dict[str, Any], **kwargs) -> None:
        service = AccountService(repository=container.account_repository)
        data = AccountCreateRequest(**payload)
        account = service.create_account(data)  # aplica reglas de negocio
```

Los handlers se registran en `src/modules/handlers/__init__.py`:

```python
EVENT_HANDLERS = {
    "account.created": AccountHandler.handle_created,
    "client.created": ClientHandler.handle_created,
    "payment.processed": PaymentHandler.handle_processed,
    ...
}
```

## Puertos y Adaptadores

### Puertos (src/ports/)

Interfaces abstractas para sistemas externos:

| Puerto | Propósito |
|--------|-----------|
| `RabbitMQPort` | Mensajería RabbitMQ |
| `KafkaPort` | Mensajería Kafka |
| `RedisPort` | Cache y almacenamiento clave-valor |
| `DatabasePort` | Operaciones con bases de datos relacionales |
| `PostgresPort` | Operaciones específicas de PostgreSQL |
| `DocumentPort` | Operaciones con bases de datos documentales |
| `SearchPort` | Búsqueda e indexación (Elasticsearch) |
| `HTTPPort` | Cliente HTTP para integraciones externas |

### Adaptadores (src/adapters/)

| Adaptador | Tecnología | Sync/Async |
|-----------|-----------|------------|
| `AsyncRabbitMQAdapter` | aio-pika | Async |
| `AsyncKafkaAdapter` | aiokafka | Async |
| `AsyncRedisAdapter` | redis.asyncio | Async |
| `RabbitMQAdapter` | pika | Sync |
| `KafkaAdapter` | kafka-python | Sync |
| `RedisAdapter` | redis-py | Sync |
| `ElasticsearchAdapter` | elasticsearch-py | Sync |
| `AwsClientFactory` | boto3 | Sync |

## Worker Asíncrono

El worker en `src/worker/` implementa patrones de sistemas distribuidos:

### Transactional Outbox (`outbox_processor.py`)
- Polling periódico de `outbox_messages` (PENDING → SENT / FAILED)
- Publicación a RabbitMQ y/o Kafka según el destino del mensaje

### Rabbit Consumer (`rabbit_consumer.py`)
- Consumo controlado con prefetch count
- Reintentos configurables con Dead Letter Queue (DLQ)
- Despacho a handlers de módulo según `event_type`

### Kafka Event Publisher (`kafka_publisher.py`)
- Enriquecimiento de eventos con `event_id`, `correlation_id`, `timestamp`
- Publicación a topics de eventos y errores

### Idempotencia (`idempotency.py`)
- Almacenamiento en Redis con SETNX + TTL configurable
- Evita procesamiento duplicado de eventos

### Health Check (`health.py`)
- Verificación periódica de dependencias (PostgreSQL, RabbitMQ, Kafka, Redis)
- Reporte agregado con estado por servicio

## Variables de Entorno

### Base de Datos
`CONNECTORS_DATABASE_*`, `DATABASE_URL`

### RabbitMQ
`RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`, `RABBITMQ_VHOST`

### Kafka
`KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_SECURITY_PROTOCOL`, `KAFKA_SASL_MECHANISM`, `KAFKA_SASL_USERNAME`, `KAFKA_SASL_PASSWORD`
`KAFKA_EVENTS_TOPIC`, `KAFKA_ERROR_TOPIC`, `KAFKA_CONSUMER_GROUP`

### Redis
`REDIS_URL`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, `REDIS_PASSWORD`

### Worker
`WORKER_OUTBOX_POLL_INTERVAL`, `WORKER_RABBITMQ_PREFETCH`, `WORKER_RABBITMQ_RETRY_DELAY`
`WORKER_RABBITMQ_MAX_RETRIES`, `WORKER_HEARTBEAT_INTERVAL`, `WORKER_IDEMPOTENCY_TTL`

### Outbox
`OUTBOX_QUEUE`, `OUTBOX_DLQ`, `OUTBOX_DLX`

## Ejecución

```bash
# Instalar dependencias
poetry install

# Ejecutar el worker
poetry run worker

# Ejecutar pruebas
poetry run pytest
```

## Docker

```bash
docker build -t kerverus-async .
docker run kerverus-async
```

## Pruebas

```bash
poetry run pytest
poetry run pytest --cov=src --cov-report=term-missing
```
