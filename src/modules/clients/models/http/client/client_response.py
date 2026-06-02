from uuid import UUID
from typing import Optional
from pydantic import Field

from src.modules.clients.models.http.base_response import BaseResponse


class ClientResponse(BaseResponse):
    id: UUID = Field(..., description="Client unique identifier")

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Client name"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional client description"
    )

    status: str = Field(
        ...,
        pattern=r"^(active|inactive|suspended)$",
        description="Client status"
    )
