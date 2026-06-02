

from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.clients.models.database.timestamps import TimestampMixin

from .database import Base

# -------------------------
# Modelo: Client
#
# Representa un cliente del sistema.
# Un cliente puede tener múltiples cuentas
# (AWS, GCP, Azure, on-prem, etc.)
# -------------------------
class Client(Base, TimestampMixin):

    __tablename__ = "clients"

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

    status = Column(
        String,
        nullable=False,
        default="active"
    )

    # -------------------------
    # Relaciones
    # -------------------------
    accounts = relationship(
        "Account",
        back_populates="client",
        cascade="all, delete-orphan"
    )
