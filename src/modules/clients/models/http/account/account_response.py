from uuid import UUID
from typing import Optional
from pydantic import Field

from src.modules.clients.models.http.base_response import BaseResponse


class AccountResponse(BaseResponse):
    id: UUID = Field(..., description="Account unique identifier")

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Account name"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional account description"
    )

    provider: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Cloud or service provider (aws, gcp, azure, etc)"
    )

    status: str = Field(
        ...,
        pattern=r"^(active|inactive|suspended)$",
        description="Account status"
    )
