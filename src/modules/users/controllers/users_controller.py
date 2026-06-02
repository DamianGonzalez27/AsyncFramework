from uuid import UUID

from global_handler.controllers.base_controller import BaseController
from global_handler.decorators.request_decorators import validate_with, validate_query_with

from src.modules.users.controllers import api_blueprint
from src.modules.clients.models.http.account.account_create_request import AccountCreateRequest
from src.modules.clients.models.http.account.account_update_request import AccountUpdateRequest
from src.modules.clients.models.http.account.account_query_params import AccountQueryParams
from src.modules.clients.models.http.client.client_create_request import ClientCreateRequest
from src.modules.clients.models.http.repo.repo_create_request import RepoCreateRequest
from src.modules.clients.models.http.repo.repo_query_params import RepoQueryParams
from src.modules.clients.models.http.application.application_create_request import ApplicationCreateRequest
from src.modules.clients.models.http.application.application_query_params import ApplicationQueryParams
from src.modules.clients.repositories.database.account_repository import AccountRepository
from src.modules.clients.repositories.database.client_repository import ClientRepository
from src.modules.clients.repositories.database.repo_repository import RepoRepository
from src.modules.clients.repositories.database.application_repository import ApplicationRepository
from src.modules.clients.repositories.database.application_env_var_repository import ApplicationEnvironmentVariableRepository
from src.modules.users.services.account_service import AccountService
from src.modules.users.services.client_service import ClientService
from src.modules.users.services.repo_service import RepoService
from src.modules.users.services.application_service import ApplicationService
from src.containers import AppContainer

base_controller = BaseController()
container = AppContainer()


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------
@api_blueprint.route("/health", methods=["GET"])
def health_check():
    return base_controller.success(
        message="Users module healthy",
        data={"module": "users", "status": "healthy"},
    )


# ---------------------------------------------------------------------------
# Accounts CRUD
# ---------------------------------------------------------------------------
@api_blueprint.route("/accounts", methods=["POST"])
@validate_with(AccountCreateRequest)
def create_account(validated_data: AccountCreateRequest):
    account_service = AccountService(repository=container.account_repository)
    account = account_service.create_account(validated_data)
    return base_controller.success(
        message="Account created",
        data={"id": str(account.id), "name": account.name},
        status_code=201,
    )


@api_blueprint.route("/accounts", methods=["GET"])
@validate_query_with(AccountQueryParams)
def list_accounts(query_params: AccountQueryParams):
    account_service = AccountService(repository=container.account_repository)
    items, total = account_service.search_accounts(query_params)
    return base_controller.success(
        message="Accounts retrieved",
        data={
            "items": [{"id": str(a.id), "name": a.name, "provider": a.provider} for a in items],
            "total": total,
        },
    )


@api_blueprint.route("/accounts/<account_id>", methods=["GET"])
def get_account(account_id: UUID):
    account_service = AccountService(repository=container.account_repository)
    account = account_service.get_account_by_id(account_id)
    return base_controller.success(
        message="Account retrieved",
        data={"id": str(account.id), "name": account.name, "provider": account.provider},
    )


@api_blueprint.route("/accounts/<account_id>", methods=["PATCH"])
@validate_with(AccountUpdateRequest)
def update_account(account_id: UUID, validated_data: AccountUpdateRequest):
    account_service = AccountService(repository=container.account_repository)
    account = account_service.update_account(account_id, validated_data)
    return base_controller.success(
        message="Account updated",
        data={"id": str(account.id), "name": account.name},
    )


@api_blueprint.route("/accounts/<account_id>", methods=["DELETE"])
def delete_account(account_id: UUID):
    account_service = AccountService(repository=container.account_repository)
    account_service.delete_account(account_id)
    return base_controller.success(message="Account deleted")


# ---------------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------------
@api_blueprint.route("/clients", methods=["POST"])
@validate_with(ClientCreateRequest)
def create_client(validated_data: ClientCreateRequest):
    client_service = ClientService(repository=container.client_repository)
    client = client_service.create_client(validated_data)
    return base_controller.success(
        message="Client created",
        data={"id": str(client.id), "name": client.name},
        status_code=201,
    )


# ---------------------------------------------------------------------------
# Repos
# ---------------------------------------------------------------------------
@api_blueprint.route("/repos", methods=["POST"])
@validate_with(RepoCreateRequest)
def create_repo(validated_data: RepoCreateRequest):
    repo_service = RepoService(repository=container.repo_repository)
    repo = repo_service.create_repo(validated_data)
    return base_controller.success(
        message="Repo created",
        data={"id": str(repo.id), "name": repo.name},
        status_code=201,
    )


@api_blueprint.route("/repos", methods=["GET"])
@validate_query_with(RepoQueryParams)
def list_repos(query_params: RepoQueryParams):
    repo_service = RepoService(repository=container.repo_repository)
    items, total = repo_service.search_repos(query_params)
    return base_controller.success(
        message="Repos retrieved",
        data={
            "items": [{"id": str(r.id), "name": r.name, "provider": r.provider} for r in items],
            "total": total,
        },
    )


# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
@api_blueprint.route("/applications", methods=["POST"])
@validate_with(ApplicationCreateRequest)
def create_application(validated_data: ApplicationCreateRequest):
    app_service = ApplicationService(
        application_repository=container.application_repository,
        env_var_repository=container.application_env_var_repository,
    )
    application = app_service.create_application(validated_data)
    return base_controller.success(
        message="Application created",
        data={"id": str(application.id), "name": application.name},
        status_code=201,
    )


@api_blueprint.route("/applications", methods=["GET"])
@validate_query_with(ApplicationQueryParams)
def list_applications(query_params: ApplicationQueryParams):
    app_service = ApplicationService(
        application_repository=container.application_repository,
        env_var_repository=container.application_env_var_repository,
    )
    items, total = app_service.search_applications(query_params)
    return base_controller.success(
        message="Applications retrieved",
        data={
            "items": [{"id": str(a.id), "name": a.name, "type": a.type} for a in items],
            "total": total,
        },
    )


@api_blueprint.route("/applications/<application_id>", methods=["GET"])
def get_application(application_id: UUID):
    app_service = ApplicationService(
        application_repository=container.application_repository,
        env_var_repository=container.application_env_var_repository,
    )
    application = app_service.get_application_by_id(application_id)
    return base_controller.success(
        message="Application retrieved",
        data={"id": str(application.id), "name": application.name},
    )


@api_blueprint.route("/applications/<application_id>", methods=["DELETE"])
def delete_application(application_id: UUID):
    app_service = ApplicationService(
        application_repository=container.application_repository,
        env_var_repository=container.application_env_var_repository,
    )
    app_service.delete_application(application_id)
    return base_controller.success(message="Application deleted")
