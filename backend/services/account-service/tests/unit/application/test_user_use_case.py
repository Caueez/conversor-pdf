from __future__ import annotations

from datetime import UTC, datetime
from typing import Sequence
from uuid import UUID

import pytest

import account_service.application.services.user_service as user_service_module
from account_service.application.schemas import CreateUserDTO, DeleteUserDTO, UpdateUserDTO
from account_service.application.services.authorization_service import AuthorizationService
from account_service.application.services.user_service import UserService
from account_service.application.use_cases.users import UserUseCase
from account_service.domain.entities.role import ROLE_KEY_ADMIN, ROLE_KEY_USER, Role
from account_service.domain.entities.user import User
from account_service.domain.exceptions import ConflictDomainError, ValidationDomainError
from tests.factories.users import make_unique_email, make_user_entity


pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


class InMemoryUserRepo:
    def __init__(self, users: Sequence[User] | None = None) -> None:
        self._users: dict[str, User] = {}
        for user in users or []:
            self._users[str(user.id)] = user

    async def create(self, user: User) -> User:
        self._users[str(user.id)] = user
        return user

    async def get(self, user_id: UUID) -> User | None:
        return self._users.get(str(user_id))

    async def get_by_email(self, email: str) -> User | None:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    async def list(self) -> Sequence[User]:
        return list(self._users.values())

    async def update(self, user: User) -> User:
        self._users[str(user.id)] = user
        return user

    async def delete(self, user_id: UUID) -> None:
        self._users.pop(str(user_id), None)


class FakeHasher:
    def __init__(self) -> None:
        self.hash_calls: list[str] = []

    def hash(self, password: str) -> str:
        self.hash_calls.append(password)
        return f"hashed::{password}"

    def check(self, password: str, hashed_password: str) -> bool:
        return hashed_password == f"hashed::{password}"


class InMemoryAuthorizationRepo:
    async def ensure_defaults(self) -> None:
        return None

    async def get_role_by_key(self, key: str) -> Role | None:
        if key == ROLE_KEY_ADMIN:
            return Role(key=ROLE_KEY_ADMIN, name="Administrator")
        if key == ROLE_KEY_USER:
            return Role(key=ROLE_KEY_USER, name="User")
        return None

    async def get_permission_by_key(self, key: str):
        return None

    async def role_has_permission(self, role_key: str, permission_key: str) -> bool:
        return False


def build_use_case(users: Sequence[User] | None = None) -> tuple[UserUseCase, InMemoryUserRepo, FakeHasher]:
    repo = InMemoryUserRepo(users=users)
    hasher = FakeHasher()
    authorization_service = AuthorizationService(InMemoryAuthorizationRepo())
    user_service = UserService(repo, hasher, authorization_service)
    return UserUseCase(user_service), repo, hasher


async def test_create_user_success() -> None:
    use_case, _, hasher = build_use_case()
    dto = CreateUserDTO(name="Alice", email=make_unique_email("create"), password="password-123")

    created = await use_case.create(dto)

    assert created.name == "Alice"
    assert created.email == dto.email
    assert hasher.hash_calls == ["password-123"]


async def test_create_user_raises_conflict_when_email_already_exists() -> None:
    existing = make_user_entity(email=make_unique_email("dup"))
    use_case, _, _ = build_use_case(users=[existing])
    dto = CreateUserDTO(name="Alice", email=existing.email, password="password-123")

    with pytest.raises(ConflictDomainError, match="Email already in use"):
        await use_case.create(dto)


async def test_create_user_rejects_invalid_email() -> None:
    use_case, _, _ = build_use_case()
    dto = CreateUserDTO(name="Alice", email="invalid-email", password="password-123")

    with pytest.raises(ValidationDomainError, match="Email is not valid"):
        await use_case.create(dto)


async def test_create_user_rejects_invalid_password() -> None:
    use_case, _, _ = build_use_case()
    dto = CreateUserDTO(name="Alice", email=make_unique_email("pwd"), password="short")

    with pytest.raises(ValidationDomainError, match="at least 8"):
        await use_case.create(dto)


