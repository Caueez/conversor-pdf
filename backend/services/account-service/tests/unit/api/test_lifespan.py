from __future__ import annotations

from dataclasses import dataclass

import pytest
from fastapi import FastAPI

import account_service.api.lifespan as lifespan_module
from account_service.api.lifespan import lifespan
from account_service.settings import AccountSettings


pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


@dataclass
class FakeContainer:
    startup_called: bool = False
    shutdown_called: bool = False

    async def startup(self) -> None:
        self.startup_called = True

    async def shutdown(self) -> None:
        self.shutdown_called = True


async def test_lifespan_builds_container_and_manages_lifecycle(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_container = FakeContainer()
    fake_settings = AccountSettings(DEBUG=False, JWT_SECRET="test-secret")
    captured_level: dict[str, int] = {}

    monkeypatch.setattr(lifespan_module, "get_settings", lambda: fake_settings)
    monkeypatch.setattr(lifespan_module.ContainerService, "build", classmethod(lambda cls, settings: fake_container))

    def fake_setup_logging(level: int) -> None:
        captured_level["value"] = level

    monkeypatch.setattr(lifespan_module, "setup_logging", fake_setup_logging)
    app = FastAPI()

    async with lifespan(app):
        assert app.state.container is fake_container
        assert fake_container.startup_called is True

    assert fake_container.shutdown_called is True
    assert "value" in captured_level
