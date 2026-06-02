from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from global_repository import BaseRepository
from src.modules.clients.models.database.environment_variables import (
    ApplicationEnvironmentVariable
)


class ApplicationEnvironmentVariableRepository(
    BaseRepository[ApplicationEnvironmentVariable]
):

    def __init__(self, session: Session) -> None:
        super().__init__(ApplicationEnvironmentVariable, session)

    # -------------------------
    # Queries
    # -------------------------
    def get_by_application(
        self,
        application_id: UUID
    ) -> List[ApplicationEnvironmentVariable]:
        return (
            self.session
            .query(ApplicationEnvironmentVariable)
            .filter(
                ApplicationEnvironmentVariable.application_id
                == application_id
            )
            .all()
        )

    def get_by_key(
        self,
        application_id: UUID,
        key: str
    ) -> Optional[ApplicationEnvironmentVariable]:
        return (
            self.session
            .query(ApplicationEnvironmentVariable)
            .filter(
                ApplicationEnvironmentVariable.application_id
                == application_id,
                ApplicationEnvironmentVariable.key == key
            )
            .one_or_none()
        )

    # -------------------------
    # Bulk operations
    # -------------------------
    def create_many(
        self,
        variables: List[ApplicationEnvironmentVariable]
    ) -> List[ApplicationEnvironmentVariable]:
        self.session.add_all(variables)
        self.session.commit()
        for var in variables:
            self.session.refresh(var)
        return variables
    
    def bulk_create(
        self,
        variables: List[ApplicationEnvironmentVariable]
    ) -> List[ApplicationEnvironmentVariable]:
        """
        Inserción masiva de variables de entorno.
        Operación atómica.
        """
        if not variables:
            return []

        self.session.add_all(variables)
        self.session.commit()

        for var in variables:
            self.session.refresh(var)

        return variables

    # -------------------------
    # Delete helpers
    # -------------------------
    def delete_by_application(
        self,
        application_id: UUID
    ) -> None:
        (
            self.session
            .query(ApplicationEnvironmentVariable)
            .filter(
                ApplicationEnvironmentVariable.application_id
                == application_id
            )
            .delete()
        )
        self.session.commit()
