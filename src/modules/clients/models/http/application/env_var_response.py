from uuid import UUID
from datetime import datetime
from src.modules.clients.models.http.base_response import BaseResponse


class ApplicationEnvVarResponse(BaseResponse):

    id: UUID
    key: str

    # valor NO se devuelve por seguridad
    masked: str = "********"

    created_at: datetime | None = None
