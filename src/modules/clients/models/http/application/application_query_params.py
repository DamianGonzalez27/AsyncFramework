from typing import Optional
from pydantic import Field
from src.modules.clients.models.http.base_pagination_params import BasePaginationParams


class ApplicationQueryParams(BasePaginationParams):

    name: Optional[str] | None = None
    type: Optional[str] | None = None
    status: Optional[str] | None = None

    # page: int = Field(default=1, ge=1)
    # size: int = Field(default=20, ge=1, le=100)

    # @property
    # def offset(self) -> int:
    #     return (self.page - 1) * self.size
