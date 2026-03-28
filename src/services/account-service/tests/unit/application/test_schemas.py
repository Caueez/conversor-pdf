from __future__ import annotations

import pytest

from account_service.application.schemas import CreateUserDTO, DeleteUserDTO, UpdateUserDTO, UserDTO


pytestmark = pytest.mark.unit


def test_application_schema_models_roundtrip() -> None:
    create = CreateUserDTO(name="Alice", email="alice@example.com", password="password-123")
    delete = DeleteUserDTO(user_id="31cb2264-07a5-4d53-a758-05476fd48341")
    update = UpdateUserDTO(user_id=delete.user_id, name="Alice Updated")
    user = UserDTO(
        id=delete.user_id,
        name=create.name,
        email=create.email,
        is_active=True,
        created_at="2024-01-01T00:00:00+00:00",
        updated_at="2024-01-01T00:00:00+00:00",
    )

    assert create.name == "Alice"
    assert delete.user_id == user.id
    assert update.name == "Alice Updated"
    assert user.email == "alice@example.com"
