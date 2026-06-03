"""Handlers para eventos del dominio de clientes."""

from typing import Any, Dict

from logger_tracker import logg_info, logg_error

from src.modules.clients.services.client_service import ClientService


class ClientHandler:
    """Procesa eventos relacionados con clientes."""

    @staticmethod
    async def handle_created(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"ClientHandler: processing client.created - {payload.get('name', 'unknown')}")
        service = ClientService()
        try:
            result = service.create_client(payload)
            logg_info(f"ClientHandler: client created successfully - id={result.get('id')}")
        except Exception as e:
            logg_error(f"ClientHandler: error creating client - {e}")
            raise

    @staticmethod
    async def handle_updated(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"ClientHandler: processing client.updated - {payload.get('id', 'unknown')}")
