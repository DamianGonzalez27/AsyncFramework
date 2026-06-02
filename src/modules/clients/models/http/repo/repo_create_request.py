from pydantic import Field, field_validator, HttpUrl

from src.modules.clients.models.http.base_model_request import BaseModelRequest

class RepoCreateRequest(BaseModelRequest):

    # -------------------------
    # Properties
    # -------------------------
    name: str = Field(
        min_length=3,
        max_length=50
    )

    provider: str = Field(
        pattern=r"^(github|gitlab|bitbucket)$"
    )

    url: HttpUrl = Field(
        max_length=255
    )

    default_branch: str = Field(
        max_length=50
    )

    # -------------------------
    # Validators
    # -------------------------
    @field_validator("name")
    def validate_name(cls, v: str):
        if v.strip() != v:
            raise ValueError("name cannot start or end with spaces")
        return v
    
    # -------------------------
    # Normalizers
    # -------------------------
    @field_validator("provider")
    def normalize_lowercase(cls, v: str):
        return v.lower()
