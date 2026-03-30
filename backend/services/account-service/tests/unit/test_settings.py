from __future__ import annotations

import pytest

from account_service.settings import AccountSettings, get_settings


pytestmark = pytest.mark.unit


def test_account_settings_accepts_explicit_values() -> None:
    settings = AccountSettings(DEBUG=False, PASSWORD_HASHER_ROUNDS=6, JWT_SECRET="test-secret")
    assert settings.DEBUG is False
    assert settings.PASSWORD_HASHER_ROUNDS == 6


def test_get_settings_uses_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("APP_DEBUG", "false")
    monkeypatch.setenv("APP_JWT_SECRET", "test-secret")

    first = get_settings()
    second = get_settings()

    assert first is second


def test_get_settings_reflects_new_env_after_cache_clear(monkeypatch: pytest.MonkeyPatch) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("APP_NAME", "name-a")
    monkeypatch.setenv("APP_JWT_SECRET", "test-secret-a")
    settings_a = get_settings()

    get_settings.cache_clear()
    monkeypatch.setenv("APP_NAME", "name-b")
    monkeypatch.setenv("APP_JWT_SECRET", "test-secret-b")
    settings_b = get_settings()

    assert settings_a.NAME == "name-a"
    assert settings_b.NAME == "name-b"
