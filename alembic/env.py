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
import logging
import sys
import os

from sqlalchemy import create_engine
from sqlalchemy import pool

# -------------------------
# Configuración del path del proyecto
#
# Se agrega el directorio raíz del proyecto al PYTHONPATH
# para permitir imports absolutos desde `src`.
# -------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logging.getLogger("alembic").setLevel(logging.INFO)

from src.utils import get_database_url

from alembic import context

# -------------------------
# Metadata de los modelos ORM
#
# Base contiene el metadata global usado por Alembic
# para la generación automática de migraciones.
# -------------------------
from src.modules.clients.models.database.database import Base


# -------------------------
# Registro explícito de modelos
#
# IMPORTANTE:
# Estos imports son intencionales y necesarios.
# Aseguran que todos los modelos se carguen en memoria
# y se registren dentro de Base.metadata, permitiendo
# que Alembic detecte correctamente el esquema.
#
# NO eliminar aunque parezcan "no usados".
# -------------------------
from src.modules.clients.models.database.account import Account
from src.modules.clients.models.database.repo import Repo
from src.modules.clients.models.database.application import Aplication
from src.modules.clients.models.database.environment import Environment
from src.modules.clients.models.database.deployment import Deployment
from src.modules.clients.models.database.environment_variables import ApplicationEnvironmentVariable
from src.modules.clients.models.database.client import Client
from src.modules.clients.models.database.outbox import OutboxMessage

# -------------------------
# Configuración principal de Alembic
#
# Objeto central que contiene la configuración cargada
# desde el archivo alembic.ini
# -------------------------
config = context.config

# -------------------------
# Configuración del sistema de logging
#
# Interpreta el archivo de configuración de logging
# definido en alembic.ini (si existe).
# -------------------------
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# -------------------------
# Metadata objetivo para autogenerate
#
# Alembic usará este metadata para:
# - Detectar cambios en los modelos
# - Generar scripts de migración
# -------------------------
target_metadata = Base.metadata

# -------------------------
# Ejecución de migraciones en modo OFFLINE
#
# - No crea conexión real a la base de datos
# - Genera SQL puro
# - Útil para revisión o ejecución manual
# -------------------------
def run_migrations_offline() -> None:
    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------
# Ejecución de migraciones en modo ONLINE
#
# - Crea una conexión real a la base de datos
# - Ejecuta directamente las migraciones
# - Es el modo usado normalmente en CI/CD y desarrollo
# -------------------------
def run_migrations_online() -> None:
    connectable = create_engine(
        get_database_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------
# Selección del modo de ejecución
#
# Alembic decide automáticamente si corre en modo
# offline u online según el contexto de ejecución.
# -------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
