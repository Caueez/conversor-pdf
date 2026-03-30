from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

import pytest

from account_service.application.services.authorization_service import AuthorizationService
from account_service.application.services.user_service import UserService
from account_service.application.use_cases.sessions import SessionUseCase
from account_service.application.use_cases.users import UserUseCase
from account_service.domain.entities.role import ROLE_KEY_ADMIN
from account_service.infra.container import ContainerService
from account_service.settings import AccountSettings


pytestmark = pytest.mark.unit


class FakeUserRepo:
    async def create(self, user):  # pragma: no cover - behavior not under test
        return user

    async def get(self, user_id):  # pragma: no cover - behavior not under test
        return None

    async def get_by_email(self, email):  # pragma: no cover - behavior not under test
        return None

    async def list(self):  # pragma: no cover - behavior not under test
        return []

    async def update(self, user):  # pragma: no cover - behavior not under test
        return user

    async def delete(self, user_id):  # pragma: no cover - behavior not under test
        return None


class FakeSessionRepo:
    async def create(self, session):  # pragma: no cover - behavior not under test
        return session

    async def get(self, session_id):  # pragma: no cover - behavior not under test
        return None

    async def rotate(self, session_id, token_id, expires_at):  # pragma: no cover
        return None

    async def revoke(self, session_id):  # pragma: no cover - behavior not under test
        return None


class FakeAuthorizationRepo:
    async def ensure_defaults(self) -> None:
        return None

    async def get_role_by_key(self, key):
        return None

    async def get_permission_by_key(self, key):
        return None

    async def role_has_permission(self, role_key, permission_key):
        return False


@dataclass
class FakeBootstrapUsers:
    created_calls: list[object]

    async def create(self, dto):  # pragma: no cover - behavior not under test
        self.created_calls.append(dto)
        return dto


class FakeHasher:
    def hash(self, password: str) -> str:
        return f"hashed::{password}"

    def check(self, password: str, hashed_password: str) -> bool:
        return hashed_password == f"hashed::{password}"


@dataclass
class FakeBackend:
    connected: bool = False
    closed: bool = False

    async def connect(self) -> None:
        self.connected = True

    async def close(self) -> None:
        self.closed = True

    async def execute(self, _query) -> str:
        return "OK"


@dataclass
class FakeMigrations:
    run_called: bool = False

    async def run(self) -> None:
        self.run_called = True


@dataclass
class FakeAuthorizationService:
    ensure_defaults_called: bool = False

    async def ensure_defaults(self) -> None:
        self.ensure_defaults_called = True

    async def get_role_by_key(self, role_key: str):
        if role_key == ROLE_KEY_ADMIN:
            from account_service.domain.entities.role import Role

            return Role(key=ROLE_KEY_ADMIN, name="Administrator")
        return None

    async def has_permission(self, role_key: str, permission_key: str) -> bool:
        return role_key == ROLE_KEY_ADMIN


def _build_settings(**kwargs: object) -> AccountSettings:
    default_kwargs: dict[str, object] = {
        "DEBUG": False,
        "PERSISTENCE_BACKEND": "postgres",
        "USER_REPO": "postgres",
        "SESSION_REPO": "postgres",
        "POSTGRES_DSN": "postgresql://postgres:postgres@127.0.0.1:5432/user_service",
        "JWT_SECRET": "test-secret",
    }
    default_kwargs.update(kwargs)
    return AccountSettings(**default_kwargs)


