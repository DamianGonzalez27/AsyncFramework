# Kerverus Server - Transactional Service Framework

Este repositorio es un punto de partida para un monolito modular con orientación a arquitectura hexagonal.
La estructura prioriza módulos independientes en `src/modules`, puertos en `src/ports`, adaptadores limpios en `src/adapters` y pruebas unitarias específicas en `tests/modules`.

## Objetivo

Este proyecto funciona como un boilerplate para desarrollar servicios internos en una sola aplicación, manteniendo:

- Módulos independientes con sus enlaces de negocio, repositorios y controladores.
- Puertos (`src/ports`) como contratos para adaptadores externos.
- Adaptadores y utilidades fuera del dominio en `src/adapters`.
- Configuraciones compatibles con PostgreSQL y Alembic.
- Soporte base para mensajería y cache: RabbitMQ, Kafka y Redis.

## Estructura principal

- `src/modules/` — módulos del dominio en formato monolito modular.
- `src/ports/` — definiciones de puertos para bases de datos, mensajería y cache.
- `src/adapters/` — adaptadores concretos para RabbitMQ, Kafka, Redis, Elasticsearch y AWS.
- `src/config.py` — configuración por variables de entorno.
- `src/containers.py` — contenedor de dependencias.
- `src/scripts/run_server.py` — arranque de la aplicación.
- `tests/modules/` — ejemplos de pruebas unitarias por módulo.

## Módulos de ejemplo

- `clients`
- `payments`
- `products`
- `users`

Cada módulo expone su propio blueprint y su estructura base de:

- `controllers/`
- `models/`
- `repositories/`
- `services/`

## Adaptadores disponibles

El proyecto incluye adaptadores concretos para sistemas externos:

- **RabbitMQAdapter** — conexión y operaciones con RabbitMQ
- **KafkaAdapter** — conexión y operaciones con Apache Kafka
- **RedisAdapter** — conexión y operaciones con Redis
- **ElasticsearchAdapter** — indexación y búsqueda con Elasticsearch
- **AwsClientFactory** — fábrica de clientes boto3 para AWS

Ver [ADAPTERS.md](./ADAPTERS.md) para documentación completa de uso.

## Logging

El proyecto utiliza `logger-tracker` para logging estructurado. Ver:
https://pypi.org/project/logger-tracker/

Importar en servicios y repositorios:

```python
from logger_tracker import logg_info, logg_debug, logg_warning, logg_error
```

El proyecto utiliza PostgreSQL como base de datos principal y Alembic para migraciones.
Las variables de entorno disponibles incluyen:

- `CONNECTORS_DATABASE_DRIVER`
- `CONNECTORS_DATABASE_HOST`
- `CONNECTORS_DATABASE_PORT`
- `CONNECTORS_DATABASE_NAME`
- `CONNECTORS_DATABASE_USER`
- `CONNECTORS_DATABASE_PASSWORD`
- `DATABASE_URL`
- `RABBITMQ_HOST`
- `RABBITMQ_PORT`
- `RABBITMQ_USER`
- `RABBITMQ_PASSWORD`
- `RABBITMQ_VHOST`
- `KAFKA_BOOTSTRAP_SERVERS`
- `KAFKA_SECURITY_PROTOCOL`
- `REDIS_URL`
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_DB`
- `REDIS_PASSWORD`

## Ejecutar el servidor

```bash
poetry install
poetry run server
```

## Ejecutar pruebas

```bash
poetry run pytest
```

## Notas importantes

- Esta rama está orientada a un `monolito modular`.
- No se aceptan contribuciones externas en este momento.
- La carpeta `src/controllers` y `src/clients` han sido removidas para reforzar la nueva estructura.
