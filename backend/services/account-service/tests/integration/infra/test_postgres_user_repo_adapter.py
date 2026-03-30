from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest
from asyncpg import UniqueViolationError

from account_service.domain.entities.role import ROLE_KEY_ADMIN, ROLE_KEY_USER
from account_service.infra.repositories.user import PostgresUserRepoAdapter
from tests.factories.users import make_unique_email, make_user_entity


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_repo_crud_flow(user_repo: PostgresUserRepoAdapter) -> None:
    created_at = datetime(2024, 1, 1, tzinfo=UTC)
    updated_at = datetime(2024, 1, 1, tzinfo=UTC)
    user = make_user_entity(
        name="Integration User",
        email=make_unique_email("integration"),
        created_at=created_at,
        updated_at=updated_at,
    )

    await user_repo.create(user)

    fetched = await user_repo.get(UUID(str(user.id)))
    assert fetched is not None
    assert fetched.name == "Integration User"
    assert fetched.email == user.email
    assert fetched.role == ROLE_KEY_USER
    assert isinstance(fetched.created_at, datetime)
    assert isinstance(fetched.updated_at, datetime)

    by_email = await user_repo.get_by_email(user.email)
    assert by_email is not None
    assert str(by_email.id) == str(user.id)

    listed = await user_repo.list()
    assert len(listed) == 1

    updated = make_user_entity(
        user_id=str(user.id),
        name="Integration User Updated",
        email=user.email,
        password_hash="hashed::updated",
        role=ROLE_KEY_ADMIN,
        created_at=created_at,
        updated_at=datetime(2024, 1, 2, tzinfo=UTC),
    )
    await user_repo.update(updated)

    persisted = await user_repo.get(UUID(str(user.id)))
    assert persisted is not None
    assert persisted.name == "Integration User Updated"
    assert persisted.password_hash == "hashed::updated"
    assert persisted.role == ROLE_KEY_ADMIN

    await user_repo.delete(UUID(str(user.id)))
    deleted = await user_repo.get(UUID(str(user.id)))
    assert deleted is None


async def test_repo_enforces_unique_email_constraint(user_repo: PostgresUserRepoAdapter) -> None:
    duplicate_email = make_unique_email("duplicate")
    user_a = make_user_entity(email=duplicate_email)
    user_b = make_user_entity(email=duplicate_email)

    await user_repo.create(user_a)

    with pytest.raises(UniqueViolationError):
        await user_repo.create(user_b)
