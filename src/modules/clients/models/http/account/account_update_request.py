
from pydantic import Field, field_validator
from typing import Optional

from src.modules.clients.models.http.base_model_request import BaseModelRequest


class AccountUpdateRequest(BaseModelRequest):
    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9\-_]+$"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=255
    )

    provider: Optional[str] = Field(
        default=None,
        pattern=r"^(aws|gcp|azure|on-prem)$"
    )

    status: Optional[str] = Field(
        default=None,
        pattern=r"^(active|inactive|suspended)$"
    )

    # -------------------------
    # Validators
    # -------------------------
    @field_validator("name")
    def validate_name(cls, v):
        if v and v.strip() != v:
            raise ValueError("name cannot start or end with spaces")
        return v

    @field_validator("provider", "status")
    def normalize_lowercase(cls, v):
        return v.lower() if v else v
