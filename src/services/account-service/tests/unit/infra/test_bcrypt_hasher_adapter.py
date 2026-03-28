from __future__ import annotations

import pytest

from account_service.infra.security.bcrypt_hasher_adapter import BcryptPasswordHasherAdapter


pytestmark = pytest.mark.unit


class FakeBcryptHasher:
    def __init__(self) -> None:
        self.hash_calls: list[str] = []
        self.check_calls: list[tuple[str, str]] = []

    def hash(self, password: str) -> str:
        self.hash_calls.append(password)
        return f"hashed::{password}"

    def check(self, password: str, hashed_password: str) -> bool:
        self.check_calls.append((password, hashed_password))
        return hashed_password == f"hashed::{password}"


def test_adapter_delegates_hash_and_check() -> None:
    backend = FakeBcryptHasher()
    adapter = BcryptPasswordHasherAdapter(backend)

    hashed = adapter.hash("password-123")
    checked = adapter.check("password-123", hashed)

    assert hashed == "hashed::password-123"
    assert checked is True
    assert backend.hash_calls == ["password-123"]
    assert backend.check_calls == [("password-123", "hashed::password-123")]
