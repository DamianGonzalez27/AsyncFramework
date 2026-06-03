import os
import config_mounter
# Configuración de la base de datos
DB_DRIVER = os.environ.get("CONNECTORS_DATABASE_DRIVER")
# Host de la base de datos
DB_HOST = os.environ.get("CONNECTORS_DATABASE_HOST")
# Puerto de la base de datos
DB_PORT = os.environ.get("CONNECTORS_DATABASE_PORT")

# Nombre de la base de datos
DB_NAME = os.environ.get("CONNECTORS_DATABASE_NAME")

# Usuario de la base de datos
DB_USER = os.environ.get("CONNECTORS_DATABASE_USER")

# Contraseña de la base de datos
DB_PASSWORD = os.environ.get("CONNECTORS_DATABASE_PASSWORD")

# URL completa para PostgreSQL (override si está presente)
DATABASE_URL = os.environ.get("DATABASE_URL")

# RabbitMQ
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.environ.get("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "guest")
RABBITMQ_VHOST = os.environ.get("RABBITMQ_VHOST", "/")

# Kafka
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_SECURITY_PROTOCOL = os.environ.get("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT")
KAFKA_SASL_MECHANISM = os.environ.get("KAFKA_SASL_MECHANISM", "")
KAFKA_SASL_USERNAME = os.environ.get("KAFKA_SASL_USERNAME", "")
KAFKA_SASL_PASSWORD = os.environ.get("KAFKA_SASL_PASSWORD", "")

# Redis
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

CAPABILITIES = ['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM', 'CAPABILITY_AUTO_EXPAND']

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")

# Worker
WORKER_OUTBOX_POLL_INTERVAL = int(os.environ.get("WORKER_OUTBOX_POLL_INTERVAL", 5))
WORKER_RABBITMQ_PREFETCH = int(os.environ.get("WORKER_RABBITMQ_PREFETCH", 20))
WORKER_RABBITMQ_RETRY_DELAY = int(os.environ.get("WORKER_RABBITMQ_RETRY_DELAY", 1000))
WORKER_RABBITMQ_MAX_RETRIES = int(os.environ.get("WORKER_RABBITMQ_MAX_RETRIES", 3))
WORKER_HEARTBEAT_INTERVAL = int(os.environ.get("WORKER_HEARTBEAT_INTERVAL", 30))
WORKER_IDEMPOTENCY_TTL = int(os.environ.get("WORKER_IDEMPOTENCY_TTL", 86400))

# Outbox
OUTBOX_QUEUE = os.environ.get("OUTBOX_QUEUE", "outbox.events")
OUTBOX_DLQ = os.environ.get("OUTBOX_DLQ", "outbox.events.dlq")
OUTBOX_DLX = os.environ.get("OUTBOX_DLX", "outbox.events.dlx")

# Kafka topics
KAFKA_EVENTS_TOPIC = os.environ.get("KAFKA_EVENTS_TOPIC", "domain.events")
KAFKA_ERROR_TOPIC = os.environ.get("KAFKA_ERROR_TOPIC", "domain.events.errors")
KAFKA_CONSUMER_GROUP = os.environ.get("KAFKA_CONSUMER_GROUP", "kerverus-worker")