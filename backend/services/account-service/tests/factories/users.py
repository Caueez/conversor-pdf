from __future__ import annotations

from datetime import UTC, datetime
from itertools import count
from uuid import uuid4

from account_service.domain.entities.user import User
from account_service.domain.entities.role import ROLE_KEY_USER


_EMAIL_COUNTER = count(1)
FIXED_TIMESTAMP = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)


def make_unique_email(prefix: str = "user") -> str:
    return f"{prefix}-{next(_EMAIL_COUNTER)}@example.com"


def make_create_user_payload(
    *,
    name: str = "Test User",
    email: str | None = None,
    password: str = "password-123",
) -> dict[str, str]:
    return {
        "name": name,
        "email": email or make_unique_email(),
        "password": password,
    }


def make_update_user_payload(
    *,
    name: str | None = None,
    email: str | None = None,
    password: str | None = None,
) -> dict[str, str]:
    payload: dict[str, str] = {}
    if name is not None:
        payload["name"] = name
    if email is not None:
        payload["email"] = email
    if password is not None:
        payload["password"] = password
    return payload


def make_user_entity(
    *,
    name: str = "Test User",
    email: str | None = None,
    password_hash: str = "hashed-password",
    role: str = ROLE_KEY_USER,
    user_id: str | None = None,
    is_active: bool = True,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
) -> User:
    return User(
        id=user_id or str(uuid4()),
        name=name,
        email=email or make_unique_email(),
        password_hash=password_hash,
        role=role,
        is_active=is_active,
        created_at=created_at or FIXED_TIMESTAMP,
        updated_at=updated_at or FIXED_TIMESTAMP,
    )
