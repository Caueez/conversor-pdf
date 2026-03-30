from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from account_service.infra.migration import Migrations
from infra.database.shared import Query


pytestmark = pytest.mark.unit


@dataclass
class FakePersistence:
    executed_queries: list[Query] = field(default_factory=list)

    async def execute(self, query: Query) -> str:
        self.executed_queries.append(query)
        return "OK"


def test_create_query_preserves_statement_and_sql() -> None:
    migration = Migrations(FakePersistence())
    query = migration.create_query(migration.USERS_TABLE)

    assert query.statement == "CREATE"
    assert "CREATE TABLE IF NOT EXISTS users" in query.query


async def test_run_executes_all_schema_queries() -> None:
    persistence = FakePersistence()
    migration = Migrations(persistence)

    await migration.run()

    assert len(persistence.executed_queries) == len(migration.tables)
    statements = {getattr(query.statement, "value", query.statement) for query in persistence.executed_queries}
    assert statements == {"CREATE", "ALTER"}
