from uuid import UUID
from typing import List, Tuple

from src.modules.clients.models.http.application.application_create_request import (
    ApplicationCreateRequest,
)
from src.modules.clients.models.http.application.application_query_params import (
    ApplicationQueryParams,
)
from src.modules.clients.models.http.application.env_var_create_request import (
    ApplicationEnvVarItem,
)

from src.modules.clients.models.database.application import Aplication
from src.modules.clients.models.database.environment_variables import ApplicationEnvironmentVariable

from src.modules.clients.repositories.database.application_repository import (
    ApplicationRepository,
)
from src.modules.clients.repositories.database.application_env_var_repository import (
    ApplicationEnvironmentVariableRepository,
)

from global_handler.exceptions.http_exceptions import (
    NotFoundHttpError,
    ValidationHttpError,
)

from logger_tracker import logg_info, logg_warning, logg_debug

class ApplicationService:

    def __init__(
        self,
        application_repository: ApplicationRepository,
        env_var_repository: ApplicationEnvironmentVariableRepository,
    ):
        self.application_repository = application_repository
        self.env_var_repository = env_var_repository

    def create_application(
        self,
        data: ApplicationCreateRequest
    ) -> Aplication:

        logg_info(
            "ApplicationService: create_application - start"
        )

        existing = self.application_repository.get_by_name_and_account(
            name=data.name,
            account_id=data.account_id,
        )
        if existing:
            logg_warning(
                "Application already exists"
            )
            raise ValidationHttpError(
                message="Application already exists",
                details=data.name
            )

        application = Aplication(
            name=data.name,
            description=data.description,
            template_uri=data.template_uri,
            type=data.type,
            status=data.status,
            account_id=data.account_id,
            repo_id=data.repo_id,
        )

        self.application_repository.create(application)

        # -------------------------
        # ENV VARS (bulk, opcional)
        # -------------------------
        if data.variables:
            self._create_env_vars_bulk(
                application_id=application.id,
                variables=data.variables
            )

        logg_info(
            "ApplicationService: create_application - success"
        )
        logg_debug(
            f"Created application ID: {application.id}"
        )

        return application


    def search_applications(
        self,
        params: ApplicationQueryParams
    ) -> Tuple[List[Aplication], int]:

        logg_info(
            "ApplicationService: search_applications - start"
        )
        logg_debug(
            f"Search parameters: {params.model_dump()}"
        )

        query = self.application_repository.session.query(Aplication)

        if params.name:
            query = query.filter(
                Aplication.name.ilike(f"%{params.name}%")
            )

        if params.type:
            query = query.filter(
                Aplication.type == params.type
            )

        if params.status:
            query = query.filter(
                Aplication.status == params.status
            )

        total = query.count()

        items = (
            query
            .offset(params.offset)
            .limit(params.size)
            .all()
        )

        logg_info(
            "ApplicationService: search_applications - end"
        )
        logg_debug(
            f"Search results: {{'total': {total}, 'returned': {len(items)}}}"
        )

        return items, total


    def get_application_by_id(
        self,
        application_id: UUID
    ) -> Aplication:

        logg_debug(
            "ApplicationService: get_application_by_id"
        )
        logg_debug(
            f"Fetching application ID: {application_id}"
        )

        application = self.application_repository.get_by_id(
            application_id
        )

        if not application:
            logg_warning(
                "Application not found",
                extra={"application_id": str(application_id)}
            )
            raise NotFoundHttpError(
                message="Application not found",
                details=str(application_id)
            )

        return application

    def update_application(
        self,
        application_id: UUID,
        data: ApplicationCreateRequest
    ) -> Aplication:

        logg_info(
            "ApplicationService: update_application - start"
        )

        application = self.get_application_by_id(application_id)

        if data.name is not None:
            application.name = data.name

        if data.description is not None:
            application.description = data.description

        if data.template_uri is not None:
            application.template_uri = data.template_uri

        if data.type is not None:
            application.type = data.type

        if data.status is not None:
            application.status = data.status

        self.application_repository.update(application)

        logg_info(
            "ApplicationService: update_application - success"
        )
        logg_debug(
            f"Updated application ID: {application.id}"
        )

        return application

    def delete_application(
        self,
        application_id: UUID
    ) -> None:

        logg_info(
            "ApplicationService: delete_application - start"
        )

        application = self.get_application_by_id(application_id)

        application.status = "inactive"
        self.application_repository.update(application)

        logg_info(
            "ApplicationService: delete_application - success"
        )
        logg_debug(
            f"Soft-deleted application ID: {application.id}"
        )

    def _create_env_vars_bulk(
        self,
        application_id: UUID,
        variables: List[ApplicationEnvVarItem]
    ) -> None:

        logg_debug(
            "Creating application env vars (bulk)"
        )

        records = [
            ApplicationEnvironmentVariable(
                application_id=application_id,
                environment_name="test",
                key=item.key,
                value=item.value,  # aquí puedes cifrar después
            )
            for item in variables
        ]

        self.env_var_repository.bulk_create(records)

        logg_debug(
            f"Created {len(records)} env vars for application {application_id}"
        )

    def get_env_vars(
        self,
        application_id: UUID
    ) -> List[ApplicationEnvironmentVariable]:

        logg_debug(
            f"Fetching env vars for application ID: {application_id}"
        )

        env_vars = self.env_var_repository.get_by_application(
            application_id
        )

        logg_debug(
            f"Found {len(env_vars)} env vars for application ID: {application_id}"
        )

        return env_vars
