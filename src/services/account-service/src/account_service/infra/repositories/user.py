

from typing import Sequence
from uuid import UUID

from infra.database.implementations.postgres import Postgres

from ...domain.entities.user import User
from account_service.application.interfaces.repository import UserRepositoryPort

from infra.database.shared import Query

from infra.database.shared import DatabaseRow

class UserRepo(UserRepositoryPort):
    def __init__(self, persistence: Postgres):
        self.db = persistence

    def _row_to_entity(self, row: DatabaseRow) -> User:
        return User(
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            id=row["id"],
            is_active=row["is_active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    async def create(self, user: User) -> User:
        query = Query("INSERT",
            """
            INSERT INTO users (id, name, email, password_hash, is_active, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            [user.id, user.name, user.email, user.password_hash, user.is_active, user.created_at, user.updated_at]
        )
        
        await self.db.execute(query)
        return user

    async def get(self, user_id: UUID) -> User | None:
        query = Query("SELECT",
            """
            SELECT id, name, email, password_hash, is_active, created_at, updated_at
            FROM users
            WHERE id = $1
            """,
            [str(user_id)]
        )

        record = await self.db.fetch_one(query)
        if not record:
            return
        return self._row_to_entity(record)
        

    async def get_by_email(self, email: str) -> User | None:
        query = Query("SELECT",
            """
            SELECT id, name, email, password_hash, is_active, created_at, updated_at
            FROM users
            WHERE email = $1
            """,
            [email]
        )

        record = await self.db.fetch_one(query)
        if not record:
            return
        return self._row_to_entity(record)

    async def list(self) -> Sequence[User]:
        query = Query("SELECT",
            """
            SELECT * FROM users
            """,
            []
        )

        records = await self.db.fetch_all(query)
        return [self._row_to_entity(record) for record in records]

    async def update(self, user: User) -> User:
        raise NotImplementedError

    async def delete(self, user_id: UUID) -> None:
        query = Query("DELETE",
            """
            DELETE FROM users
            WHERE id = $1
            """,
            [str(user_id)]
        )

        await self.db.execute(query)
