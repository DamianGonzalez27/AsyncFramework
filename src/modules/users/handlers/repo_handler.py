"""Handlers para eventos del dominio de repositorios."""

from typing import Any, Dict

from logger_tracker import logg_info, logg_error

from src.modules.clients.models.http.repo.repo_create_request import RepoCreateRequest
from src.modules.users.services.repo_service import RepoService
from src.containers import AppContainer

container = AppContainer()


class RepoHandler:
    """Procesa eventos relacionados con repositorios de código."""

    @staticmethod
    async def handle_created(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"RepoHandler: processing repo.created - {payload.get('name', 'unknown')}")
        service = RepoService(repository=container.repo_repository)
        try:
            data = RepoCreateRequest(**payload)
            repo = service.create_repo(data)
            logg_info(f"RepoHandler: repo created - id={repo.id}")
        except Exception as e:
            logg_error(f"RepoHandler: error creating repo - {e}")
            raise
