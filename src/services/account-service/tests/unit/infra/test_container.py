from __future__ import annotations

from dataclasses import dataclass

import pytest

from account_service.application.use_cases.users import UserUseCase
from account_service.infra.container import ContainerService
from account_service.settings import AccountSettings


pytestmark = pytest.mark.unit


class FakeRepo:
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


def _build_settings(**kwargs: object) -> AccountSettings:
    default_kwargs: dict[str, object] = {
        "DEBUG": False,
        "PERSISTENCE_BACKEND": "postgres",
        "USER_REPO": "postgres",
        "POSTGRES_DSN": "postgresql://postgres:postgres@127.0.0.1:5432/user_service",
    }
    default_kwargs.update(kwargs)
    return AccountSettings(**default_kwargs)


async def test_container_build_wires_dependencies(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_backend = FakeBackend()
    fake_repo = FakeRepo()
    settings = _build_settings()

    def fake_persistence_build(cls, settings):
        return fake_backend

    def fake_repo_build(cls, settings, persistence_backend):
        return fake_repo

    monkeypatch.setattr(ContainerService, "_persistence_build", classmethod(fake_persistence_build))
    monkeypatch.setattr(ContainerService, "_repo_build", classmethod(fake_repo_build))

    container = ContainerService.build(settings)

    assert container.settings == settings
    assert container.user_repo is fake_repo
    assert isinstance(container.users, UserUseCase)
    assert container._persistence_backend is fake_backend  # noqa: SLF001


async def test_container_startup_and_shutdown() -> None:
    settings = _build_settings()
    backend = FakeBackend()
    migrations = FakeMigrations()
    repo = FakeRepo()
    users = UserUseCase(repo, FakeHasher())
    container = ContainerService(
        settings=settings,
        users=users,
        user_repo=repo,
        _migrations=migrations,
        _persistence_backend=backend,
    )

    await container.startup()
    await container.shutdown()

    assert backend.connected is True
    assert migrations.run_called is True
    assert backend.closed is True


def test_persistence_build_rejects_unknown_backend() -> None:
    settings = _build_settings(PERSISTENCE_BACKEND="unknown")

    with pytest.raises(ValueError, match="Persistence backend not found"):
        ContainerService._persistence_build(settings)


def test_repo_build_rejects_unknown_repo_backend() -> None:
    settings = _build_settings(USER_REPO="unknown")

    with pytest.raises(ValueError, match="Persistence backend not found"):
        ContainerService._repo_build(settings, FakeBackend())
