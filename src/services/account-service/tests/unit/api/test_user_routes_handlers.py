from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from account_service.api.routes.user import create_user, delete_user, list_users, update_user
from account_service.api.schemas import CreateUserRequest, UpdateUserRequest
from account_service.application.schemas import UserDTO


pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


@dataclass
class FakeUsersUseCase:
    list_result: list[UserDTO] = field(default_factory=list)
    create_result: UserDTO | None = None
    update_result: UserDTO | None = None
    delete_calls: list[str] = field(default_factory=list)

    async def list(self):
        return self.list_result

    async def create(self, dto):
        self.created_dto = dto
        return self.create_result

    async def delete(self, dto):
        self.delete_calls.append(dto.user_id)

    async def update(self, dto):
        self.updated_dto = dto
        return self.update_result


@dataclass
class FakeContainer:
    users: FakeUsersUseCase


def _user_dto(user_id: str = "31cb2264-07a5-4d53-a758-05476fd48341") -> UserDTO:
    return UserDTO(
        id=user_id,
        name="Alice",
        email="alice@example.com",
        is_active=True,
        created_at="2024-01-01T00:00:00+00:00",
        updated_at="2024-01-01T00:00:00+00:00",
    )


async def test_list_users_maps_user_dtos_to_response_models() -> None:
    use_case = FakeUsersUseCase(list_result=[_user_dto()])
    container = FakeContainer(users=use_case)

    response = await list_users("trace-id", container)

    assert len(response) == 1
    assert response[0].email == "alice@example.com"


async def test_create_user_builds_dto_and_returns_response() -> None:
    use_case = FakeUsersUseCase(create_result=_user_dto())
    container = FakeContainer(users=use_case)
    request = CreateUserRequest(name="Alice", email="alice@example.com", password="password-123")

    response = await create_user(request, "trace-id", container)

    assert response.name == "Alice"
    assert use_case.created_dto.email == "alice@example.com"


async def test_delete_user_builds_delete_dto() -> None:
    use_case = FakeUsersUseCase()
    container = FakeContainer(users=use_case)
    user_id = "31cb2264-07a5-4d53-a758-05476fd48341"

    await delete_user(user_id, "trace-id", container)

    assert use_case.delete_calls == [user_id]


async def test_update_user_builds_update_dto_and_returns_response() -> None:
    use_case = FakeUsersUseCase(update_result=_user_dto())
    container = FakeContainer(users=use_case)
    user_id = "31cb2264-07a5-4d53-a758-05476fd48341"

    response = await update_user(user_id, UpdateUserRequest(name="Alice Updated"), "trace-id", container)

    assert response.name == "Alice"
    assert use_case.updated_dto.user_id == user_id
    assert use_case.updated_dto.name == "Alice Updated"
