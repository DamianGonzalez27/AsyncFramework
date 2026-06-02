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

from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.clients.models.database.timestamps import TimestampMixin
from .database import Base

# -------------------------
# Modelo Repo
#
# Representa un repositorio de código fuente que contiene
# una o más aplicaciones desplegables.
#
# El repositorio es una entidad independiente del proveedor
# (GitHub, GitLab, Bitbucket, etc.) y sirve como punto de
# referencia para versionado, templates y pipelines.
# -------------------------
class Repo(Base, TimestampMixin):

    __tablename__ = "repos"

    # -------------------------
    # Identificador único
    # -------------------------
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    # -------------------------
    # Información del repositorio
    # -------------------------
    name = Column(
        String,
        nullable=False,
        index=True
    )

    provider = Column(
        String,
        nullable=False
    )

    url = Column(
        String,
        nullable=False,
        unique=True
    )

    default_branch = Column(
        String,
        nullable=False,
        default="main"
    )

    status = Column(
        String,
        nullable=False,
        default="active"
    )

    # -------------------------
    # Relaciones
    # -------------------------
    aplications = relationship(
        "Aplication",
        back_populates="repo"
    )
