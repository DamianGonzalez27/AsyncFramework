from uuid import UUID
from typing import List, Tuple

from src.modules.clients.models.database.client import Client
from global_handler.exceptions.http_exceptions import (
    NotFoundHttpError,
    ValidationHttpError,
)
from logger_tracker import logg_debug, logg_info, logg_warning
from src.modules.clients.models.http.client.client_create_request import ClientCreateRequest
from src.modules.clients.repositories.database.client_repository import ClientRepository


class ClientService:

    def __init__(self, repository: ClientRepository):
        self.repository = repository

    # -------------------------
    # CREATE
    # -------------------------
    def create_client(self, data: ClientCreateRequest) -> Client:
        logg_info(
            "ClientService: create_client - start"
        )

        existing = self.repository.get_by_name(data.name)
        if existing:
            logg_warning(
                "Client already exists"
            )
            raise ValidationHttpError(
                message="Client already exists",
                details=data.name
            )

        client = Client(
            name=data.name,
            description=data.description,
            status="active",
        )

        self.repository.create(client)

        logg_info(
            "ClientService: create_client - success"
        )
        logg_debug(
            f"Created client ID: {client.id}"
        )

        return client