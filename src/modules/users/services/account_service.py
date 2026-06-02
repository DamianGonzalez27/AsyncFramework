from uuid import UUID
from typing import List, Tuple

from src.modules.clients.models.http.account.account_create_request import AccountCreateRequest
from src.modules.clients.models.http.account.account_update_request import AccountUpdateRequest
from src.modules.clients.models.http.account.account_query_params import AccountQueryParams
from src.modules.clients.repositories.database.account_repository import AccountRepository
from src.modules.clients.models.database.account import Account
from global_handler.exceptions.http_exceptions import (
    NotFoundHttpError,
    ValidationHttpError,
)
from logger_tracker import logg_info, logg_warning, logg_debug


class AccountService:

    def __init__(self, repository: AccountRepository):
        self.repository = repository

    # -------------------------
    # CREATE
    # -------------------------
    def create_account(self, data: AccountCreateRequest) -> Account:
        logg_info(
            "AccountService: create_account - start"
        )

        existing = self.repository.get_by_name(data.name)
        if existing:
            logg_warning(
                "Account already exists"
            )
            raise ValidationHttpError(
                message="Account already exists",
                details=data.name
            )

        account = Account(
            name=data.name,
            provider=data.provider,
            description=data.description,
            client_id=data.client_id,
            status="active",
        )

        self.repository.create(account)

        logg_info(
            "AccountService: create_account - success"
        )
        logg_debug(
            f"Created account ID: {account.id}"
        )

        return account

    # -------------------------
    # SEARCH (filters + pagination)
    # -------------------------
    def search_accounts(
        self,
        params: AccountQueryParams
    ) -> Tuple[List[Account], int]:
        extra=params.model_dump()
        logg_info(
            "AccountService: search_accounts - start"
        )
        logg_debug(
            f"Search parameters: {extra}"
        )

        query = self.repository.session.query(Account)

        if params.name:
            query = query.filter(Account.name.ilike(f"%{params.name}%"))

        if params.provider:
            query = query.filter(Account.provider == params.provider)

        if params.status:
            is_active = params.status == "active"
            query = query.filter(Account.is_active.is_(is_active))

        total = query.count()

        items = (
            query
            .offset(params.offset)
            .limit(params.size)
            .all()
        )
        extra={"total": total, "returned": len(items)}
        logg_info(
            "AccountService: search_accounts - end"
        )
        logg_debug(
            f"Search results: {extra}"
        )   

        return items, total

    # -------------------------
    # GET BY ID
    # -------------------------
    def get_account_by_id(self, account_id: UUID) -> Account:
        extra={"account_id": str(account_id)}
        logg_debug(
            "AccountService: get_account_by_id"
        )
        logg_debug(
            f"Fetching account with ID: {extra}"
        )
        account = self.repository.get_by_id(account_id)
        if not account:
            logg_warning(
                "Account not found",
                extra={"account_id": str(account_id)}
            )
            raise NotFoundHttpError(
                message="Account not found",
                details=str(account_id)
            )

        return account

    # -------------------------
    # UPDATE
    # -------------------------
    def update_account(
        self,
        account_id: UUID,
        data: AccountUpdateRequest
    ) -> Account:
        logg_info(
            "AccountService: update_account - start"
        )
        logg_debug(
            f"Updating account with ID: {str(account_id)}"
        )

        account = self.get_account_by_id(account_id)

        if data.name is not None:
            account.name = data.name

        if data.description is not None:
            account.description = data.description

        if data.status is not None:
            account.is_active = data.status == "active"

        self.repository.update(account)

        logg_info(
            "AccountService: update_account - success"
        )
        logg_debug(
            f"Updated account ID: {account.id}"
        )

        return account

    # -------------------------
    # DELETE (soft delete)
    # -------------------------
    def delete_account(self, account_id: UUID) -> None:
        logg_info(
            "AccountService: delete_account - start"
        )
        logg_debug(
            f"Deleting account with ID: {str(account_id)}"
        )

        account = self.get_account_by_id(account_id)

        # soft delete (mucho más sano)
        account.is_active = False
        self.repository.update(account)

        logg_info(
            "AccountService: delete_account - success"
        )
        logg_debug(
            f"Soft-deleted account ID: {account.id}"
        )

