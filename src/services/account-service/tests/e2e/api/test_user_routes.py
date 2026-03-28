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


@pytest.mark.contract
@pytest.mark.smoke
async def test_create_user_returns_contract_shape(app_client: AsyncClient) -> None:
    payload = make_create_user_payload()

    response = await app_client.post("/", json=payload)

    assert response.status_code == 201
    body = response.json()
    _assert_user_response_shape(body)
    assert body["name"] == payload["name"]
    assert body["email"] == payload["email"]


@pytest.mark.contract
@pytest.mark.smoke
async def test_get_users_returns_contract_shape(app_client: AsyncClient) -> None:
    payload = make_create_user_payload()
    await app_client.post("/", json=payload)

    response = await app_client.get("/")

    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) == 1
    _assert_user_response_shape(users[0])


@pytest.mark.contract
@pytest.mark.smoke
async def test_delete_user_returns_204_without_body(app_client: AsyncClient) -> None:
    payload = make_create_user_payload()
    create_response = await app_client.post("/", json=payload)
    user_id = create_response.json()["id"]

    delete_response = await app_client.delete(f"/{user_id}")

    assert delete_response.status_code == 204
    assert delete_response.text == ""


@pytest.mark.contract
async def test_patch_user_returns_contract_shape(app_client: AsyncClient) -> None:
    payload = make_create_user_payload()
    create_response = await app_client.post("/", json=payload)
    user_id = create_response.json()["id"]

    patch_response = await app_client.patch(f"/{user_id}", json=make_update_user_payload(name="Updated Name"))

    assert patch_response.status_code == 200
    body = patch_response.json()
    _assert_user_response_shape(body)
    assert body["name"] == "Updated Name"


async def test_duplicate_email_returns_409(app_client: AsyncClient) -> None:
    payload = make_create_user_payload(email=make_unique_email("dup"))
    await app_client.post("/", json=payload)

    response = await app_client.post("/", json=payload)

    assert response.status_code == 409
    assert response.json() == {"message": "Email already in use"}


async def test_create_user_with_invalid_domain_email_returns_422(app_client: AsyncClient) -> None:
    payload = make_create_user_payload(email="invalid-email")

    response = await app_client.post("/", json=payload)

    assert response.status_code == 422
    assert response.json() == {"message": "Email is not valid"}


async def test_delete_with_invalid_uuid_returns_400(app_client: AsyncClient) -> None:
    response = await app_client.delete("/invalid-uuid")

    assert response.status_code == 400
    assert response.json() == {"message": "Invalid request data"}


async def test_delete_missing_user_returns_409(app_client: AsyncClient) -> None:
    response = await app_client.delete("/5b026afe-7b66-4a0b-9322-b9726a2120f2")

    assert response.status_code == 409
    assert response.json() == {"message": "User not found"}


async def test_patch_requires_at_least_one_field(app_client: AsyncClient) -> None:
    payload = make_create_user_payload()
    create_response = await app_client.post("/", json=payload)
    user_id = create_response.json()["id"]

    response = await app_client.patch(f"/{user_id}", json={})

    assert response.status_code == 422


@pytest.mark.xfail(
    strict=True,
    reason="Bug rastreado em src/services/account-service/docs/tasks/task-002-correcao-de-update-de-email-no-user-use-case.md",
)
async def test_patch_email_should_update_email_field(app_client: AsyncClient) -> None:
    payload = make_create_user_payload(email=make_unique_email("before-email"))
    create_response = await app_client.post("/", json=payload)
    user_id = create_response.json()["id"]
    updated_email = make_unique_email("after-email")

    response = await app_client.patch(f"/{user_id}", json=make_update_user_payload(email=updated_email))

    assert response.status_code == 200
    assert response.json()["email"] == updated_email
