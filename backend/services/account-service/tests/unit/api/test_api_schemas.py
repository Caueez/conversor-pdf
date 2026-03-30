from __future__ import annotations

import pytest
from pydantic import ValidationError

from account_service.api.schemas import CreateUserRequest, LoginRequest, TokenPairResponse, UpdateUserRequest


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


def test_login_request_accepts_valid_payload() -> None:
    payload = LoginRequest(email="alice@example.com", password="password-123")
    assert payload.email == "alice@example.com"


def test_login_request_rejects_short_password() -> None:
    with pytest.raises(ValidationError):
        LoginRequest(email="alice@example.com", password="short")


def test_token_pair_response_schema_maps_tokens() -> None:
    payload = TokenPairResponse(
        access_token="access",
        refresh_token="refresh",
        token_type="bearer",
        access_expires_at="2024-01-01T00:15:00+00:00",
        refresh_expires_at="2024-01-08T00:00:00+00:00",
    )
    assert payload.token_type == "bearer"
