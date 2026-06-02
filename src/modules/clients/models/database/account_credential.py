from sqlalchemy import (
    Column,
    DateTime,
    String,
    Text,
    ForeignKey,
    Boolean,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from src.modules.clients.models.database.timestamps import TimestampMixin
from .database import Base

class AccountCredential(Base, TimestampMixin):

    __tablename__ = "account_credentials"

    # -------------------------
    # Identificador único
    # -------------------------
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # -------------------------
    # Relación con Account
    # -------------------------
    account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    account = relationship(
        "Account",
        back_populates="credentials"
    )

    # -------------------------
    # Payload cifrado
    #
    # Ejemplo (ANTES de cifrar):
    # {
    #   "access_key_id": "...",
    #   "secret_access_key": "...",
    #   "region": "us-east-1"
    # }
    # -------------------------
    encrypted_payload = Column(
        Text,
        nullable=False
    )

    # -------------------------
    # Fingerprint seguro (NO reversible)
    #
    # Ejemplo:
    # SHA256(access_key_id + region)
    # -------------------------
    key_fingerprint = Column(
        String(64),
        nullable=False,
        index=True
    )

    # -------------------------
    # Estado de la credencial
    # -------------------------
    status = Column(
        String(20),
        nullable=False,
        default="active",
        index=True
    )

    # -------------------------
    # Flags útiles
    # -------------------------
    is_primary = Column(
        Boolean,
        nullable=False,
        default=False
    )

    # -------------------------
    # Auditoría funcional
    # -------------------------
    created_by = Column(
        String,
        nullable=True
    )

    last_used_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # -------------------------
    # Índices compuestos
    # -------------------------
    __table_args__ = (
        Index(
            "uq_account_provider_fingerprint",
            "account_id",
            "key_fingerprint",
            unique=True
        ),
    )
