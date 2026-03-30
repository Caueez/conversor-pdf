from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

import infra.database.implementations.postgres as postgres_module
from infra.database.implementations.postgres import Postgres
from infra.database.shared import Query


pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


@dataclass
class FakePool:
    fetchrow_result: dict[str, Any] | None = None
    fetch_result: list[dict[str, Any]] | None = None
    execute_result: str = "EXECUTED"
    closed: bool = False

    async def fetchrow(self, _query: str, *_values: object):
        return self.fetchrow_result

    async def fetch(self, _query: str, *_values: object):
        return self.fetch_result or []

    async def execute(self, _query: str, *_values: object):
        return self.execute_result

    async def close(self) -> None:
        self.closed = True


async def test_connect_uses_asyncpg_pool(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_pool = FakePool()

    async def fake_create_pool(*, dsn: str):
        assert dsn == "postgresql://example"
        return fake_pool

    monkeypatch.setattr(postgres_module.asyncpg, "create_pool", fake_create_pool)
    db = Postgres("postgresql://example")

    await db.connect()

    assert db._pool is fake_pool  # noqa: SLF001


async def test_close_closes_existing_pool() -> None:
    db = Postgres("postgresql://example")
    fake_pool = FakePool()
    db._pool = fake_pool  # noqa: SLF001

    await db.close()

    assert fake_pool.closed is True


async def test_fetch_one_requires_initialized_pool() -> None:
    db = Postgres("postgresql://example")
    query = Query.create("SELECT", "SELECT 1", [])

    with pytest.raises(RuntimeError, match="Postgres not initialized"):
        await db.fetch_one(query)


async def test_fetch_one_returns_database_row_or_none() -> None:
    db = Postgres("postgresql://example")
    fake_pool = FakePool(fetchrow_result={"id": "123", "name": "Alice"})
    db._pool = fake_pool  # noqa: SLF001
    query = Query.create("SELECT", "SELECT id, name FROM users", [])

    row = await db.fetch_one(query)

    assert row is not None
    assert row["id"] == "123"
    assert row["name"] == "Alice"

    fake_pool.fetchrow_result = None
    no_row = await db.fetch_one(query)
    assert no_row is None


async def test_fetch_all_and_execute_delegate_to_pool() -> None:
    db = Postgres("postgresql://example")
    fake_pool = FakePool(fetch_result=[{"id": "1"}, {"id": "2"}], execute_result="DELETE 1")
    db._pool = fake_pool  # noqa: SLF001
    select_query = Query.create("SELECT", "SELECT id FROM users", [])
    delete_query = Query.create("DELETE", "DELETE FROM users WHERE id = $1", ["1"])

    rows = await db.fetch_all(select_query)
    result = await db.execute(delete_query)

    assert [row["id"] for row in rows] == ["1", "2"]
    assert result == "DELETE 1"
