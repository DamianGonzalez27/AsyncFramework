from pydantic import Field, field_validator
from typing import Optional
from uuid import UUID

from src.modules.clients.models.http.base_model_request import BaseModelRequest


class AccountCreateRequest(BaseModelRequest):
    # -------------------------
    # Parametros normales
    # -------------------------
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9\-_]+$",
        description="Unique account name"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=255
    )

    provider: str = Field(
        ...,
        pattern=r"^(aws|gcp|azure|on-prem)$",
        description="Infrastructure provider"
    )

    status: str = Field(
        default="active",
        pattern=r"^(active|inactive|suspended)$"
    )
    
    # -------------------------
    # Relaciones
    # -------------------------
    client_id: UUID = Field(
        ...,
        description="Client identifier that owns the account"
    )

    # -------------------------
    # Validators
    # -------------------------
    @field_validator("name")
    def validate_name(cls, v: str):
        if v.strip() != v:
            raise ValueError("name cannot start or end with spaces")
        return v

    @field_validator("provider", "status")
    def normalize_lowercase(cls, v: str):
        return v.lower()
