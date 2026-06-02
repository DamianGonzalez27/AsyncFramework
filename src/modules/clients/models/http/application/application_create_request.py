from typing import Optional
from uuid import UUID
from pydantic import Field
from src.modules.clients.models.http.application.env_var_create_request import ApplicationEnvVarItem
from src.modules.clients.models.http.base_model_request import BaseModelRequest


class ApplicationCreateRequest(BaseModelRequest):

    name: str = Field(min_length=3, max_length=100)
    description: str = Field(default=None, max_length=255)
    template_uri: str = Field(default=None, max_length=255)
    type: str = Field(
        pattern=r"^(api|worker|web|app)$"
    )
    status: str = Field(
        default="active",
        pattern=r"^(active|inactive)$"
    )

    account_id: UUID
    repo_id: UUID

    # variables iniciales (opcional)
    variables: Optional[list[ApplicationEnvVarItem]] | None = None

    __db_exclude__ = {"env_vars"}
