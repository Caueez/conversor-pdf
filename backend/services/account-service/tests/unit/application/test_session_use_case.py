from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Sequence
from uuid import UUID

import pytest

from account_service.application.schemas import CreateUserDTO, LoginDTO
from account_service.application.services.authorization_service import AuthorizationService
from account_service.application.services.user_service import UserService
from account_service.application.use_cases.sessions import SessionUseCase
from account_service.domain.entities.permission import PERMISSION_USERS_MANAGE
from account_service.domain.entities.role import ROLE_KEY_ADMIN, ROLE_KEY_USER, Role
from account_service.domain.entities.session import Session
from account_service.domain.entities.user import User
from account_service.domain.exceptions import AuthenticationDomainError, AuthorizationDomainError
from tests.factories.users import make_unique_email, make_user_entity


pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


class InMemoryUserRepo:
    def __init__(self, users: Sequence[User] | None = None) -> None:
        self._users: dict[str, User] = {}
        for user in users or []:
            self._users[str(user.id)] = user

    async def create(self, user: User) -> User:
        self._users[str(user.id)] = user
        return user

    async def get(self, user_id: UUID) -> User | None:
        return self._users.get(str(user_id))

    async def get_by_email(self, email: str) -> User | None:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    async def list(self) -> Sequence[User]:
        return list(self._users.values())

    async def update(self, user: User) -> User:
        self._users[str(user.id)] = user
        return user

    async def delete(self, user_id: UUID) -> None:
        self._users.pop(str(user_id), None)


class InMemorySessionRepo:
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    async def create(self, session: Session) -> Session:
        self._sessions[str(session.id)] = session
        return session

    async def get(self, session_id: UUID) -> Session | None:
        return self._sessions.get(str(session_id))

    async def rotate(self, session_id: UUID, token_id: str, expires_at: datetime) -> None:
        current = self._sessions.get(str(session_id))
        if not current:
            return
        self._sessions[str(session_id)] = Session(
            id=current.id,
            user_id=current.user_id,
            token_id=token_id,
            expires_at=expires_at,
            revoked=current.revoked,
            created_at=current.created_at,
        )

    async def revoke(self, session_id: UUID) -> None:
        current = self._sessions.get(str(session_id))
        if not current:
            return
        self._sessions[str(session_id)] = Session(
            id=current.id,
            user_id=current.user_id,
            token_id=current.token_id,
            expires_at=current.expires_at,
            revoked=True,
            created_at=current.created_at,
        )


class FakeHasher:
    def hash(self, password: str) -> str:
        return f"hashed::{password}"

    def check(self, password: str, hashed_password: str) -> bool:
        return hashed_password == f"hashed::{password}"


class InMemoryAuthorizationRepo:
    async def ensure_defaults(self) -> None:
        return None

    async def get_role_by_key(self, key: str) -> Role | None:
        if key == ROLE_KEY_ADMIN:
            return Role(key=ROLE_KEY_ADMIN, name="Administrator")
        if key == ROLE_KEY_USER:
            return Role(key=ROLE_KEY_USER, name="User")
        return None

    async def get_permission_by_key(self, key: str):
        return None

    async def role_has_permission(self, role_key: str, permission_key: str) -> bool:
        return role_key == ROLE_KEY_ADMIN and permission_key == PERMISSION_USERS_MANAGE


class FakeTokenService:
    def __init__(self) -> None:
        self._tokens: dict[str, dict[str, str | int]] = {}
        self._counter = 0

    def issue_access_token(self, *, user_id: str, session_id: str, expires_at: datetime) -> str:
        token = self._next_token("access")
        self._tokens[token] = {
            "sub": user_id,
            "session_id": session_id,
            "type": "access",
            "exp": int(expires_at.timestamp()),
        }
        return token

    def issue_refresh_token(self, *, user_id: str, session_id: str, token_id: str, expires_at: datetime) -> str:
        token = self._next_token("refresh")
        self._tokens[token] = {
            "sub": user_id,
            "session_id": session_id,
            "jti": token_id,
            "type": "refresh",
            "exp": int(expires_at.timestamp()),
        }
        return token

    def decode_access_token(self, token: str):
        payload = self._tokens.get(token)
        if not payload or payload["type"] != "access":
            raise AuthenticationDomainError("Invalid access token")
        from account_service.application.schemas import AccessTokenPayloadDTO

        return AccessTokenPayloadDTO.model_validate(payload)

    def decode_refresh_token(self, token: str):
        payload = self._tokens.get(token)
        if not payload or payload["type"] != "refresh":
            raise AuthenticationDomainError("Invalid refresh token")
        from account_service.application.schemas import RefreshTokenPayloadDTO

        return RefreshTokenPayloadDTO.model_validate(payload)

    def _next_token(self, prefix: str) -> str:
        self._counter += 1
        return f"{prefix}-{self._counter}"


