
from pydantic import Field, field_validator
from typing import Optional

from src.modules.clients.models.http.base_pagination_params import BasePaginationParams

class AccountQueryParams(BasePaginationParams):

    name: Optional[str] = Field(
        default=None, 
        min_length=3, 
        max_length=50
    )

    provider: Optional[str] = Field(
        default=None,
        pattern=r"^(aws|gcp|azure|on-prem)$"
    )

    status: Optional[str] = Field(
        default=None,
        pattern=r"^(active|inactive|suspended)$"
    )

    @field_validator("provider", "status")
    def normalize_lowercase(cls, v):
        return v.lower() if v else v
