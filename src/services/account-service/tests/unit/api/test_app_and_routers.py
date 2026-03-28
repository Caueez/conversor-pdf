from __future__ import annotations

import pytest

from account_service.api.app import create_app
from account_service.api.routes.routers import build_routers


pytestmark = pytest.mark.unit


def test_build_routers_includes_user_routes() -> None:
    router = build_routers()
    route_paths = {route.path for route in router.routes}
    assert "/" in route_paths
    assert "/{user_id}" in route_paths


def test_create_app_registers_routes_and_title() -> None:
    app = create_app()
    route_paths = {route.path for route in app.routes}

    assert app.title == "Conversor de PDF"
    assert "/" in route_paths
    assert "/{user_id}" in route_paths
