from pydantic import BaseModel, Field, field_validator


class BasePaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @field_validator("page", "size")
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError("Pagination values must be greater than zero")
        return v
