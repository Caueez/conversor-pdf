from __future__ import annotations

import pytest
from pydantic import ValidationError

from account_service.api.schemas import CreateUserRequest, UpdateUserRequest


pytestmark = pytest.mark.unit


def test_create_user_request_accepts_valid_payload() -> None:
    payload = CreateUserRequest(name="Alice", email="alice@example.com", password="password-123")
    assert payload.name == "Alice"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("name", "A"),
        ("email", "a@b"),
        ("password", "1234567"),
    ],
)
def test_create_user_request_rejects_invalid_min_lengths(field: str, value: str) -> None:
    kwargs = {"name": "Alice", "email": "alice@example.com", "password": "password-123"}
    kwargs[field] = value
    with pytest.raises(ValidationError):
        CreateUserRequest(**kwargs)


def test_update_user_request_requires_at_least_one_field() -> None:
    with pytest.raises(ValidationError, match="At least one field must be provided for update"):
        UpdateUserRequest()


def test_update_user_request_rejects_password_above_max_length() -> None:
    with pytest.raises(ValidationError):
        UpdateUserRequest(password="a" * 73)


def test_update_user_request_accepts_single_field() -> None:
    payload = UpdateUserRequest(name="Updated")
    assert payload.name == "Updated"
