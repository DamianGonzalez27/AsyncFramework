from pydantic import Field, field_validator
from typing import Optional

from src.modules.clients.models.http.base_model_request import BaseModelRequest


class ClientCreateRequest(BaseModelRequest):

    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Nombre del cliente"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=255
    )
    # -------------------------
    # Validators
    # -------------------------
    @field_validator("name")
    def validate_name(cls, v: str):
        if v.strip() != v:
            raise ValueError("name cannot start or end with spaces")
        return v
