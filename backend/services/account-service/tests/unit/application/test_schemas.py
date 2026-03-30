from __future__ import annotations

import pytest

from account_service.application.schemas import (
    AccessTokenPayloadDTO,
    CreateUserDTO,
    DeleteUserDTO,
    LoginDTO,
    RefreshTokenPayloadDTO,
    SessionTokenPairDTO,
    UpdateUserDTO,
    UserDTO,
)
from account_service.domain.entities.role import ROLE_KEY_USER


pytestmark = pytest.mark.unit


def test_application_schema_models_roundtrip() -> None:
    create = CreateUserDTO(name="Alice", email="alice@example.com", password="password-123")
    delete = DeleteUserDTO(user_id="31cb2264-07a5-4d53-a758-05476fd48341")
    update = UpdateUserDTO(user_id=delete.user_id, name="Alice Updated")
    user = UserDTO(
        id=delete.user_id,
        name=create.name,
        email=create.email,
        is_active=True,
        created_at="2024-01-01T00:00:00+00:00",
        updated_at="2024-01-01T00:00:00+00:00",
    )

    assert create.name == "Alice"
    assert create.role == ROLE_KEY_USER
    assert delete.user_id == user.id
    assert update.name == "Alice Updated"
    assert user.email == "alice@example.com"


def test_session_schema_models_roundtrip() -> None:
    login = LoginDTO(email="alice@example.com", password="password-123")
    tokens = SessionTokenPairDTO(
        access_token="access",
        refresh_token="refresh",
        token_type="bearer",
        access_expires_at="2024-01-01T00:15:00+00:00",
        refresh_expires_at="2024-01-08T00:00:00+00:00",
    )
    access_payload = AccessTokenPayloadDTO(
        sub="31cb2264-07a5-4d53-a758-05476fd48341",
        session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
        type="access",
        exp=2_000_000_000,
    )
    refresh_payload = RefreshTokenPayloadDTO(
        sub=access_payload.sub,
        session_id=access_payload.session_id,
        jti="7f21a6ef-cf5a-4f4e-b4e5-d57af02104d4",
        type="refresh",
        exp=2_000_000_500,
    )

    assert login.email == "alice@example.com"
    assert tokens.token_type == "bearer"
    assert access_payload.type == "access"
    assert refresh_payload.type == "refresh"
