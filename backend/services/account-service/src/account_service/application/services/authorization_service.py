from __future__ import annotations

from account_service.application.interfaces.repository import AuthorizationRepositoryPort
from account_service.domain.entities.role import Role


class AuthorizationService:
    def __init__(self, repository: AuthorizationRepositoryPort) -> None:
        self._repository = repository

    async def ensure_defaults(self) -> None:
        await self._repository.ensure_defaults()

    async def get_role_by_key(self, role_key: str) -> Role | None:
        return await self._repository.get_role_by_key(role_key)

    async def has_permission(self, role_key: str, permission_key: str) -> bool:
        return await self._repository.role_has_permission(role_key, permission_key)
