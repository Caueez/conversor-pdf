from __future__ import annotations

import pytest

from infra.database.shared import DatabaseRow, Query


pytestmark = pytest.mark.unit


def test_database_row_returns_none_for_missing_key() -> None:
    row = DatabaseRow.create({"id": "123"})
    assert row["id"] == "123"
    assert row["unknown"] is None


def test_query_create_accepts_matching_statement() -> None:
    query = Query.create("SELECT", "SELECT id FROM users", [])
    assert query.statement.value == "SELECT"
    assert query.query.startswith("SELECT")


def test_query_create_rejects_mismatched_statement() -> None:
    with pytest.raises(RuntimeError, match="Invalid query"):
        Query.create("INSERT", "SELECT id FROM users", [])
