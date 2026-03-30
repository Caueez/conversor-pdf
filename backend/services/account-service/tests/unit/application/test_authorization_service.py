from __future__ import annotations

from dataclasses import dataclass

import pytest

from account_service.application.services.authorization_service import AuthorizationService
from account_service.domain.entities.role import ROLE_KEY_ADMIN, Role


pytestmark = pytest.mark.unit


@dataclass
class FakeAuthorizationRepo:
    ensured: bool = False

    async def ensure_defaults(self) -> None:
        self.ensured = True

    async def get_role_by_key(self, key: str) -> Role | None:
        if key == ROLE_KEY_ADMIN:
            return Role(key=ROLE_KEY_ADMIN, name="Administrator")
        return None

    async def get_permission_by_key(self, key: str):  # pragma: no cover
        return None

    async def role_has_permission(self, role_key: str, permission_key: str) -> bool:
        return role_key == ROLE_KEY_ADMIN and permission_key == "users:manage"


@pytest.mark.asyncio
async def test_authorization_service_methods_delegate_to_repository() -> None:
    repo = FakeAuthorizationRepo()
    service = AuthorizationService(repo)

    await service.ensure_defaults()
    role = await service.get_role_by_key(ROLE_KEY_ADMIN)
    allowed = await service.has_permission(ROLE_KEY_ADMIN, "users:manage")

    assert repo.ensured is True
    assert role is not None
    assert role.key == ROLE_KEY_ADMIN
    assert allowed is True
