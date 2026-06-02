from pydantic import BaseModel, Field
from typing import Optional


class AccountCredentialUpdateRequest(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100
    )

    access_key_id: Optional[str] = Field(
        None,
        min_length=16,
        max_length=128
    )

    secret_access_key: Optional[str] = Field(
        None,
        min_length=32,
        max_length=256
    )

    region: Optional[str] = None

    is_default: Optional[bool] = None

    status: Optional[str] = Field(
        None,
        description="active | inactive"
    )
