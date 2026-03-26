from typing import Sequence
from uuid import UUID

from account_service.application.schemas import CreateUserDTO, DeleteUserDTO, UserDTO, UpdateUserDTO
from account_service.application.interfaces.repository import UserRepositoryPort
from account_service.domain.entities.user import User
from account_service.domain.exceptions import ConflictDomainError
from account_service.domain.value_objects.user import Email, Password
from account_service.shared.typed import utc_now

from account_service.application.interfaces.hasher import PasswordHasherPort


class UserUseCase:
    def __init__(self, user_repository: UserRepositoryPort, password_hasher: PasswordHasherPort) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def create(self, dto: CreateUserDTO) -> UserDTO:
        Email(dto.email)
        Password(dto.password)
        existing = await self._user_repository.get_by_email(dto.email)
        if existing:
            raise ConflictDomainError("Email already in use")
        
        password_hash: str = self._password_hasher.hash(dto.password)

        user = User(
            name=dto.name,
            email=dto.email,
            password_hash=password_hash,
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

    async def update(self, dto: UpdateUserDTO) -> UserDTO:
        user_id = UUID(dto.user_id)
        existing = await self._user_repository.get(user_id)
        if not existing:
            raise ConflictDomainError("User not found")
        name = existing.name
        if dto.name:
            name = dto.name

        email = existing.email
        if dto.email:
            Email(dto.email)
            user_with_same_email = await self._user_repository.get_by_email(dto.email)
            if user_with_same_email and str(user_with_same_email.id) != str(existing.id):
                raise ConflictDomainError("Email already in use")
        
        password_hash = existing.password_hash
        if dto.password:
            Password(dto.password)
            password_hash = self._password_hasher.hash(dto.password)


        user = User(
            id=existing.id,
            name=name,
            email=email,
            password_hash=password_hash,
            created_at=existing.created_at,
            updated_at=utc_now(),
        )

        updated_user = await self._user_repository.update(user)
        return UserDTO.model_validate(updated_user.to_dict())
