
from typing import Sequence
from uuid import UUID

from account_service.domain.entities.user import User
from account_service.domain.value_objects.user import Email, PasswordHash
from account_service.application.interfaces.repository import UserRepositoryPort

from account_service.application.schemas import CreateUserDTO, DeleteUserDTO, UserDTO, UpdateUserDTO

from account_service.domain.exceptions import (
    ConflictDomainError
)

from account_service.shared.typed import utc_now

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
    
    async def delete(self, dto: DeleteUserDTO) -> None:
        user_id = UUID(dto.user_id)
        existing = await self._user_repository.get(user_id)
        if not existing:
            raise ConflictDomainError("User not found")
        
        await self._user_repository.delete(user_id)
    
    async def update(self, dto: UpdateUserDTO):
        user_id = UUID(dto.user_id)
        existing = await self._user_repository.get(user_id)
        if not existing:
            raise ConflictDomainError("User not found")
        
        user = User(
            id=existing.id,
            name=dto.name if dto.name else existing.name,
            email=dto.email if dto.email else existing.email,
            password_hash=PasswordHash.from_plain(dto.password).value if dto.password else existing.password_hash,
            created_at=existing.created_at,
            updated_at=utc_now()
        )

        return await self._user_repository.update(user)
