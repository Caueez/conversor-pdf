from __future__ import annotations

import pytest

from account_service.api.app import create_app
from account_service.api.routes.routers import build_routers


pytestmark = pytest.mark.unit


def test_build_routers_includes_user_routes() -> None:
    router = build_routers()
    route_paths = {route.path for route in router.routes}
    assert "/session/register" in route_paths
    assert "/session/login" in route_paths
    assert "/session/admin/login" in route_paths
    assert "/session/refresh" in route_paths
    assert "/session/logout" in route_paths
    assert "/session/me" in route_paths
    assert "/" in route_paths
    assert "/{user_id}" in route_paths


def test_create_app_registers_routes_and_title() -> None:
    app = create_app()
    route_paths = {route.path for route in app.routes}
    openapi = app.openapi()

    assert app.title == "Conversor de PDF"
    assert "/session/register" in route_paths
    assert "/session/login" in route_paths
    assert "/session/admin/login" in route_paths
    assert "/session/refresh" in route_paths
    assert "/session/logout" in route_paths
    assert "/session/me" in route_paths
    assert "/" in route_paths
    assert "/{user_id}" in route_paths
    assert "securitySchemes" in openapi["components"]
    assert "BearerAuth" in openapi["components"]["securitySchemes"]
