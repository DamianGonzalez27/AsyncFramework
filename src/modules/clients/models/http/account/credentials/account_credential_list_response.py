from typing import List
from src.modules.clients.models.http.account.credentials.account_credential_response import (
    AccountCredentialResponse
)
from pydantic import BaseModel

class AccountCredentialListResponse(BaseModel):
    items: List[AccountCredentialResponse]
    total: int
