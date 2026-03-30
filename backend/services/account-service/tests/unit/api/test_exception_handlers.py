from __future__ import annotations

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from account_service.api.exception_handlers import register_exception_handlers
from account_service.domain.exceptions import (
    AuthenticationDomainError,
    AuthorizationDomainError,
    ConflictDomainError,
    ValidationDomainError,
)


pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


def _build_test_app() -> FastAPI:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/validation")
    async def validation_error() -> None:
        raise ValidationDomainError("validation failed")

    @app.get("/conflict")
    async def conflict_error() -> None:
        raise ConflictDomainError("conflict happened")

    @app.get("/authentication")
    async def authentication_error() -> None:
        raise AuthenticationDomainError("auth required")

    @app.get("/authorization")
    async def authorization_error() -> None:
        raise AuthorizationDomainError("forbidden")

    @app.get("/value")
    async def value_error() -> None:
        raise ValueError("invalid")

    @app.get("/unexpected")
    async def unexpected_error() -> None:
        raise RuntimeError("boom")

    return app


async def test_domain_validation_maps_to_422() -> None:
    app = _build_test_app()
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/validation")

    assert response.status_code == 422
    assert response.json() == {"message": "validation failed"}


async def test_domain_conflict_maps_to_409() -> None:
    app = _build_test_app()
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/conflict")

    assert response.status_code == 409
    assert response.json() == {"message": "conflict happened"}


async def test_domain_authentication_maps_to_401() -> None:
    app = _build_test_app()
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/authentication")

    assert response.status_code == 401
    assert response.json() == {"message": "auth required"}


async def test_domain_authorization_maps_to_403() -> None:
    app = _build_test_app()
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/authorization")

    assert response.status_code == 403
    assert response.json() == {"message": "forbidden"}


async def test_value_error_maps_to_400() -> None:
    app = _build_test_app()
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/value")

    assert response.status_code == 400
    assert response.json() == {"message": "Invalid request data"}


async def test_unexpected_exception_maps_to_500() -> None:
    app = _build_test_app()
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/unexpected")

    assert response.status_code == 500
    assert response.json() == {"message": "Internal server error"}
