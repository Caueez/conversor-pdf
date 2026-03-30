
from typing import Sequence
from uuid import UUID

from infra.database.implementations.postgres import Postgres

from ...domain.entities.user import User
from ...domain.entities.role import ROLE_KEY_USER
from account_service.application.interfaces.repository import UserRepositoryPort

from infra.database.shared import DatabaseRow, Query


class PostgresUserRepoAdapter(UserRepositoryPort):
    def __init__(self, persistence: Postgres):
        self._db = persistence

    def _row_to_entity(self, row: DatabaseRow) -> User:
        return User(
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            role=row["role"] or ROLE_KEY_USER,
            id=row["id"],
            is_active=row["is_active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    async def create(self, user: User) -> User:
        query = Query.create(
            "INSERT",
            """
            INSERT INTO users (id, name, email, password_hash, role, is_active, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
            [
                user.id,
                user.name,
                user.email,
                user.password_hash,
                user.role,
                user.is_active,
                user.created_at,
                user.updated_at,
            ],
        )

        await self._db.execute(query)
        return user

    async def get(self, user_id: UUID) -> User | None:
        query = Query.create(
            "SELECT",
            """
            SELECT id, name, email, password_hash, role, is_active, created_at, updated_at
            FROM users
            WHERE id = $1
            """,
            [str(user_id)],
        )

        record = await self._db.fetch_one(query)
        if not record:
            return None
        return self._row_to_entity(record)

    async def get_by_email(self, email: str) -> User | None:
        query = Query.create(
            "SELECT",
            """
            SELECT id, name, email, password_hash, role, is_active, created_at, updated_at
            FROM users
            WHERE email = $1
            """,
            [email],
        )

        record = await self._db.fetch_one(query)
        if not record:
            return None
        return self._row_to_entity(record)

    async def list(self) -> Sequence[User]:
        query = Query.create(
            "SELECT",
            """
            SELECT * FROM users
            """,
            [],
        )

        records = await self._db.fetch_all(query)
        return [self._row_to_entity(record) for record in records]

    async def update(self, user: User) -> User:
        query = Query.create(
            "UPDATE",
            """
            UPDATE users
            SET name = $1, email = $2, password_hash = $3, role = $4, is_active = $5, updated_at = $6
            WHERE id = $7
            """,
            [
                user.name,
                user.email,
                user.password_hash,
                user.role,
                user.is_active,
                user.updated_at,
                user.id,
            ],
        )

        await self._db.execute(query)
        return user

    async def delete(self, user_id: UUID) -> None:
        query = Query.create(
            "DELETE",
            """
            DELETE FROM users
            WHERE id = $1
            """,
            [str(user_id)],
        )

        await self._db.execute(query)
