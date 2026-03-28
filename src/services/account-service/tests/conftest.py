from __future__ import annotations

import os
from typing import AsyncIterator

import asyncpg
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

import account_service.api.lifespan as lifespan_module
from account_service.api.app import create_app
from account_service.infra.migration import Migrations
from account_service.infra.repositories.user import PostgresUserRepoAdapter
from account_service.settings import AccountSettings
from infra.database.implementations.postgres import Postgres


DEFAULT_TEST_POSTGRES_DSN = "postgresql://postgres:postgres@127.0.0.1:5432/user_service"


def _postgres_dsn_from_env() -> str:
    return os.getenv("APP_TEST_POSTGRES_DSN", DEFAULT_TEST_POSTGRES_DSN)


async def _truncate_tables(postgres_dsn: str) -> None:
    connection = await asyncpg.connect(postgres_dsn)
    try:
        await connection.execute("TRUNCATE TABLE users, sessions RESTART IDENTITY CASCADE;")
    finally:
        await connection.close()


@pytest.fixture(scope="session")
def postgres_dsn() -> str:
    return _postgres_dsn_from_env()


@pytest_asyncio.fixture(scope="session")
async def require_postgres(postgres_dsn: str) -> None:
    try:
        connection = await asyncpg.connect(postgres_dsn)
    except Exception as exc:  # pragma: no cover - depends on local infra availability
        pytest.skip(f"Postgres indisponivel para testes de integracao/e2e: {exc}")
    else:
        await connection.close()


@pytest.fixture
def test_settings(postgres_dsn: str) -> AccountSettings:
    return AccountSettings(
        DEBUG=False,
        PERSISTENCE_BACKEND="postgres",
        USER_REPO="postgres",
        POSTGRES_DSN=postgres_dsn,
    )


@pytest_asyncio.fixture
async def db_backend(require_postgres: None, postgres_dsn: str) -> AsyncIterator[Postgres]:
    backend = Postgres(postgres_dsn)
    await backend.connect()
    await Migrations(backend).run()
    try:
        yield backend
    finally:
        await backend.close()


@pytest_asyncio.fixture
async def clean_database(db_backend: Postgres, postgres_dsn: str) -> AsyncIterator[None]:
    await _truncate_tables(postgres_dsn)
    try:
        yield
    finally:
        await _truncate_tables(postgres_dsn)


@pytest_asyncio.fixture
async def user_repo(db_backend: Postgres, clean_database: None) -> PostgresUserRepoAdapter:
    return PostgresUserRepoAdapter(db_backend)


@pytest_asyncio.fixture
async def app_client(
    test_settings: AccountSettings,
    clean_database: None,
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncIterator[AsyncClient]:
    monkeypatch.setattr(lifespan_module, "get_settings", lambda: test_settings)
    app = create_app()

    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client