async def test_container_build_wires_dependencies(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_backend = FakeBackend()
    fake_user_repo = FakeUserRepo()
    fake_session_repo = FakeSessionRepo()
    fake_authorization_repo = FakeAuthorizationRepo()
    settings = _build_settings()

    def fake_persistence_build(cls, settings):
        return fake_backend

    def fake_user_repo_build(cls, settings, persistence_backend):
        return fake_user_repo

    def fake_session_repo_build(cls, settings, persistence_backend):
        return fake_session_repo

    def fake_authorization_repo_build(cls, settings, persistence_backend):
        return fake_authorization_repo

    monkeypatch.setattr(ContainerService, "_persistence_build", classmethod(fake_persistence_build))
    monkeypatch.setattr(ContainerService, "_user_repo_build", classmethod(fake_user_repo_build))
    monkeypatch.setattr(ContainerService, "_session_repo_build", classmethod(fake_session_repo_build))
    monkeypatch.setattr(
        ContainerService,
        "_authorization_repo_build",
        classmethod(fake_authorization_repo_build),
    )

    container = ContainerService.build(settings)

    assert container.settings == settings
    assert container.user_repo is fake_user_repo
    assert container.session_repo is fake_session_repo
    assert container.authorization_repo is fake_authorization_repo
    assert isinstance(container.user_service, UserService)
    assert isinstance(container.authorization_service, AuthorizationService)
    assert isinstance(container.users, UserUseCase)
    assert isinstance(container.sessions, SessionUseCase)
    assert container._persistence_backend is fake_backend  # noqa: SLF001


async def test_container_startup_and_shutdown() -> None:
    settings = _build_settings()
    backend = FakeBackend()
    migrations = FakeMigrations()
    user_repo = FakeUserRepo()
    session_repo = FakeSessionRepo()
    authorization_service = FakeAuthorizationService()
    user_service = UserService(user_repo, FakeHasher(), authorization_service)  # type: ignore[arg-type]
    users = UserUseCase(user_service)
    sessions = SessionUseCase(
        user_service=user_service,
        authorization_service=authorization_service,  # type: ignore[arg-type]
        session_repository=session_repo,
        token_service=object(),
        access_ttl=timedelta(minutes=15),
        refresh_ttl=timedelta(days=7),
    )
    container = ContainerService(
        settings=settings,
        users=users,
        sessions=sessions,
        user_service=user_service,
        authorization_service=authorization_service,  # type: ignore[arg-type]
        user_repo=user_repo,
        session_repo=session_repo,
        authorization_repo=FakeAuthorizationRepo(),
        _migrations=migrations,
        _persistence_backend=backend,
    )

    await container.startup()
    await container.shutdown()

    assert backend.connected is True
    assert migrations.run_called is True
    assert authorization_service.ensure_defaults_called is True
    assert backend.closed is True


def test_persistence_build_rejects_unknown_backend() -> None:
    settings = _build_settings(PERSISTENCE_BACKEND="unknown")

    with pytest.raises(ValueError, match="Persistence backend not found"):
        ContainerService._persistence_build(settings)


def test_user_repo_build_rejects_unknown_repo_backend() -> None:
    settings = _build_settings(USER_REPO="unknown")

    with pytest.raises(ValueError, match="User repository backend not found"):
        ContainerService._user_repo_build(settings, FakeBackend())


def test_session_repo_build_rejects_unknown_repo_backend() -> None:
    settings = _build_settings(SESSION_REPO="unknown")

    with pytest.raises(ValueError, match="Session repository backend not found"):
        ContainerService._session_repo_build(settings, FakeBackend())


def test_authorization_repo_build_rejects_unknown_repo_backend() -> None:
    settings = _build_settings(USER_REPO="unknown")

    with pytest.raises(ValueError, match="Authorization repository backend not found"):
        ContainerService._authorization_repo_build(settings, FakeBackend())


async def test_container_startup_bootstraps_admin_when_enabled_and_empty_db() -> None:
    settings = _build_settings(
        BOOTSTRAP_ADMIN_ENABLED=True,
        BOOTSTRAP_ADMIN_NAME="Bootstrap Admin",
        BOOTSTRAP_ADMIN_EMAIL="bootstrap@example.com",
        BOOTSTRAP_ADMIN_PASSWORD="password-123",
    )
    backend = FakeBackend()
    migrations = FakeMigrations()
    user_repo = FakeUserRepo()
    session_repo = FakeSessionRepo()
    authorization_service = FakeAuthorizationService()
    user_service = FakeBootstrapUsers(created_calls=[])
    container = ContainerService(
        settings=settings,
        users=UserUseCase(UserService(user_repo, FakeHasher(), authorization_service)),  # type: ignore[arg-type]
        sessions=SessionUseCase(  # pragma: no cover - not relevant in this test
            user_service=UserService(user_repo, FakeHasher(), authorization_service),  # type: ignore[arg-type]
            authorization_service=authorization_service,  # type: ignore[arg-type]
            session_repository=session_repo,
            token_service=object(),
            access_ttl=timedelta(minutes=15),
            refresh_ttl=timedelta(days=7),
        ),
        user_service=user_service,  # type: ignore[arg-type]
        authorization_service=authorization_service,  # type: ignore[arg-type]
        user_repo=user_repo,
        session_repo=session_repo,
        authorization_repo=FakeAuthorizationRepo(),
        _migrations=migrations,
        _persistence_backend=backend,
    )

    await container.startup()

    assert len(user_service.created_calls) == 1
    dto = user_service.created_calls[0]
    assert dto.name == "Bootstrap Admin"
    assert dto.email == "bootstrap@example.com"
    assert dto.role == ROLE_KEY_ADMIN
