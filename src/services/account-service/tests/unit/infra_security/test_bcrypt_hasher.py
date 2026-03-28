from __future__ import annotations

import pytest

from infra.security.password_hashers.bcrypt import BcryptHasher


pytestmark = pytest.mark.unit


def test_bcrypt_hasher_hash_and_check_roundtrip() -> None:
    hasher = BcryptHasher(rounds=4)

    hashed = hasher.hash("password-123")

    assert hasher.check("password-123", hashed) is True
    assert hasher.check("wrong-password", hashed) is False
