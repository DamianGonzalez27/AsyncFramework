"""Servicio base para el módulo de clientes."""

from typing import Optional, Dict, Any


class ClientService:
    """Servicio de dominio para operaciones sobre clientes."""

    def __init__(self, repository: Optional[Any] = None):
        self.repository = repository

    def create_client(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        client = {
            "id": payload.get("id", "client-0001"),
            "name": payload.get("name", "default-client"),
            "metadata": payload.get("metadata", {}),
        }
        if self.repository is not None:
            self.repository.save(client)
        return client
