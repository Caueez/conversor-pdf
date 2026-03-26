from typing import Any, TypeVar

from pydantic import BaseModel

from account_service.api.schemas import UserResponse

TModel = TypeVar("TModel", bound=BaseModel)


def dto_to_user_response(dto: BaseModel) -> UserResponse: 
    return UserResponse.model_validate(dto.model_dump())


def request_to_dto(dto_cls: type[TModel], /, **kwargs: Any) -> TModel:
    return dto_cls(**kwargs)
