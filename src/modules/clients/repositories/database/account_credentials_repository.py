from typing import List, Tuple, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select, func

from src.modules.clients.models.database.account import Account
from src.modules.clients.models.http.account.account_query_params import AccountQueryParams
from src.modules.clients.models.http.account.account_create_request import AccountCreateRequest
from src.modules.clients.models.http.account.account_update_request import AccountUpdateRequest

from global_repository import BaseRepository

class AccountRepository:

    def __init__(self, session: Session):
        self.session = session

    # -------------------------
    # CREATE
    # -------------------------
    def create(self, data: AccountCreateRequest) -> Account:
        account = Account(**data.model_dump())
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return account

    # -------------------------
    # GET BY ID
    # -------------------------
    def get_by_id(self, account_id: UUID) -> Optional[Account]:
        return self.session.get(Account, account_id)

    # -------------------------
    # UPDATE
    # -------------------------
    def update(
        self,
        account: Account,
        data: AccountUpdateRequest
    ) -> Account:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(account, field, value)

        self.session.commit()
        self.session.refresh(account)
        return account

    # -------------------------
    # DELETE
    # -------------------------
    def delete(self, account: Account) -> None:
        self.session.delete(account)
        self.session.commit()

    # -------------------------
    # SEARCH / LIST
    # -------------------------
    def search(
        self,
        params: AccountQueryParams
    ) -> Tuple[List[Account], int]:

        stmt = select(Account)
        count_stmt = select(func.count(Account.id))

        # -------- Filters --------
        if params.name:
            stmt = stmt.where(Account.name.ilike(f"%{params.name}%"))
            count_stmt = count_stmt.where(Account.name.ilike(f"%{params.name}%"))

        if params.is_active is not None:
            stmt = stmt.where(Account.is_active == params.is_active)
            count_stmt = count_stmt.where(Account.is_active == params.is_active)

        # -------- Pagination --------
        stmt = stmt.offset(params.offset).limit(params.limit)

        items = self.session.execute(stmt).scalars().all()
        total = self.session.execute(count_stmt).scalar_one()

        return items, total
