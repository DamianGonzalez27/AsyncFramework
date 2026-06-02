from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class BaseListResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int

    @classmethod
    def from_items(cls, items: List[T]):
        return cls(
            items=items,
            total=len(items)
        )
