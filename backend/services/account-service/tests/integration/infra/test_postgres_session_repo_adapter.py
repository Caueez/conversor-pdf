from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest

from account_service.domain.entities.session import Session
from account_service.infra.repositories.session import PostgresSessionRepoAdapter
from account_service.infra.repositories.user import PostgresUserRepoAdapter
from tests.factories.users import make_user_entity


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_repo_session_flow(
    user_repo: PostgresUserRepoAdapter,
    session_repo: PostgresSessionRepoAdapter,
) -> None:
    user = make_user_entity(email="integration-session@example.com")
    await user_repo.create(user)

    created_at = datetime(2024, 1, 1, tzinfo=UTC)
    expires_at = created_at + timedelta(days=7)
    session = Session(
        user_id=str(user.id),
        token_id="initial-token-id",
        expires_at=expires_at,
        created_at=created_at,
    )

    created = await session_repo.create(session)
    assert created.id == session.id

    fetched = await session_repo.get(UUID(str(session.id)))
    assert fetched is not None
    assert fetched.user_id == str(user.id)
    assert fetched.token_id == "initial-token-id"
    assert fetched.revoked is False

    rotated_expires_at = expires_at + timedelta(days=2)
    await session_repo.rotate(UUID(str(session.id)), "rotated-token-id", rotated_expires_at)

    rotated = await session_repo.get(UUID(str(session.id)))
    assert rotated is not None
    assert rotated.token_id == "rotated-token-id"
    assert rotated.expires_at == rotated_expires_at

    await session_repo.revoke(UUID(str(session.id)))
    revoked = await session_repo.get(UUID(str(session.id)))
    assert revoked is not None
    assert revoked.revoked is True
