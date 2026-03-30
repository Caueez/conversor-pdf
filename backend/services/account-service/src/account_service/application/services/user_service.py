from __future__ import annotations

from typing import Sequence
from uuid import UUID

from account_service.application.interfaces.hasher import PasswordHasherPort
from account_service.application.interfaces.repository import UserRepositoryPort
from account_service.application.schemas import CreateUserDTO, DeleteUserDTO, LoginDTO, UpdateUserDTO
from account_service.application.services.authorization_service import AuthorizationService
from account_service.domain.entities.user import User
from account_service.domain.entities.role import ROLE_KEY_ADMIN
from account_service.domain.exceptions import ConflictDomainError, ValidationDomainError
from account_service.domain.value_objects.user import Email, Password, Role
from account_service.shared.typed import utc_now


class UserService:
    def __init__(
        self,
        user_repository: UserRepositoryPort,
        password_hasher: PasswordHasherPort,
        authorization_service: AuthorizationService,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._authorization_service = authorization_service

    async def create(self, dto: CreateUserDTO) -> User:
        Email(dto.email)
        Password(dto.password)
        Role(dto.role)
        role = await self._authorization_service.get_role_by_key(dto.role)
        if not role:
            raise ValidationDomainError("Role is not valid")

        existing = await self._user_repository.get_by_email(dto.email)
        if existing:
            raise ConflictDomainError("Email already in use")

        password_hash = self._password_hasher.hash(dto.password)
        user = User(
            name=dto.name,
            email=dto.email,
            password_hash=password_hash,
            role=role.key,
        )
        return await self._user_repository.create(user)

    async def list(self) -> Sequence[User]:
        return await self._user_repository.list()

    async def delete(self, dto: DeleteUserDTO) -> None:
        user_id = UUID(dto.user_id)
        existing = await self._user_repository.get(user_id)
        if not existing:
            raise ConflictDomainError("User not found")

        await self._user_repository.delete(user_id)

    async def update(self, dto: UpdateUserDTO) -> User:
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
            email = dto.email

        password_hash = existing.password_hash
        if dto.password:
            Password(dto.password)
            password_hash = self._password_hasher.hash(dto.password)

        user = User(
            id=existing.id,
            name=name,
            email=email,
            password_hash=password_hash,
            role=existing.role,
            created_at=existing.created_at,
            updated_at=utc_now(),
        )

        return await self._user_repository.update(user)

    async def authenticate(self, dto: LoginDTO) -> User | None:
        user = await self._user_repository.get_by_email(dto.email)
        if not user:
            return None

        if not self._password_hasher.check(dto.password, user.password_hash):
            return None

        return user

    async def get_active_by_id(self, user_id: UUID) -> User | None:
        user = await self._user_repository.get(user_id)
        if not user or not user.is_active:
            return None
        return user

    async def is_admin(self, user_id: UUID) -> bool:
        user = await self.get_active_by_id(user_id)
        return bool(user and user.role == ROLE_KEY_ADMIN)
