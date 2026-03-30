from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest

from account_service.domain.entities.user import User
from account_service.domain.entities.role import ROLE_KEY_USER


pytestmark = pytest.mark.unit


def test_user_to_dict_excludes_password_hash_and_serializes_dates() -> None:
    created_at = datetime(2024, 1, 1, 12, 0, tzinfo=UTC)
    updated_at = datetime(2024, 1, 2, 12, 0, tzinfo=UTC)
    user = User(
        name="User Name",
        email="user@example.com",
        password_hash="hashed",
        created_at=created_at,
        updated_at=updated_at,
    )

    payload = user.to_dict()
    assert "password_hash" not in payload
    assert payload["id"] == user.id
    assert payload["name"] == "User Name"
    assert payload["email"] == "user@example.com"
    assert payload["is_active"] is True
    assert payload["created_at"] == created_at.isoformat()
    assert payload["updated_at"] == updated_at.isoformat()


def test_user_defaults_generate_uuid_and_timestamps() -> None:
    user = User(name="User Name", email="user@example.com", password_hash="hashed")

    UUID(user.id)
    assert user.role == ROLE_KEY_USER
    assert user.is_active is True
    assert user.created_at.tzinfo is UTC
    assert user.updated_at.tzinfo is UTC
