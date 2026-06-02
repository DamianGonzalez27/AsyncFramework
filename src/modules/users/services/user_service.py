"""Servicio base del módulo de usuarios."""

from typing import Dict, Any, Optional


class UserService:
    def __init__(self, repository: Optional[Any] = None):
        self.repository = repository

    def create_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        user = {
            "id": payload.get("id", "user-0001"),
            "username": payload.get("username", "default-user"),
            "email": payload.get("email", "user@example.com"),
        }
        if self.repository is not None:
            self.repository.save(user)
        return user
