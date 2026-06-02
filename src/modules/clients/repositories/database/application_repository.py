from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.modules.clients.models.database.application import Aplication
from global_repository import BaseRepository


class ApplicationRepository(BaseRepository[Aplication]):

    def __init__(self, session: Session) -> None:
        super().__init__(Aplication, session)

    # -------------------------
    # Queries
    # -------------------------
    def get_by_name(
        self,
        account_id: UUID,
        name: str
    ) -> Optional[Aplication]:
        return (
            self.session
            .query(Aplication)
            .filter(
                Aplication.account_id == account_id,
                Aplication.name == name
            )
            .one_or_none()
        )

    def get_by_name_and_account(
        self,
        name: str,
        account_id: UUID
    ) -> Optional[Aplication]:
        """
        Valida unicidad de aplicación por cuenta.
        Usado en CREATE.
        """
        return (
            self.session
            .query(Aplication)
            .filter(
                Aplication.account_id == account_id,
                Aplication.name == name
            )
            .one_or_none()
        )

    def get_by_repo_id(
        self,
        repo_id: UUID
    ) -> List[Aplication]:
        return (
            self.session
            .query(Aplication)
            .filter(Aplication.repo_id == repo_id)
            .all()
        )

    def get_active_by_account(
        self,
        account_id: UUID
    ) -> List[Aplication]:
        return (
            self.session
            .query(Aplication)
            .filter(
                Aplication.account_id == account_id,
                Aplication.status == "active"
            )
            .all()
        )

    # -------------------------
    # Validations / Checks
    # -------------------------
    def exists(self, application_id: UUID) -> bool:
        return (
            self.session
            .query(Aplication.id)
            .filter(Aplication.id == application_id)
            .first()
            is not None
        )
