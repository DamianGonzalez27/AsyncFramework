from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class AccountCredentialResponse(BaseModel):
    id: UUID
    account_id: UUID

    provider: str
    name: str
    region: str

    is_default: bool
    status: str

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
