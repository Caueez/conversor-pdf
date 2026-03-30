from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest

from account_service.domain.entities.session import Session


pytestmark = pytest.mark.unit


def test_session_to_dict_serializes_expected_fields() -> None:
    created_at = datetime(2024, 1, 1, 12, 0, tzinfo=UTC)
    expires_at = datetime(2024, 1, 8, 12, 0, tzinfo=UTC)
    session = Session(
        user_id="31cb2264-07a5-4d53-a758-05476fd48341",
        token_id="refresh-jti",
        expires_at=expires_at,
        created_at=created_at,
    )

    payload = session.to_dict()
    assert payload["id"] == session.id
    assert payload["user_id"] == session.user_id
    assert payload["token_id"] == "refresh-jti"
    assert payload["revoked"] is False
    assert payload["created_at"] == created_at.isoformat()
    assert payload["expires_at"] == expires_at.isoformat()


def test_session_defaults_generate_uuid_and_created_at() -> None:
    session = Session(
        user_id="31cb2264-07a5-4d53-a758-05476fd48341",
        token_id="refresh-jti",
        expires_at=datetime(2024, 1, 8, 12, 0, tzinfo=UTC),
    )

    UUID(session.id)
    assert session.created_at.tzinfo is UTC
    assert session.revoked is False
