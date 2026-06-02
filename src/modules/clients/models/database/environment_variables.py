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
# Modelo: ApplicationEnvironmentVariable
#
# Representa una variable de entorno asociada directamente
# a una aplicación, cuyo valor puede variar según el entorno
# en el que se realice el despliegue.
#
# La consulta de variables se realiza siempre desde la aplicación,
# nunca desde el entorno.
# -------------------------
class ApplicationEnvironmentVariable(Base, TimestampMixin):

    __tablename__ = "application_environment_variables"

    # -------------------------
    # Identificador primario
    # -------------------------
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    # -------------------------
    # Relación con aplicación
    # -------------------------
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("aplications.id"),
        nullable=False
    )

    # -------------------------
    # Contexto del entorno
    # -------------------------
    environment_name = Column(
        String,
        nullable=False,
        index=True
    )

    # -------------------------
    # Variable de entorno
    # -------------------------
    key = Column(
        String,
        nullable=False
    )

    value = Column(
        String,
        nullable=False
    )

    # -------------------------
    # Relación ORM
    # -------------------------
    aplication = relationship(
        "Aplication",
        back_populates="environment_variables"
    )
