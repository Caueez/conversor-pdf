from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request

import account_service.api.dependencies as dependencies_module
from account_service.api.dependencies import (
    AuthenticatedSession,
    get_admin_session,
    get_authenticated_session,
    get_bearer_token,
    get_container,
    get_trace_id,
)
from account_service.application.schemas import AccessTokenPayloadDTO
from account_service.domain.entities.role import ROLE_KEY_ADMIN, ROLE_KEY_USER
from account_service.domain.exceptions import AuthenticationDomainError, AuthorizationDomainError


pytestmark = pytest.mark.unit


@dataclass
class FakeSessionsUseCase:
    payload: AccessTokenPayloadDTO

    async def authenticate_access_token(self, token: str) -> AccessTokenPayloadDTO:
        self.received_token = token
        return self.payload


@dataclass
class FakeUser:
    role: str


@dataclass
class FakeUserService:
    user: FakeUser | None

    async def get_active_by_id(self, user_id: UUID) -> FakeUser | None:
        self.received_user_id = user_id
        return self.user


@dataclass
class FakeAuthorizationService:
    allowed: bool

    async def has_permission(self, role_key: str, permission_key: str) -> bool:
        self.received_role_key = role_key
        self.received_permission_key = permission_key
        return self.allowed


@dataclass
class FakeContainer:
    sessions: FakeSessionsUseCase
    user_service: FakeUserService
    authorization_service: FakeAuthorizationService


def _build_request(
    *,
    app: FastAPI | None = None,
    headers: list[tuple[bytes, bytes]] | None = None,
) -> Request:
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "path": "/",
        "headers": headers or [],
        "app": app or FastAPI(),
    }
    return Request(scope)


def test_get_container_reads_container_from_app_state() -> None:
    app = FastAPI()
    container = object()
    app.state.container = container
    request = _build_request(app=app)

    assert get_container(request) is container


def test_get_trace_id_prefers_request_state() -> None:
    request = _build_request(headers=[(b"x-trace-id", b"header-trace-id")])
    request._state = SimpleNamespace(trace_id="state-trace-id")  # noqa: SLF001

    assert get_trace_id(request) == "state-trace-id"


def test_get_trace_id_uses_header_when_state_is_missing() -> None:
    request = _build_request(headers=[(b"x-trace-id", b"header-trace-id")])

    assert get_trace_id(request) == "header-trace-id"


def test_get_trace_id_generates_value_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(dependencies_module, "new_uuid", lambda: "generated-trace-id")
    request = _build_request()

    assert get_trace_id(request) == "generated-trace-id"


def test_get_bearer_token_reads_authorization_header() -> None:
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="test-token")

    assert get_bearer_token(credentials) == "test-token"


@pytest.mark.parametrize(
    "credentials",
    [
        None,
        HTTPAuthorizationCredentials(scheme="Basic", credentials="abc"),
        HTTPAuthorizationCredentials(scheme="Bearer", credentials=""),
    ],
)
def test_get_bearer_token_rejects_invalid_headers(
    credentials: HTTPAuthorizationCredentials | None,
) -> None:
    with pytest.raises(AuthenticationDomainError):
        get_bearer_token(credentials)


@pytest.mark.asyncio
async def test_get_authenticated_session_validates_token_and_returns_payload() -> None:
    payload = AccessTokenPayloadDTO(
        sub="31cb2264-07a5-4d53-a758-05476fd48341",
        session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
        type="access",
        exp=2_000_000_000,
    )
    sessions = FakeSessionsUseCase(payload=payload)
    user_service = FakeUserService(user=FakeUser(role=ROLE_KEY_USER))
    authorization_service = FakeAuthorizationService(allowed=False)
    app = FastAPI()
    app.state.container = FakeContainer(
        sessions=sessions,
        user_service=user_service,
        authorization_service=authorization_service,
    )
    request = _build_request(app=app)

    authenticated = await get_authenticated_session(request, "access-token")

    assert sessions.received_token == "access-token"
    assert user_service.received_user_id == UUID(payload.sub)
    assert authenticated.user_id == payload.sub
    assert authenticated.session_id == payload.session_id
    assert authenticated.role == ROLE_KEY_USER


@pytest.mark.asyncio
async def test_get_authenticated_session_rejects_missing_active_user() -> None:
    payload = AccessTokenPayloadDTO(
        sub="31cb2264-07a5-4d53-a758-05476fd48341",
        session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
        type="access",
        exp=2_000_000_000,
    )
    sessions = FakeSessionsUseCase(payload=payload)
    user_service = FakeUserService(user=None)
    authorization_service = FakeAuthorizationService(allowed=False)
    app = FastAPI()
    app.state.container = FakeContainer(
        sessions=sessions,
        user_service=user_service,
        authorization_service=authorization_service,
    )
    request = _build_request(app=app)

    with pytest.raises(AuthenticationDomainError, match="Session is not active"):
        await get_authenticated_session(request, "access-token")


@pytest.mark.asyncio
async def test_get_admin_session_allows_admin() -> None:
    app = FastAPI()
    authorization_service = FakeAuthorizationService(allowed=True)
    app.state.container = FakeContainer(
        sessions=FakeSessionsUseCase(
            payload=AccessTokenPayloadDTO(
                sub="31cb2264-07a5-4d53-a758-05476fd48341",
                session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
                type="access",
                exp=2_000_000_000,
            )
        ),
        user_service=FakeUserService(user=FakeUser(role=ROLE_KEY_ADMIN)),
        authorization_service=authorization_service,
    )
    request = _build_request(app=app)
    session = AuthenticatedSession(
        user_id="31cb2264-07a5-4d53-a758-05476fd48341",
        session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
        role=ROLE_KEY_ADMIN,
    )

    assert await get_admin_session(request, session) == session
    assert authorization_service.received_role_key == ROLE_KEY_ADMIN


@pytest.mark.asyncio
async def test_get_admin_session_rejects_non_admin() -> None:
    app = FastAPI()
    app.state.container = FakeContainer(
        sessions=FakeSessionsUseCase(
            payload=AccessTokenPayloadDTO(
                sub="31cb2264-07a5-4d53-a758-05476fd48341",
                session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
                type="access",
                exp=2_000_000_000,
            )
        ),
        user_service=FakeUserService(user=FakeUser(role=ROLE_KEY_USER)),
        authorization_service=FakeAuthorizationService(allowed=False),
    )
    request = _build_request(app=app)
    session = AuthenticatedSession(
        user_id="31cb2264-07a5-4d53-a758-05476fd48341",
        session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
        role=ROLE_KEY_USER,
    )

    with pytest.raises(AuthorizationDomainError, match="Admin privileges are required"):
        await get_admin_session(request, session)
