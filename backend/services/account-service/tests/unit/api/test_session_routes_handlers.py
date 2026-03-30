from __future__ import annotations

from dataclasses import dataclass

import pytest

from account_service.api.routes.session import login, login_admin, logout, me, refresh, register
from account_service.api.schemas import CreateUserRequest, LoginRequest
from account_service.application.schemas import SessionTokenPairDTO, UserDTO


pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


@dataclass
class FakeSessionsUseCase:
    register_result: SessionTokenPairDTO | None = None
    login_result: SessionTokenPairDTO | None = None
    login_admin_result: SessionTokenPairDTO | None = None
    refresh_result: SessionTokenPairDTO | None = None
    me_result: UserDTO | None = None

    async def register(self, dto):
        self.register_dto = dto
        return self.register_result

    async def login(self, dto):
        self.login_dto = dto
        return self.login_result

    async def login_admin(self, dto):
        self.login_admin_dto = dto
        return self.login_admin_result

    async def refresh(self, token: str):
        self.refresh_token = token
        return self.refresh_result

    async def logout(self, token: str):
        self.logout_token = token

    async def me(self, token: str):
        self.me_token = token
        return self.me_result


@dataclass
class FakeContainer:
    sessions: FakeSessionsUseCase


def _token_pair_dto() -> SessionTokenPairDTO:
    return SessionTokenPairDTO(
        access_token="access-token",
        refresh_token="refresh-token",
        token_type="bearer",
        access_expires_at="2024-01-01T00:15:00+00:00",
        refresh_expires_at="2024-01-08T00:00:00+00:00",
    )


def _user_dto(user_id: str = "31cb2264-07a5-4d53-a758-05476fd48341") -> UserDTO:
    return UserDTO(
        id=user_id,
        name="Alice",
        email="alice@example.com",
        is_active=True,
        created_at="2024-01-01T00:00:00+00:00",
        updated_at="2024-01-01T00:00:00+00:00",
    )


async def test_login_builds_dto_and_returns_token_pair() -> None:
    sessions = FakeSessionsUseCase(login_result=_token_pair_dto())
    container = FakeContainer(sessions=sessions)

    response = await login(
        LoginRequest(email="alice@example.com", password="password-123"),
        "trace-id",
        container,
    )

    assert response.token_type == "bearer"
    assert sessions.login_dto.email == "alice@example.com"


async def test_register_builds_dto_and_returns_token_pair() -> None:
    sessions = FakeSessionsUseCase(register_result=_token_pair_dto())
    container = FakeContainer(sessions=sessions)

    response = await register(
        CreateUserRequest(name="Alice", email="alice@example.com", password="password-123"),
        "trace-id",
        container,
    )

    assert response.token_type == "bearer"
    assert sessions.register_dto.email == "alice@example.com"


async def test_admin_login_builds_dto_and_returns_token_pair() -> None:
    sessions = FakeSessionsUseCase(login_admin_result=_token_pair_dto())
    container = FakeContainer(sessions=sessions)

    response = await login_admin(
        LoginRequest(email="admin@example.com", password="password-123"),
        "trace-id",
        container,
    )

    assert response.token_type == "bearer"
    assert sessions.login_admin_dto.email == "admin@example.com"


async def test_refresh_forwards_bearer_token() -> None:
    sessions = FakeSessionsUseCase(refresh_result=_token_pair_dto())
    container = FakeContainer(sessions=sessions)

    response = await refresh("refresh-token", "trace-id", container)

    assert response.refresh_token == "refresh-token"
    assert sessions.refresh_token == "refresh-token"


async def test_logout_forwards_bearer_token() -> None:
    sessions = FakeSessionsUseCase()
    container = FakeContainer(sessions=sessions)

    await logout("access-token", "trace-id", container)

    assert sessions.logout_token == "access-token"


async def test_me_returns_user_response() -> None:
    sessions = FakeSessionsUseCase(me_result=_user_dto())
    container = FakeContainer(sessions=sessions)

    response = await me("access-token", "trace-id", container)

    assert response.email == "alice@example.com"
    assert sessions.me_token == "access-token"
