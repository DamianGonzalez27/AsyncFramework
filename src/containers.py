from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.modules.clients.repositories.database.account_repository import AccountRepository
from src.modules.clients.repositories.database.application_env_var_repository import ApplicationEnvironmentVariableRepository
from src.modules.clients.repositories.database.application_repository import ApplicationRepository
from src.modules.clients.repositories.database.client_repository import ClientRepository
from src.modules.clients.repositories.database.repo_repository import RepoRepository
from src.modules.users.services.application_service import ApplicationService
from src.modules.users.services.client_service import ClientService
from src.modules.users.services.deployment_service import DeploymentService
from src.modules.clients.repositories.aws_repository import AwsRepository
from src.modules.users.services.account_service import AccountService
from src.modules.users.services.repo_service import RepoService
from src.utils import get_database_url
from src.modules.clients.models.database import *

class AppContainer:
    """
    Contenedor de dependencias de la aplicación.
    Aquí se crean las instancias de repositorios y servicios.
    """
    def __init__(self):
        # -------------------------
        # Database
        # -------------------------
        self.engine = create_engine(
            get_database_url(),
            pool_pre_ping=True,
        )

        self.session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
            )
        )

        # -------------------------
        # Repositories
        # -------------------------
        self.account_repository = AccountRepository(
            session=self.session_factory()
        )

        self.client_repository = ClientRepository(
            session=self.session_factory()
        )

        self.repo_repository = RepoRepository(
            session=self.session_factory()
        )
        self.application_repository = ApplicationRepository(
            session=self.session_factory()
        )
        self.application_env_var_repository = ApplicationEnvironmentVariableRepository(
            session=self.session_factory()
        )

        self.aws_repository = AwsRepository()

        # -------------------------
        # Services
        # -------------------------
        self.account_service = AccountService(
            repository=self.account_repository
        )

        self.client_service = ClientService(
            repository=self.client_repository
        )

        self.deployment_service = DeploymentService(
            aws_repository=self.aws_repository
        )

        self.repo_service = RepoService(
            repository=self.repo_repository
        )

        self.application_service = ApplicationService(
            application_repository=self.application_repository,
            env_var_repository=self.application_env_var_repository
        )
