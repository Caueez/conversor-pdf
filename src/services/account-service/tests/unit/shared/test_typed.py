from __future__ import annotations

from datetime import UTC
from uuid import UUID

import pytest

from account_service.shared.typed import new_uuid, utc_now


pytestmark = pytest.mark.unit


def test_utc_now_returns_utc_timezone() -> None:
    now = utc_now()
    assert now.tzinfo is UTC


def test_new_uuid_returns_valid_uuid_string() -> None:
    value = new_uuid()
    UUID(value)
