from __future__ import annotations

import pytest
from httpx import AsyncClient


pytestmark = [pytest.mark.e2e, pytest.mark.asyncio]


def _assert_token_pair_shape(payload: dict[str, object]) -> None:
    assert set(payload.keys()) == {
        "access_token",
        "refresh_token",
        "token_type",
        "access_expires_at",
        "refresh_expires_at",
    }


async def _login(client: AsyncClient) -> dict[str, object]:
    response = await client.post(
        "/session/login",
        json={"email": "admin@example.com", "password": "password-123"},
    )
    assert response.status_code == 200
    return response.json()


async def _admin_login(client: AsyncClient) -> dict[str, object]:
    response = await client.post(
        "/session/admin/login",
        json={"email": "admin@example.com", "password": "password-123"},
    )
    assert response.status_code == 200
    return response.json()


async def _register(client: AsyncClient, *, email: str) -> dict[str, object]:
    response = await client.post(
        "/session/register",
        json={"name": "Register User", "email": email, "password": "password-123"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.mark.contract
@pytest.mark.smoke
async def test_login_returns_token_pair_contract_shape(app_client: AsyncClient) -> None:
    response = await app_client.post(
        "/session/login",
        json={"email": "admin@example.com", "password": "password-123"},
    )

    assert response.status_code == 200
    body = response.json()
    _assert_token_pair_shape(body)
    assert body["token_type"] == "bearer"


@pytest.mark.contract
async def test_admin_login_returns_token_pair_for_admin(app_client: AsyncClient) -> None:
    body = await _admin_login(app_client)
    _assert_token_pair_shape(body)
    assert body["token_type"] == "bearer"


async def test_admin_login_rejects_common_user_credentials(app_client: AsyncClient) -> None:
    email = "common-admin-login@example.com"
    await _register(app_client, email=email)

    response = await app_client.post(
        "/session/admin/login",
        json={"email": email, "password": "password-123"},
    )

    assert response.status_code == 403
    assert response.json() == {"message": "Admin credentials are required"}


@pytest.mark.contract
async def test_register_returns_token_pair_and_authenticates_user(app_client: AsyncClient) -> None:
    registered = await _register(app_client, email="register-user@example.com")
    _assert_token_pair_shape(registered)
    assert registered["token_type"] == "bearer"

    me_response = await app_client.get(
        "/session/me",
        headers={"Authorization": f"Bearer {registered['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "register-user@example.com"


async def test_login_with_invalid_credentials_returns_401(app_client: AsyncClient) -> None:
    response = await app_client.post(
        "/session/login",
        json={"email": "admin@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json() == {"message": "Invalid credentials"}


@pytest.mark.contract
async def test_me_returns_authenticated_user(app_client: AsyncClient) -> None:
    tokens = await _login(app_client)

    response = await app_client.get(
        "/session/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "admin@example.com"


@pytest.mark.contract
async def test_refresh_rotates_refresh_token(app_client: AsyncClient) -> None:
    tokens = await _login(app_client)

    refresh_response = await app_client.post(
        "/session/refresh",
        headers={"Authorization": f"Bearer {tokens['refresh_token']}"},
    )

    assert refresh_response.status_code == 200
    refreshed_body = refresh_response.json()
    _assert_token_pair_shape(refreshed_body)
    assert refreshed_body["refresh_token"] != tokens["refresh_token"]

    stale_response = await app_client.post(
        "/session/refresh",
        headers={"Authorization": f"Bearer {tokens['refresh_token']}"},
    )

    assert stale_response.status_code == 401
    assert stale_response.json() == {"message": "Invalid refresh token"}


@pytest.mark.contract
async def test_logout_revokes_current_session_immediately(app_client: AsyncClient) -> None:
    tokens = await _login(app_client)
    access_headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    logout_response = await app_client.post("/session/logout", headers=access_headers)

    assert logout_response.status_code == 204

    me_response = await app_client.get("/session/me", headers=access_headers)
    assert me_response.status_code == 401
    assert me_response.json() == {"message": "Session is not active"}


async def test_refresh_requires_bearer_header(app_client: AsyncClient) -> None:
    response = await app_client.post("/session/refresh")

    assert response.status_code == 401
    assert response.json() == {"message": "Authentication required"}