async def test_list_returns_user_dtos() -> None:
    users = [make_user_entity(name="A"), make_user_entity(name="B")]
    use_case, _, _ = build_use_case(users=users)

    listed = await use_case.list()

    assert [item.name for item in listed] == ["A", "B"]


async def test_delete_existing_user() -> None:
    existing = make_user_entity()
    use_case, repo, _ = build_use_case(users=[existing])

    await use_case.delete(DeleteUserDTO(user_id=str(existing.id)))

    assert await repo.get(UUID(str(existing.id))) is None


async def test_delete_raises_when_user_not_found() -> None:
    use_case, _, _ = build_use_case()

    with pytest.raises(ConflictDomainError, match="User not found"):
        await use_case.delete(DeleteUserDTO(user_id="5b026afe-7b66-4a0b-9322-b9726a2120f2"))


async def test_delete_invalid_uuid_raises_value_error() -> None:
    use_case, _, _ = build_use_case()

    with pytest.raises(ValueError):
        await use_case.delete(DeleteUserDTO(user_id="invalid-uuid"))


async def test_update_raises_when_user_not_found() -> None:
    use_case, _, _ = build_use_case()

    with pytest.raises(ConflictDomainError, match="User not found"):
        await use_case.update(UpdateUserDTO(user_id="5b026afe-7b66-4a0b-9322-b9726a2120f2", name="new"))


async def test_update_name_only_keeps_email_and_password(monkeypatch: pytest.MonkeyPatch) -> None:
    base_time = datetime(2024, 1, 1, tzinfo=UTC)
    next_time = datetime(2024, 2, 1, tzinfo=UTC)
    existing = make_user_entity(
        name="Before",
        email=make_unique_email("before"),
        password_hash="hashed::old",
        created_at=base_time,
        updated_at=base_time,
    )
    use_case, _, _ = build_use_case(users=[existing])
    monkeypatch.setattr(user_service_module, "utc_now", lambda: next_time)

    updated = await use_case.update(UpdateUserDTO(user_id=str(existing.id), name="After"))

    assert updated.name == "After"
    assert updated.email == existing.email
    assert updated.updated_at == next_time.isoformat()


async def test_update_password_hashes_new_password(monkeypatch: pytest.MonkeyPatch) -> None:
    base_time = datetime(2024, 1, 1, tzinfo=UTC)
    next_time = datetime(2024, 2, 1, tzinfo=UTC)
    existing = make_user_entity(password_hash="hashed::old", created_at=base_time, updated_at=base_time)
    use_case, repo, hasher = build_use_case(users=[existing])
    monkeypatch.setattr(user_service_module, "utc_now", lambda: next_time)

    await use_case.update(UpdateUserDTO(user_id=str(existing.id), password="new-password-123"))
    persisted = await repo.get(UUID(str(existing.id)))

    assert hasher.hash_calls == ["new-password-123"]
    assert persisted is not None
    assert persisted.password_hash == "hashed::new-password-123"


async def test_update_raises_conflict_when_target_email_belongs_to_another_user() -> None:
    existing = make_user_entity(email=make_unique_email("existing"))
    another = make_user_entity(email=make_unique_email("another"))
    use_case, _, _ = build_use_case(users=[existing, another])

    with pytest.raises(ConflictDomainError, match="Email already in use"):
        await use_case.update(UpdateUserDTO(user_id=str(existing.id), email=another.email))


async def test_update_allows_same_email_for_same_user() -> None:
    existing = make_user_entity(email=make_unique_email("same-email"))
    use_case, _, _ = build_use_case(users=[existing])

    updated = await use_case.update(UpdateUserDTO(user_id=str(existing.id), email=existing.email))

    assert updated.email == existing.email


async def test_update_email_should_change_email_value() -> None:
    existing = make_user_entity(email=make_unique_email("before-email"))
    use_case, _, _ = build_use_case(users=[existing])
    new_email = make_unique_email("after-email")

    updated = await use_case.update(UpdateUserDTO(user_id=str(existing.id), email=new_email))

    assert updated.email == new_email
