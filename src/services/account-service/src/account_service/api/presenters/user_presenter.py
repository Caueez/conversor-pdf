
from typing import Any

from pydantic import BaseModel

from account_service.api.schemas import UserResponse



def dto_to_user_response(dto: BaseModel) -> UserResponse: 
    return UserResponse.model_validate(dto.model_dump())


def request_to_dto(dto: BaseModel, /, **kwargs: dict[str, Any]) -> BaseModel:
    return dto(**kwargs)