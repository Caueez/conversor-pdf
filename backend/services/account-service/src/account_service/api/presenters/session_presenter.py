from pydantic import BaseModel

from account_service.api.schemas import TokenPairResponse


def dto_to_token_pair_response(dto: BaseModel) -> TokenPairResponse:
    return TokenPairResponse.model_validate(dto.model_dump())
