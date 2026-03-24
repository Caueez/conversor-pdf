
from typing import Protocol, Sequence

from account_service.domain.entities.user import User

from uuid import UUID


class UserRepositoryPort(Protocol):
    async def create(self, user: User) -> User: ...

    async def get(self, user_id: UUID) -> User | None: ...

    async def get_by_email(self, email: str) -> User | None: ...

    async def list(self) -> Sequence[User]: ...

    async def update(self, user: User) -> User: ...

    async def delete(self, user_id: UUID) -> None: ...