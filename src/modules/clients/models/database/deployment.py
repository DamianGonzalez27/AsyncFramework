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

from sqlalchemy import Column, String, text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.modules.clients.models.database.timestamps import TimestampMixin

from .database import Base


# -------------------------
# Modelo: Deployment
#
# Representa el despliegue de una aplicación en un entorno específico.
# Este modelo actúa como entidad intermedia entre Aplication y Environment
# y contiene la información operativa del despliegue.
#
# Tabla asociada:
# - deployments
#
# Relaciones:
# - Aplication (muchos a uno)
# - Environment (muchos a uno)
# -------------------------
class Deployment(Base, TimestampMixin):

    __tablename__ = "deployments"

    # -------------------------
    # Identificador primario
    # -------------------------
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    # -------------------------
    # Relaciones foráneas
    # -------------------------
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("aplications.id"),
        nullable=False
    )

    environment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("environments.id"),
        nullable=False
    )

    account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id"),
        nullable=False
    )

    # -------------------------
    # Información del despliegue
    # -------------------------
    deploy_version = Column(String, nullable=False)
    region = Column(String, nullable=False)
    status = Column(String, nullable=False)

    env_snapshot = Column(
        JSONB,
        nullable=False
    )

    # -------------------------
    # Auditoría
    # -------------------------
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # -------------------------
    # Relaciones ORM
    # -------------------------
    application = relationship(
        "Aplication",
        back_populates="deployments"
    )

    environment = relationship(
        "Environment",
        back_populates="deployments"
    )

    account = relationship(
        "Account",
        back_populates="deployments"
    )