def _build_use_case(users: Sequence[User] | None = None) -> tuple[SessionUseCase, InMemorySessionRepo]:
    user_repo = InMemoryUserRepo(users)
    authorization_service = AuthorizationService(InMemoryAuthorizationRepo())
    user_service = UserService(user_repo, FakeHasher(), authorization_service)
    session_repo = InMemorySessionRepo()
    use_case = SessionUseCase(
        user_service=user_service,
        authorization_service=authorization_service,
        session_repository=session_repo,
        token_service=FakeTokenService(),
        access_ttl=timedelta(minutes=15),
        refresh_ttl=timedelta(days=7),
    )
    return use_case, session_repo


async def test_login_creates_session_and_returns_token_pair() -> None:
    user = make_user_entity(email=make_unique_email("login"), password_hash="hashed::password-123")
    use_case, session_repo = _build_use_case(users=[user])

    response = await use_case.login(LoginDTO(email=user.email, password="password-123"))

    assert response.token_type == "bearer"
    assert response.access_token
    assert response.refresh_token
    assert len(session_repo._sessions) == 1  # noqa: SLF001


async def test_register_creates_user_and_returns_token_pair() -> None:
    use_case, session_repo = _build_use_case(users=None)
    dto = CreateUserDTO(name="Alice", email=make_unique_email("register"), password="password-123")

    response = await use_case.register(dto)

    assert response.token_type == "bearer"
    assert response.access_token
    assert response.refresh_token
    assert len(session_repo._sessions) == 1  # noqa: SLF001


async def test_login_rejects_invalid_credentials() -> None:
    user = make_user_entity(email=make_unique_email("invalid-credentials"), password_hash="hashed::password-123")
    use_case, _ = _build_use_case(users=[user])

    with pytest.raises(AuthenticationDomainError, match="Invalid credentials"):
        await use_case.login(LoginDTO(email=user.email, password="wrong-password"))


async def test_admin_login_accepts_admin_credentials() -> None:
    admin = make_user_entity(
        email=make_unique_email("admin-login"),
        password_hash="hashed::password-123",
        role=ROLE_KEY_ADMIN,
    )
    use_case, session_repo = _build_use_case(users=[admin])

    response = await use_case.login_admin(LoginDTO(email=admin.email, password="password-123"))

    assert response.access_token
    assert len(session_repo._sessions) == 1  # noqa: SLF001


async def test_admin_login_rejects_non_admin_credentials() -> None:
    user = make_user_entity(
        email=make_unique_email("common-login"),
        password_hash="hashed::password-123",
        role=ROLE_KEY_USER,
    )
    use_case, _ = _build_use_case(users=[user])

    with pytest.raises(AuthorizationDomainError, match="Admin credentials are required"):
        await use_case.login_admin(LoginDTO(email=user.email, password="password-123"))


async def test_refresh_rotates_refresh_token_and_rejects_previous_one() -> None:
    user = make_user_entity(email=make_unique_email("refresh"), password_hash="hashed::password-123")
    use_case, _ = _build_use_case(users=[user])

    login_response = await use_case.login(LoginDTO(email=user.email, password="password-123"))
    refreshed = await use_case.refresh(login_response.refresh_token)

    assert refreshed.refresh_token != login_response.refresh_token

    with pytest.raises(AuthenticationDomainError, match="Invalid refresh token"):
        await use_case.refresh(login_response.refresh_token)


async def test_logout_revokes_session_and_blocks_token_usage() -> None:
    user = make_user_entity(email=make_unique_email("logout"), password_hash="hashed::password-123")
    use_case, _ = _build_use_case(users=[user])

    login_response = await use_case.login(LoginDTO(email=user.email, password="password-123"))

    await use_case.logout(login_response.access_token)

    with pytest.raises(AuthenticationDomainError, match="Session is not active"):
        await use_case.authenticate_access_token(login_response.access_token)


async def test_me_returns_user_for_valid_access_token() -> None:
    user = make_user_entity(
        user_id="31cb2264-07a5-4d53-a758-05476fd48341",
        email=make_unique_email("me"),
        password_hash="hashed::password-123",
    )
    use_case, _ = _build_use_case(users=[user])

    login_response = await use_case.login(LoginDTO(email=user.email, password="password-123"))
    me_response = await use_case.me(login_response.access_token)

    assert me_response.id == str(user.id)
    assert me_response.email == user.email


async def test_refresh_rejects_expired_session(monkeypatch: pytest.MonkeyPatch) -> None:
    user = make_user_entity(email=make_unique_email("refresh-expired"), password_hash="hashed::password-123")
    use_case, _ = _build_use_case(users=[user])

    frozen_now = datetime(2024, 1, 1, tzinfo=UTC)
    monkeypatch.setattr("account_service.application.use_cases.sessions.utc_now", lambda: frozen_now)
    login_response = await use_case.login(LoginDTO(email=user.email, password="password-123"))

    monkeypatch.setattr(
        "account_service.application.use_cases.sessions.utc_now",
        lambda: frozen_now + timedelta(days=8),
    )

    with pytest.raises(AuthenticationDomainError, match="Invalid refresh token"):
        await use_case.refresh(login_response.refresh_token)
