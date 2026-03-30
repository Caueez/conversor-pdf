from __future__ import annotations

import pytest

from account_service.domain.exceptions import ValidationDomainError
from account_service.domain.value_objects.user import (
    Email,
    Password,
    Role,
)
from account_service.domain.entities.role import ROLE_KEY_ADMIN, ROLE_KEY_USER


pytestmark = pytest.mark.unit


def test_email_accepts_valid_format() -> None:
    email = Email("valid.user@example.com")
    assert email.value == "valid.user@example.com"


@pytest.mark.parametrize(
    "raw_email",
    [
        "invalid",
        "missing-at.example.com",
        "missing-domain@",
        "bad space@example.com",
    ],
)
def test_email_rejects_invalid_format(raw_email: str) -> None:
    with pytest.raises(ValidationDomainError, match="Email is not valid"):
        Email(raw_email)


def test_password_rejects_too_short() -> None:
    with pytest.raises(ValidationDomainError, match="at least 8"):
        Password("1234567")


def test_password_accepts_minimum_length() -> None:
    password = Password("12345678")
    assert password.value == "12345678"


def test_password_accepts_maximum_length() -> None:
    raw_password = "a" * 72
    password = Password(raw_password)
    assert password.value == raw_password


def test_password_rejects_above_maximum_length() -> None:
    with pytest.raises(ValidationDomainError, match="at most 72"):
        Password("a" * 73)


@pytest.mark.parametrize("role", [ROLE_KEY_ADMIN, ROLE_KEY_USER, "role:auditor"])
def test_role_accepts_allowed_values(role: str) -> None:
    validated = Role(role)
    assert validated.value == role


def test_role_rejects_unknown_value() -> None:
    with pytest.raises(ValidationDomainError, match="Role is not valid"):
        Role("A")
