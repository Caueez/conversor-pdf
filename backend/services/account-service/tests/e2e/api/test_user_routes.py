from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.factories.users import make_create_user_payload, make_unique_email, make_update_user_payload


pytestmark = [pytest.mark.e2e, pytest.mark.asyncio]


def _assert_user_response_shape(payload: dict[str, object]) -> None:
    assert set(payload.keys()) == {
        "id",
        "name",
        "email",
        "is_active",
        "created_at",
        "updated_at",
    }


async def _auth_headers(client: AsyncClient) -> dict[str, str]:
    login_response = await client.post(
        "/session/login",
        json={"email": "admin@example.com", "password": "password-123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def _non_admin_auth(client: AsyncClient) -> tuple[dict[str, str], str]:
    email = make_unique_email("common")
    register_response = await client.post(
        "/session/register",
        json={"name": "Common User", "email": email, "password": "password-123"},
    )
    assert register_response.status_code == 201

    headers = {"Authorization": f"Bearer {register_response.json()['access_token']}"}
    me_response = await client.get("/session/me", headers=headers)
    assert me_response.status_code == 200

    return headers, me_response.json()["id"]


@pytest.mark.contract
@pytest.mark.smoke
async def test_create_user_returns_contract_shape(app_client: AsyncClient) -> None:
    headers = await _auth_headers(app_client)
    payload = make_create_user_payload()

    response = await app_client.post("/", json=payload, headers=headers)

    assert response.status_code == 201
    body = response.json()
    _assert_user_response_shape(body)
    assert body["name"] == payload["name"]
    assert body["email"] == payload["email"]


@pytest.mark.contract
@pytest.mark.smoke
async def test_get_users_returns_contract_shape(app_client: AsyncClient) -> None:
    headers = await _auth_headers(app_client)
    payload = make_create_user_payload()
    await app_client.post("/", json=payload, headers=headers)

    response = await app_client.get("/", headers=headers)

    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert any(user["email"] == payload["email"] for user in users)
    _assert_user_response_shape(users[0])


@pytest.mark.contract
@pytest.mark.smoke
async def test_delete_user_returns_204_without_body(app_client: AsyncClient) -> None:
    headers = await _auth_headers(app_client)
    payload = make_create_user_payload()
    create_response = await app_client.post("/", json=payload, headers=headers)
    user_id = create_response.json()["id"]

    delete_response = await app_client.delete(f"/{user_id}", headers=headers)

    assert delete_response.status_code == 204
    assert delete_response.text == ""


@pytest.mark.contract
async def test_patch_user_returns_contract_shape(app_client: AsyncClient) -> None:
    headers = await _auth_headers(app_client)
    payload = make_create_user_payload()
    create_response = await app_client.post("/", json=payload, headers=headers)
    user_id = create_response.json()["id"]

    patch_response = await app_client.patch(
        f"/{user_id}",
        json=make_update_user_payload(name="Updated Name"),
        headers=headers,
    )

    assert patch_response.status_code == 200
    body = patch_response.json()
    _assert_user_response_shape(body)
    assert body["name"] == "Updated Name"


async def test_user_endpoints_require_authentication(app_client: AsyncClient) -> None:
    payload = make_create_user_payload()

    response = await app_client.post("/", json=payload)

    assert response.status_code == 401
    assert response.json() == {"message": "Authentication required"}


async def test_non_admin_cannot_access_user_management_endpoints(app_client: AsyncClient) -> None:
    headers, user_id = await _non_admin_auth(app_client)

    list_response = await app_client.get("/", headers=headers)
    create_response = await app_client.post("/", json=make_create_user_payload(), headers=headers)
    patch_response = await app_client.patch(
        f"/{user_id}",
        json=make_update_user_payload(name="Updated Name"),
        headers=headers,
    )
    delete_response = await app_client.delete(f"/{user_id}", headers=headers)

    for response in (list_response, create_response, patch_response, delete_response):
        assert response.status_code == 403
        assert response.json() == {"message": "Admin privileges are required"}


async def test_duplicate_email_returns_409(app_client: AsyncClient) -> None:
    headers = await _auth_headers(app_client)
    payload = make_create_user_payload(email=make_unique_email("dup"))
    await app_client.post("/", json=payload, headers=headers)

    response = await app_client.post("/", json=payload, headers=headers)

    assert response.status_code == 409
    assert response.json() == {"message": "Email already in use"}


async def test_create_user_with_invalid_domain_email_returns_422(app_client: AsyncClient) -> None:
    headers = await _auth_headers(app_client)
    payload = make_create_user_payload(email="invalid-email")

    response = await app_client.post("/", json=payload, headers=headers)

    assert response.status_code == 422
    assert response.json() == {"message": "Email is not valid"}


async def test_delete_with_invalid_uuid_returns_400(app_client: AsyncClient) -> None:
    headers = await _auth_headers(app_client)

    response = await app_client.delete("/invalid-uuid", headers=headers)

    assert response.status_code == 400
    assert response.json() == {"message": "Invalid request data"}


async def test_delete_missing_user_returns_409(app_client: AsyncClient) -> None:
    headers = await _auth_headers(app_client)

    response = await app_client.delete("/5b026afe-7b66-4a0b-9322-b9726a2120f2", headers=headers)

    assert response.status_code == 409
    assert response.json() == {"message": "User not found"}


async def test_patch_requires_at_least_one_field(app_client: AsyncClient) -> None:
    headers = await _auth_headers(app_client)
    payload = make_create_user_payload()
    create_response = await app_client.post("/", json=payload, headers=headers)
    user_id = create_response.json()["id"]

    response = await app_client.patch(f"/{user_id}", json={}, headers=headers)

    assert response.status_code == 422


async def test_patch_email_should_update_email_field(app_client: AsyncClient) -> None:
    headers = await _auth_headers(app_client)
    payload = make_create_user_payload(email=make_unique_email("before-email"))
    create_response = await app_client.post("/", json=payload, headers=headers)
    user_id = create_response.json()["id"]
    updated_email = make_unique_email("after-email")

    response = await app_client.patch(
        f"/{user_id}",
        json=make_update_user_payload(email=updated_email),
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["email"] == updated_email
