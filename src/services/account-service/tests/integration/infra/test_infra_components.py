from __future__ import annotations

import pytest

from account_service.infra.security.bcrypt_hasher_adapter import BcryptPasswordHasherAdapter
from infra.database.implementations.postgres import Postgres
from infra.database.shared import Query
from infra.security.password_hashers.bcrypt import BcryptHasher


pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_postgres_backend_executes_real_query(db_backend: Postgres) -> None:
    query = Query.create("SELECT", "SELECT 1 AS value", [])

    row = await db_backend.fetch_one(query)

    assert row is not None
    assert row["value"] == 1


def test_query_create_rejects_invalid_statement_order() -> None:
    with pytest.raises(RuntimeError, match="Invalid query"):
        Query.create("DELETE", "SELECT 1", [])


def test_bcrypt_adapter_hash_and_check() -> None:
    adapter = BcryptPasswordHasherAdapter(BcryptHasher(rounds=4))
    hashed = adapter.hash("password-123")

    assert adapter.check("password-123", hashed) is True
    assert adapter.check("wrong-password", hashed) is False
