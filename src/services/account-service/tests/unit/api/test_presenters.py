from __future__ import annotations

import pytest

from account_service.api.presenters.user_presenter import dto_to_user_response, request_to_dto
from account_service.api.schemas import UserResponse
from account_service.application.schemas import CreateUserDTO, UserDTO


pytestmark = pytest.mark.unit


def test_request_to_dto_builds_requested_model() -> None:
    dto = request_to_dto(
        CreateUserDTO,
        name="Alice",
        email="alice@example.com",
        password="password-123",
    )
    assert isinstance(dto, CreateUserDTO)
    assert dto.email == "alice@example.com"


def test_dto_to_user_response_maps_expected_fields() -> None:
    user_dto = UserDTO(
        id="31cb2264-07a5-4d53-a758-05476fd48341",
        name="Alice",
        email="alice@example.com",
        is_active=True,
        created_at="2024-01-01T00:00:00+00:00",
        updated_at="2024-01-01T00:00:00+00:00",
    )

    response = dto_to_user_response(user_dto)

    assert isinstance(response, UserResponse)
    assert response.model_dump() == user_dto.model_dump()
