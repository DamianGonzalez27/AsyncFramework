"""Handlers para eventos del dominio de aplicaciones."""

from typing import Any, Dict

from logger_tracker import logg_info, logg_error

from src.modules.clients.models.http.application.application_create_request import ApplicationCreateRequest
from src.modules.users.services.application_service import ApplicationService
from src.containers import AppContainer

container = AppContainer()


class ApplicationHandler:
    """Procesa eventos relacionados con aplicaciones."""

    @staticmethod
    async def handle_created(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"ApplicationHandler: processing application.created - {payload.get('name', 'unknown')}")
        service = ApplicationService(
            application_repository=container.application_repository,
            env_var_repository=container.application_env_var_repository,
        )
        try:
            data = ApplicationCreateRequest(**payload)
            app = service.create_application(data)
            logg_info(f"ApplicationHandler: application created - id={app.id}")
        except Exception as e:
            logg_error(f"ApplicationHandler: error creating application - {e}")
            raise

    @staticmethod
    async def handle_deleted(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"ApplicationHandler: processing application.deleted - {payload.get('id', 'unknown')}")
