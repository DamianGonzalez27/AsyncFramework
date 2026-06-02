from uuid import UUID
from datetime import datetime
from pydantic import Field
from src.modules.clients.models.http.base_response import BaseResponse


class ApplicationResponse(BaseResponse):

    id: UUID
    name: str
    description: str | None
    template_uri: str | None
    type: str
    status: str

    account_id: UUID
    repo_id: UUID

    created_at: datetime | None = None
    updated_at: datetime | None = None
