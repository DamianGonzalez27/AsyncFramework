"""
Este proyecto es 100% asíncrono basado en eventos.

No expone una API REST. El punto de entrada es el worker
que reacciona a eventos de RabbitMQ y Kafka.

Ejecutar:
    poetry run worker
"""