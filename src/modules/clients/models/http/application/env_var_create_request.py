from pydantic import Field
from src.modules.clients.models.http.base_model_request import BaseModelRequest


class ApplicationEnvVarItem(BaseModelRequest):

    key: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[A-Z_][A-Z0-9_]*$"
    )
    value: str = Field(min_length=0, max_length=4096)


class ApplicationEnvVarCreateRequest(BaseModelRequest):

    variables: list[ApplicationEnvVarItem]
