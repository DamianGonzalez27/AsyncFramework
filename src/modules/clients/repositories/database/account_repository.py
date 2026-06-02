# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
#
# Este software y su código fuente han sido desarrollados por Erick Damian Gonzalez Aranda, mediante 
# NeuronexoTec Organizacion de desarrollo de Software.
# Todos los derechos están reservados.
#
# Se permite el uso, copia y modificación del código únicamente para fines
# personales, educativos o internos, siempre que se conserve este aviso
# de copyright y no se redistribuya el software, total o parcialmente,
# sin autorización expresa del autor.
#
# Queda estrictamente prohibida la venta, sublicencia, redistribución,
# exposición como servicio (SaaS), o incorporación en productos comerciales
# sin consentimiento previo y por escrito del autor.
#
# Este software se proporciona "tal cual", sin garantía de ningún tipo,
# expresa o implícita, incluyendo pero no limitado a garantías de
# comercialización, idoneidad para un propósito particular o ausencia
# de defectos.
# 
# El autor no será responsable por ningún daño directo o indirecto
# derivado del uso de este software.
# -------------------------
from typing import Optional, List
from sqlalchemy.orm import Session

from src.modules.clients.models.database.account import Account
from src.modules.clients.models.database.account_credential import AccountCredential
from src.modules.clients.models.database.timestamps import TimestampMixin
from global_repository import BaseRepository


class AccountRepository(BaseRepository[Account]):

    def __init__(self, session: Session) -> None:
        super().__init__(Account, session)

    # -------------------------
    # Queries
    # -------------------------
    def get_by_name(self, name: str) -> Optional[Account]:
        return (
            self.session
            .query(Account)
            .filter(Account.name == name)
            .one_or_none()
        )

    def get_active_accounts(self) -> List[Account]:
        return (
            self.session
            .query(Account)
            .filter(Account.is_active.is_(True))
            .all()
        )

    # -------------------------
    # Validations / Checks
    # -------------------------
    def exists(self, account_id) -> bool:
        return (
            self.session
            .query(Account.id)
            .filter(Account.id == account_id)
            .first()
            is not None
        )
