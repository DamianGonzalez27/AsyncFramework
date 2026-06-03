"""Handlers para eventos del dominio de cuentas."""

from typing import Any, Dict

from logger_tracker import logg_info, logg_error

from src.modules.clients.models.http.account.account_create_request import AccountCreateRequest
from src.modules.users.services.account_service import AccountService
from src.containers import AppContainer

container = AppContainer()


class AccountHandler:
    """Procesa eventos relacionados con cuentas de infraestructura."""

    @staticmethod
    async def handle_created(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"AccountHandler: processing account.created - {payload.get('name', 'unknown')}")
        service = AccountService(repository=container.account_repository)
        try:
            data = AccountCreateRequest(**payload)
            account = service.create_account(data)
            logg_info(f"AccountHandler: account created - id={account.id}")
        except Exception as e:
            logg_error(f"AccountHandler: error creating account - {e}")
            raise

    @staticmethod
    async def handle_updated(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"AccountHandler: processing account.updated - {payload.get('id', 'unknown')}")

    @staticmethod
    async def handle_deleted(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"AccountHandler: processing account.deleted - {payload.get('id', 'unknown')}")
