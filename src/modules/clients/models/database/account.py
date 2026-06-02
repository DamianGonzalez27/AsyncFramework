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

from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.clients.models.database.timestamps import TimestampMixin
from .database import Base

# -------------------------
# Modelo Account
#
#    Representa una cuenta o contexto de infraestructura donde se realizan
#    los despliegues de aplicaciones.
#
#    Una cuenta puede corresponder a:
#    - Una cuenta de AWS
#    - Un proyecto de GCP
#    - Una suscripción de Azure
#    - Un entorno on-premise
#    - Cualquier proveedor o contexto de infraestructura
#
#    Este modelo actúa como frontera lógica entre aplicaciones y la
#    infraestructura donde serán desplegadas.
# -------------------------
class Account(Base, TimestampMixin):

    __tablename__ = "accounts"

    # -------------------------
    # Identificador único
    # -------------------------
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    # -------------------------
    # Información básica
    # -------------------------
    name = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )

    description = Column(
        String,
        nullable=True
    )

    provider = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="active"
    )

    # -------------------------
    # Clave foránea
    # -------------------------
    client_id = Column(
        UUID(as_uuid=True),
        ForeignKey("clients.id"),
        nullable=False,
        index=True
    )

    # -------------------------
    # Relaciones
    # -------------------------
    aplications = relationship(
        "Aplication",
        back_populates="account"
    )

    deployments = relationship(
        "Deployment",
        back_populates="account"
    )

    client = relationship(
        "Client",
        back_populates="accounts"
    )

    credentials = relationship(
        "AccountCredential",
        back_populates="account",
        cascade="all, delete-orphan"
    )
