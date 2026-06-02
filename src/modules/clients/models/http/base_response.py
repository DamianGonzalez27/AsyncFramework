from pydantic import BaseModel
from uuid import UUID


class BaseResponse(BaseModel):
    id: UUID

    model_config = {
        "from_attributes": True
    }
