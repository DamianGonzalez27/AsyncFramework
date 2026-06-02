from uuid import UUID
from typing import List

from src.modules.clients.models.database.account_credential import AccountCredential
from src.modules.clients.models.http.account.credentials.account_credentials_create_request import (
    AccountCredentialCreateRequest,
)
from src.modules.clients.models.http.account.credentials.account_credential_update_request import (
    AccountCredentialUpdateRequest,
)

from src.modules.clients.repositories.database.account_credentials_repository import (
    AccountCredentialRepository,
)
from src.modules.clients.repositories.database.account_repository import AccountRepository

from src.exceptions.http_exceptions import (
    NotFoundHttpError,
    ValidationHttpError,
)

from logger_tracker import logg_info, logg_warning, logg_debug, logg_error


class AccountCredentialService:

    def __init__(
        self,
        credential_repository: AccountCredentialRepository,
        account_repository: AccountRepository,
    ):
        self.credential_repository = credential_repository
        self.account_repository = account_repository

    # -------------------------
    # CREATE
    # -------------------------
    def create_credential(
        self,
        data: AccountCredentialCreateRequest
    ) -> AccountCredential:

        logg_info(
            "AccountCredentialService: create_credential - start"
        )

        # validar que la cuenta exista
        if not self.account_repository.exists(data.account_id):
            logg_warning(
                "Account not found for credential creation"
            )
            raise NotFoundHttpError(
                message="Account not found",
                details=str(data.account_id)
            )

        # evitar duplicados por tipo/proveedor
        existing = self.credential_repository.get_by_account_and_type(
            account_id=data.account_id,
            credential_type=data.credential_type
        )
        if existing:
            logg_warning(
                "Credential already exists for this account and type"
            )
            raise ValidationHttpError(
                message="Credential already exists",
                details=data.credential_type
            )

        credential = AccountCredential(
            account_id=data.account_id,
            credential_type=data.credential_type,
            access_key_id=data.access_key_id,
            secret_access_key=data.secret_access_key,
            region=data.region,
            metadata=data.metadata,
            status="active",
        )

        self.credential_repository.create(credential)

        logg_info(
            "AccountCredentialService: create_credential - success"
        )
        logg_debug(
            f"Created credential ID: {credential.id}"
        )

        return credential

    # -------------------------
    # GET BY ACCOUNT
    # -------------------------
    def get_credentials_by_account(
        self,
        account_id: UUID
    ) -> List[AccountCredential]:

        logg_debug(
            "AccountCredentialService: get_credentials_by_account"
        )

        if not self.account_repository.exists(account_id):
            raise NotFoundHttpError(
                message="Account not found",
                details=str(account_id)
            )

        return self.credential_repository.get_by_account(account_id)

    # -------------------------
    # GET BY ID
    # -------------------------
    def get_credential_by_id(
        self,
        credential_id: UUID
    ) -> AccountCredential:

        credential = self.credential_repository.get_by_id(
            credential_id
        )

        if not credential:
            logg_warning(
                "Credential not found"
            )
            raise NotFoundHttpError(
                message="Credential not found",
                details=str(credential_id)
            )

        return credential

    # -------------------------
    # UPDATE
    # -------------------------
    def update_credential(
        self,
        credential_id: UUID,
        data: AccountCredentialUpdateRequest
    ) -> AccountCredential:

        logg_info(
            "AccountCredentialService: update_credential - start"
        )

        credential = self.get_credential_by_id(credential_id)

        if data.access_key_id is not None:
            credential.access_key_id = data.access_key_id

        if data.secret_access_key is not None:
            credential.secret_access_key = data.secret_access_key

        if data.region is not None:
            credential.region = data.region

        if data.metadata is not None:
            credential.metadata = data.metadata

        if data.status is not None:
            credential.status = data.status

        self.credential_repository.update(credential)

        logg_info(
            "AccountCredentialService: update_credential - success"
        )
        logg_debug(
            f"Updated credential ID: {credential.id}"
        )

        return credential

    # -------------------------
    # DELETE (soft delete)
    # -------------------------
    def delete_credential(
        self,
        credential_id: UUID
    ) -> None:

        logg_info(
            "AccountCredentialService: delete_credential - start"
        )

        credential = self.get_credential_by_id(credential_id)

        credential.status = "inactive"
        credential.deleted_at = None  # si luego automatizas soft-delete por timestamp

        self.credential_repository.update(credential)

        logg_info(
            "AccountCredentialService: delete_credential - success"
        )
        logg_debug(
            f"Soft-deleted credential ID: {credential.id}"
        )
