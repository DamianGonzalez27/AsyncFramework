from typing import List, Tuple
from global_handler.exceptions.http_exceptions import (
    ValidationHttpError,
)
from logger_tracker import logg_info, logg_warning, logg_debug
from src.modules.clients.models.database.repo import Repo
from src.modules.clients.models.http.repo.repo_create_request import RepoCreateRequest
from src.modules.clients.models.http.repo.repo_query_params import RepoQueryParams
from src.modules.clients.repositories.database.repo_repository import RepoRepository


class RepoService:

    def __init__(self, repository: RepoRepository):
        self.repository = repository

    # -------------------------
    # CREATE
    # -------------------------
    def create_repo(self, data: RepoCreateRequest) -> Repo:
        logg_info(
            "RepoService: create_repo - start"
        )

        existing = self.repository.get_by_name(data.name)
        if existing:
            logg_warning(
                "Repo already exists"
            )
            raise ValidationHttpError(
                message="Repo already exists",
                details=data.name
            )

        client = Repo(**data.to_db())

        self.repository.create(client)

        logg_info(
            "RepoService: create_repo - success"
        )
        logg_debug(
            f"Created repo ID: {client.id}"
        )

        return client
    
    # -------------------------
    # SEARCH (filters + pagination)
    # -------------------------
    def search_repos(
        self,
        params: RepoQueryParams
    ) -> Tuple[List[Repo], int]:
        extra=params.model_dump()
        logg_info(
            "RepoService: search_repos - start"
        )
        logg_debug(
            f"Search parameters: {extra}"
        )

        query = self.repository.session.query(Repo)

        if params.name:
            query = query.filter(Repo.name.ilike(f"%{params.name}%"))

        if params.provider:
            query = query.filter(Repo.provider == params.provider)

        total = query.count()

        items = (
            query
            .offset(params.offset)
            .limit(params.size)
            .all()
        )
        extra={"total": total, "returned": len(items)}
        logg_info(
            "AccountService: search_accounts - end"
        )
        logg_debug(
            f"Search results: {extra}"
        )   

        return items, total