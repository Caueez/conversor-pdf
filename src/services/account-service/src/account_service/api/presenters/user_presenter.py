
from pydantic import BaseModel

from account_service.api.schemas import UserResponse



def dto_to_response(dto: BaseModel) -> BaseModel: 
    return UserResponse.model_validate(dto.model_dump())


def request_to_dto(request: BaseModel, dto_class: BaseModel) -> BaseModel:
    return dto_class.model_validate(request.model_dump())