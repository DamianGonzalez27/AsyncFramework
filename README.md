# Kerverus Async Framework

Framework asíncrono para servicios modulares con arquitectura hexagonal, orientado a despliegues en infraestructura cloud.

## Arquitectura

El proyecto implementa **Arquitectura Hexagonal (Ports & Adapters)** combinada con **Monolito Modular**, separando claramente el dominio de la infraestructura.

```
src/
├── ports/          # Contratos abstractos (interfaces)
├── adapters/       # Implementaciones concretas de los puertos
├── modules/        # Módulos de negocio independientes
├── worker/         # Worker asíncrono con outbox, idempotencia, DLQ
├── scripts/        # Puntos de entrada
├── containers.py   # Contenedor de dependencias
└── config.py       # Configuración por variables de entorno
```

### Puertos (src/ports/)

Interfaces abstractas que definen contratos para sistemas externos:

| Puerto | Propósito |
|--------|-----------|
| `DatabasePort` | Operaciones con bases de datos relacionales (transacciones, CRUD) |
| `DocumentPort` | Operaciones con bases de datos documentales (MongoDB, CouchDB) |
| `SearchPort` | Búsqueda e indexación (Elasticsearch/OpenSearch) |
| `HTTPPort` | Cliente HTTP/REST (GET, POST, PUT, PATCH, DELETE) |
| `RabbitMQPort` | Mensajería RabbitMQ |
| `KafkaPort` | Mensajería Kafka |
| `PostgresPort` | Operaciones específicas de PostgreSQL |
| `RedisPort` | Cache y almacenamiento clave-valor |

### Adaptadores (src/adapters/)

Implementaciones concretas de los puertos:

| Adaptador | Tecnología | Sync/Async |
|-----------|-----------|------------|
| `RabbitMQAdapter` | pika | Sync |
| `AsyncRabbitMQAdapter` | aio-pika | Async |
| `KafkaAdapter` | kafka-python | Sync |
| `AsyncKafkaAdapter` | aiokafka | Async |
| `RedisAdapter` | redis-py | Sync |
| `AsyncRedisAdapter` | redis.asyncio | Async |
| `ElasticsearchAdapter` | elasticsearch-py | Sync |
| `AwsClientFactory` | boto3 | Sync |

## Módulos de Negocio

Cada módulo en `src/modules/` sigue una estructura consistente:

```
module/
├── controllers/   # Endpoints HTTP con decoradores de validación
├── services/      # Lógica de negocio
├── repositories/  # Acceso a datos
└── models/        # Modelos Pydantic y SQLAlchemy
```

### Módulos incluidos

- **clients** — Modelos HTTP y de base de datos compartidos
- **users** — Gestión de cuentas, clientes, repositorios, aplicaciones y despliegues
- **payments** — Ejemplo de módulo de pagos
- **products** — Ejemplo de módulo de productos

## Worker Asíncrono

El worker en `src/worker/` implementa patrones de sistemas distribuidos:

### Transactional Outbox (`outbox_processor.py`)
- Polling periódico de la tabla `outbox_messages`
- Publicación a RabbitMQ y/o Kafka según el destino
- Actualización de estado (PENDING → SENT / FAILED)

### Rabbit Consumer (`rabbit_consumer.py`)
- Consumo controlado con prefetch count
- Reintentos configurables con backoff
- Dead Letter Queue (DLQ) mediante encabezado `x-retry-count`

### Kafka Event Publisher (`kafka_publisher.py`)
- Enriquecimiento de eventos con metadatos (event_id, correlation_id, timestamp)
- Topic de errores separado

### Idempotencia (`idempotency.py`)
- Almacenamiento en Redis con SETNX
- TTL configurable para limpieza automática
- Seguimiento de estado de agregados

### Health Check (`health.py`)
- Verificación periódica de dependencias: base de datos, RabbitMQ, Kafka, Redis
- Reporte agregado con estado por servicio

## Librerías Externas

| Librería | Propósito |
|----------|-----------|
| `global-handler` | Manejo de errores HTTP, validación de requests y métricas. Proporciona `BaseController`, decoradores `validate_with`/`validate_query_with`/`validate_headers_with`, y registro global de errores |
| `logger-tracker` | Logging estructurado con trazabilidad por request |
| `config-mounter` | Montaje de configuración desde variables de entorno |
| `global-repository` | Repositorio base genérico para SQLAlchemy |
| `sqlalchemy` | ORM para base de datos relacional |
| `alembic` | Migraciones de base de datos |
| `pydantic` | Validación y serialización de datos |
| `aio-pika` | Cliente asíncrono para RabbitMQ |
| `aiokafka` | Cliente asíncrono para Kafka |

## Variables de Entorno

### Base de Datos
- `CONNECTORS_DATABASE_DRIVER`, `CONNECTORS_DATABASE_HOST`, `CONNECTORS_DATABASE_PORT`
- `CONNECTORS_DATABASE_NAME`, `CONNECTORS_DATABASE_USER`, `CONNECTORS_DATABASE_PASSWORD`
- `DATABASE_URL` (URL completa, anula las anteriores)

### RabbitMQ
- `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`, `RABBITMQ_VHOST`

### Kafka
- `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_SECURITY_PROTOCOL`, `KAFKA_SASL_MECHANISM`
- `KAFKA_SASL_USERNAME`, `KAFKA_SASL_PASSWORD`
- `KAFKA_EVENTS_TOPIC`, `KAFKA_ERROR_TOPIC`, `KAFKA_CONSUMER_GROUP`

### Redis
- `REDIS_URL`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, `REDIS_PASSWORD`

### Worker
- `WORKER_OUTBOX_POLL_INTERVAL`, `WORKER_RABBITMQ_PREFETCH`
- `WORKER_RABBITMQ_RETRY_DELAY`, `WORKER_RABBITMQ_MAX_RETRIES`
- `WORKER_HEARTBEAT_INTERVAL`, `WORKER_IDEMPOTENCY_TTL`

### Global Handler
- `GLOBAL_HANDLER_DEBUG`, `GLOBAL_HANDLER_ENV`, `GLOBAL_HANDLER_SANITIZE_ERRORS`
- `GLOBAL_HANDLER_LOG_LEVEL`, `GLOBAL_HANDLER_CORRELATION_HEADER`, `GLOBAL_HANDLER_USER_ID_HEADER`

## Ejecución

```bash
# Instalar dependencias
poetry install

# Ejecutar worker asíncrono
poetry run worker

# Ejecutar pruebas
poetry run pytest
```

## Pruebas

```bash
poetry run pytest
poetry run pytest --cov=src --cov-report=term-missing
```
