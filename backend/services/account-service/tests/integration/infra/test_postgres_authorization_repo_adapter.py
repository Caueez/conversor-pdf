from __future__ import annotations

import pytest

from account_service.domain.entities.permission import PERMISSION_USERS_MANAGE
from account_service.domain.entities.role import ROLE_KEY_ADMIN, ROLE_KEY_USER
from account_service.infra.repositories.authorization import PostgresAuthorizationRepoAdapter


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_authorization_repo_seeds_defaults_and_checks_permissions(db_backend, clean_database) -> None:
    repo = PostgresAuthorizationRepoAdapter(db_backend)

    await repo.ensure_defaults()

    admin_role = await repo.get_role_by_key(ROLE_KEY_ADMIN)
    user_role = await repo.get_role_by_key(ROLE_KEY_USER)
    admin_allowed = await repo.role_has_permission(ROLE_KEY_ADMIN, PERMISSION_USERS_MANAGE)
    user_allowed = await repo.role_has_permission(ROLE_KEY_USER, PERMISSION_USERS_MANAGE)

    assert admin_role is not None
    assert user_role is not None
    assert admin_allowed is True
    assert user_allowed is False
