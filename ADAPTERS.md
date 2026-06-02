# Adaptadores del Proyecto

Este documento explica cómo usar los adaptadores disponibles en `src/adapters/`.

## Adaptadores Disponibles

### 1. RabbitMQAdapter

Conexión y operaciones con RabbitMQ mediante pika.

```python
from src.adapters import RabbitMQAdapter

# Crear adaptador
adapter = RabbitMQAdapter(
    host="localhost",
    port=5672,
    username="guest",
    password="guest",
    vhost="/"
)

# Conectar
adapter.connect()

# Declarar cola
adapter.declare_queue("my_queue", durable=True)

# Publicar mensaje
adapter.publish("my_queue", {"msg": "hello"})

# Consumir mensajes
def callback(ch, method, properties, body):
    print(f"Received: {body}")
    adapter.ack(method.delivery_tag)

adapter.consume("my_queue", callback)

# Cerrar conexión
adapter.close()
```

### 2. KafkaAdapter

Conexión y operaciones con Apache Kafka mediante kafka-python.

```python
from src.adapters import KafkaAdapter

# Crear adaptador
adapter = KafkaAdapter(
    bootstrap_servers=["localhost:9092"],
    client_id="kerverus-client"
)

# Conectar
adapter.connect()

# Publicar a topic
adapter.publish("my_topic", {"msg": "hello"})

# Suscribirse a topic
adapter.subscribe("my_topic", group_id="my_group")

# Poll mensajes
messages = adapter.poll(timeout_ms=1000)

# Confirmar offset
adapter.commit()

# Cerrar conexión
adapter.close()
```

### 3. RedisAdapter

Conexión y operaciones con Redis mediante redis-py.

```python
from src.adapters import RedisAdapter

# Crear adaptador
adapter = RedisAdapter(
    host="localhost",
    port=6379,
    db=0,
    password=None
)

# Conectar
adapter.connect()

# Establecer valor
adapter.set("key", "value")
adapter.set("key_with_expire", "value", expire=3600)  # 1 hora

# Obtener valor
value = adapter.get("key")

# Verificar existencia
exists = adapter.exists("key")

# Eliminar clave
adapter.delete("key")

# Cerrar conexión
adapter.close()
```

### 4. ElasticsearchAdapter

Conexión y operaciones con Elasticsearch mediante elasticsearch-py.

```python
from src.adapters import ElasticsearchAdapter

# Crear adaptador
adapter = ElasticsearchAdapter(
    hosts=["localhost:9200"],
    scheme="http",
    username=None,
    password=None
)

# Conectar
adapter.connect()

# Crear índice
adapter.create_index(
    "my_index",
    settings={"number_of_shards": 1},
    mappings={"properties": {"title": {"type": "text"}}}
)

# Indexar documento
doc_id = adapter.index_document(
    "my_index",
    body={"title": "My Document"}
)

# Buscar documentos
results = adapter.search(
    "my_index",
    query={"match": {"title": "My"}}
)

# Obtener documento
doc = adapter.get_document("my_index", doc_id)

# Eliminar documento
adapter.delete_document("my_index", doc_id)

# Eliminar índice
adapter.delete_index("my_index")

# Cerrar conexión
adapter.close()
```

### 5. AwsClientFactory

Fábrica de clientes boto3 para AWS con cacheo de sesiones.

```python
from src.adapters import AwsClientFactory

# Obtener cliente S3
s3_client = AwsClientFactory.get_client(
    service_name="s3",
    profile="develop",
    region="us-east-1"
)

# Obtener cliente CloudFormation
cf_client = AwsClientFactory.get_client(
    service_name="cloudformation",
    profile="develop",
    region="us-east-1"
)

# Usar cliente
s3_client.list_buckets()
```

## Logger Tracker

Se utiliza `logger_tracker` en lugar de un logger custom. Importar desde:

```python
from logger_tracker import logg_info, logg_debug, logg_warning, logg_error
```

### Ejemplo de uso:

```python
from logger_tracker import logg_info, logg_debug, logg_error

def process_data():
    logg_info("Starting data processing...")
    try:
        # Tu lógica aquí
        logg_debug("Processing step 1")
        logg_info("Data processed successfully")
    except Exception as e:
        logg_error(f"Error processing data: {e}")
```

## Variables de Entorno de Configuración

```bash
# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_SECURITY_PROTOCOL=PLAINTEXT
KAFKA_SASL_MECHANISM=
KAFKA_SASL_USERNAME=
KAFKA_SASL_PASSWORD=

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Elasticsearch
ELASTICSEARCH_HOSTS=localhost:9200
```

## Notas

- Todos los adaptadores manualhan errores de conexión y las capturan usando `logger_tracker`.
- Los adaptadores son thread-safe donde aplica (p.ej., AwsClientFactory usa Lock para cacheo).
- Se recomienda usar el contenedor de dependencias (`src/containers.py`) para inyectar adaptadores.
