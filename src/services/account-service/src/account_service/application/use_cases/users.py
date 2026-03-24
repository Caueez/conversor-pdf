
from typing import Sequence

from account_service.domain.entities.user import User
from account_service.domain.value_objects.user import Email, PasswordHash
from account_service.application.interfaces.repository import UserRepositoryPort

from account_service.application.schemas import CreateUserDTO, UserDTO

from account_service.domain.exceptions import (
    ConflictDomainError
)


class UserUseCase:
    def __init__(
            self,
            user_repository: UserRepositoryPort
            ) -> None:
        
        self._user_repository = user_repository
    
    async def create(self, dto: CreateUserDTO) -> UserDTO:
        Email(dto.email)
        existing = await self._user_repository.get_by_email(dto.email)
        if existing:
            raise ConflictDomainError("Email aready using")
        
        user = User(
            name=dto.name,
            email=dto.email,
            password_hash=PasswordHash.from_plain(dto.password).value
        )

        user = await self._user_repository.create(user)

        return UserDTO.model_validate(user.to_dict())
    
    async def list(self) -> Sequence[UserDTO]:
        return [UserDTO.model_validate(user.to_dict()) for user in await self._user_repository.list()]
