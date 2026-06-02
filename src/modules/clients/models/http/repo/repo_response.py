from uuid import UUID
from typing import Optional
from pydantic import Field

from src.modules.clients.models.http.base_response import BaseResponse


class RepoResponse(BaseResponse):
    id: UUID = Field(..., description="Repo unique identifier")

    name: Optional[str] = Field(
        max_length=250,
        description="Repo name"
    )

    name: Optional[str] = Field(
        max_length=250,
        description="Cloud or service provider (aws, gcp, azure, etc)"
    )
