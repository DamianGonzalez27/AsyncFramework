from uuid import UUID
from pydantic import BaseModel, Field


class AccountCredentialCreateRequest(BaseModel):
    account_id: UUID

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nombre lógico de las credenciales"
    )

    access_key_id: str = Field(
        ...,
        min_length=16,
        max_length=128
    )

    secret_access_key: str = Field(
        ...,
        min_length=32,
        max_length=256
    )

    region: str = Field(
        ...,
        example="us-east-1"
    )

    is_default: bool = False
