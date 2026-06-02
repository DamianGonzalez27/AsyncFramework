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

from sqlalchemy import Column, String, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.clients.models.database.timestamps import TimestampMixin

from .database import Base


# -------------------------
# Modelo: Aplication
#
# Representa una aplicación desplegable dentro del sistema.
# Una aplicación puede ser desplegada en múltiples entornos
# mediante la entidad Deployment.
#
# Tabla asociada:
# - aplications
#
# Relaciones:
# - Deployment (uno a muchos)
# - Environment (muchos a muchos, vía Deployment)
# -------------------------
class Aplication(Base, TimestampMixin):

    __tablename__ = "aplications"

    # -------------------------
    # Identificador primario
    # -------------------------
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    # -------------------------
    # Metadatos de la aplicación
    # -------------------------
    name = Column(String)
    description = Column(String, index=True)
    template_uri = Column(String)
    type = Column(String)
    status = Column(String)

    # -------------------------
    # Claves foraneas
    # -------------------------
    account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id")
    )

    repo_id = Column(
        UUID(as_uuid=True),
        ForeignKey("repos.id"),
        nullable=False
    )

    # -------------------------
    # Relaciones ORM
    # -------------------------
    deployments = relationship(
        "Deployment",
        back_populates="application",
        cascade="all, delete-orphan"
    )

    environments = relationship(
        "Environment",
        secondary="deployments",
        viewonly=True
    )

    account = relationship(
        "Account",
        back_populates="aplications"
    )

    repo = relationship(
        "Repo",
        back_populates="aplications"
    )

    environment_variables = relationship(
        "ApplicationEnvironmentVariable",
        back_populates="aplication",
        cascade="all, delete-orphan"
    )
