from typing import Sequence

from account_service.application.schemas import CreateUserDTO, DeleteUserDTO, UpdateUserDTO, UserDTO
from account_service.application.services.user_service import UserService


class UserUseCase:
    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service

    async def create(self, dto: CreateUserDTO) -> UserDTO:
        user = await self._user_service.create(dto)
        return UserDTO.model_validate(user.to_dict())

    async def list(self) -> Sequence[UserDTO]:
        users = await self._user_service.list()
        return [UserDTO.model_validate(user.to_dict()) for user in users]

    async def delete(self, dto: DeleteUserDTO) -> None:
        await self._user_service.delete(dto)

    async def update(self, dto: UpdateUserDTO) -> UserDTO:
        updated_user = await self._user_service.update(dto)
        return UserDTO.model_validate(updated_user.to_dict())
