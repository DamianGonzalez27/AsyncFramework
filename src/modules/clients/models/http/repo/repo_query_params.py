
from pydantic import Field, field_validator
from typing import Optional

from src.modules.clients.models.http.base_pagination_params import BasePaginationParams

class RepoQueryParams(BasePaginationParams):

    name: Optional[str] = Field(
        default=None, 
        min_length=3, 
        max_length=50
    )

    provider: Optional[str] = Field(
        default=None,
        pattern=r"^(github|gitlab|bitbucket)$"
    )

    @field_validator("provider")
    def normalize_lowercase(cls, v):
        return v.lower() if v else v
