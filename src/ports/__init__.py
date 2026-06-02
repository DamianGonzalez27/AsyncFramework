# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
#
# Este software y su código fuente han sido desarrollados por Erick Damian Gonzalez Aranda, mediante 
# NeuronexoTec Organizacion de desarrollo de Software.
# Todos los derechos están reservados.
#
# Se permite el uso, copia y modificación del código únicamente para fines
# personales, educativos o internos, siempre que se conserve este aviso
# de copyright y no se redistribuya el software, total o parcialmente,
# sin autorización expresa del autor.
#
# Queda estrictamente prohibida la venta, sublicencia, redistribución,
# exposición como servicio (SaaS), o incorporación en productos comerciales
# sin consentimiento previo y por escrito del autor.
#
# Este software se proporciona "tal cual", sin garantía de ningún tipo,
# expresa o implícita, incluyendo pero no limitado a garantías de
# comercialización, idoneidad para un propósito particular o ausencia
# de defectos.
# 
# El autor no será responsable por ningún daño directo o indirecto
# derivado del uso de este software.
# -------------------------

"""
Paquete de puertos (Ports & Adapters).

Este paquete contiene las interfaces abstractas (puertos) que definen
los contratos para los adaptadores de conexión a sistemas externos.

Clases disponibles:
- BasePort: Clase base para todos los puertos
- DatabasePort: Interfaz para bases de datos relacionales
- DocumentPort: Interfaz para bases de datos de documentos
- SearchPort: Interfaz para motores de búsqueda
- HTTPPort: Interfaz para APIs HTTP/REST
"""

from src.ports.base_port import BasePort, ConnectionStatus
from src.ports.database_port import DatabasePort
from src.ports.document_port import DocumentPort, InsertResult, UpdateResult, DeleteResult
from src.ports.search_port import SearchPort, SearchResult, IndexResult
from src.ports.http_port import HTTPPort, HTTPMethod, HTTPResponse, HTTPCredentials
from src.ports.rabbitmq_port import RabbitMQPort
from src.ports.kafka_port import KafkaPort
from src.ports.postgres_port import PostgresPort
from src.ports.redis_port import RedisPort

__all__ = [
    # Base
    "BasePort",
    "ConnectionStatus",
    # Database
    "DatabasePort",
    # Document
    "DocumentPort",
    "InsertResult",
    "UpdateResult",
    "DeleteResult",
    # Search
    "SearchPort",
    "SearchResult",
    "IndexResult",
    # HTTP
    "HTTPPort",
    "HTTPMethod",
    "HTTPResponse",
    "HTTPCredentials",
    # Messaging
    "RabbitMQPort",
    "KafkaPort",
    # Relational DB
    "PostgresPort",
    # Cache
    "RedisPort",
]