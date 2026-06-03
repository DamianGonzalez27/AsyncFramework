"""Handlers para eventos de clientes en el módulo de usuarios."""

from typing import Any, Dict

from logger_tracker import logg_info, logg_error

from src.modules.clients.models.http.client.client_create_request import ClientCreateRequest
from src.modules.users.services.client_service import ClientService
from src.containers import AppContainer

container = AppContainer()


class ClientHandler:
    """Procesa eventos de clientes usando los servicios del módulo users."""

    @staticmethod
    async def handle_created(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"ClientHandler (users): processing user.client.created - {payload.get('name', 'unknown')}")
        service = ClientService(repository=container.client_repository)
        try:
            data = ClientCreateRequest(**payload)
            client = service.create_client(data)
            logg_info(f"ClientHandler (users): client created - id={client.id}")
        except Exception as e:
            logg_error(f"ClientHandler (users): error creating client - {e}")
            raise
