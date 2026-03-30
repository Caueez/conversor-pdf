from __future__ import annotations

from infra.database.implementations.postgres import Postgres
from infra.database.shared import DatabaseRow, Query

from account_service.application.interfaces.repository import AuthorizationRepositoryPort
from account_service.domain.entities.permission import PERMISSION_USERS_MANAGE, Permission
from account_service.domain.entities.role import ROLE_KEY_ADMIN, ROLE_KEY_USER, Role
from account_service.shared.typed import new_uuid


class PostgresAuthorizationRepoAdapter(AuthorizationRepositoryPort):
    def __init__(self, persistence: Postgres):
        self._db = persistence

    async def ensure_defaults(self) -> None:
        await self._db.execute(
            Query.create(
                "INSERT",
                """
                INSERT INTO roles (id, key, name, created_at, updated_at)
                VALUES ($1, $2, $3, NOW(), NOW())
                ON CONFLICT (key) DO UPDATE
                SET name = EXCLUDED.name, updated_at = NOW()
                """,
                [new_uuid(), ROLE_KEY_ADMIN, "Administrator"],
            )
        )
        await self._db.execute(
            Query.create(
                "INSERT",
                """
                INSERT INTO roles (id, key, name, created_at, updated_at)
                VALUES ($1, $2, $3, NOW(), NOW())
                ON CONFLICT (key) DO UPDATE
                SET name = EXCLUDED.name, updated_at = NOW()
                """,
                [new_uuid(), ROLE_KEY_USER, "User"],
            )
        )
        await self._db.execute(
            Query.create(
                "INSERT",
                """
                INSERT INTO permissions (id, key, description, created_at, updated_at)
                VALUES ($1, $2, $3, NOW(), NOW())
                ON CONFLICT (key) DO UPDATE
                SET description = EXCLUDED.description, updated_at = NOW()
                """,
                [new_uuid(), PERMISSION_USERS_MANAGE, "Manage users endpoints"],
            )
        )
        await self._db.execute(
            Query.create(
                "INSERT",
                """
                INSERT INTO role_permissions (role_id, permission_id, created_at)
                SELECT r.id, p.id, NOW()
                FROM roles AS r
                JOIN permissions AS p ON p.key = $2
                WHERE r.key = $1
                ON CONFLICT (role_id, permission_id) DO NOTHING
                """,
                [ROLE_KEY_ADMIN, PERMISSION_USERS_MANAGE],
            )
        )

    async def get_role_by_key(self, key: str) -> Role | None:
        record = await self._db.fetch_one(
            Query.create(
                "SELECT",
                """
                SELECT id, key, name, created_at, updated_at
                FROM roles
                WHERE key = $1
                """,
                [key],
            )
        )
        if not record:
            return None
        return self._row_to_role(record)

    async def get_permission_by_key(self, key: str) -> Permission | None:
        record = await self._db.fetch_one(
            Query.create(
                "SELECT",
                """
                SELECT id, key, description, created_at, updated_at
                FROM permissions
                WHERE key = $1
                """,
                [key],
            )
        )
        if not record:
            return None
        return self._row_to_permission(record)

    async def role_has_permission(self, role_key: str, permission_key: str) -> bool:
        record = await self._db.fetch_one(
            Query.create(
                "SELECT",
                """
                SELECT 1 AS allowed
                FROM roles AS r
                JOIN role_permissions AS rp ON rp.role_id = r.id
                JOIN permissions AS p ON p.id = rp.permission_id
                WHERE r.key = $1 AND p.key = $2
                """,
                [role_key, permission_key],
            )
        )
        return bool(record)

    def _row_to_role(self, row: DatabaseRow) -> Role:
        return Role(
            id=str(row["id"]),
            key=row["key"],
            name=row["name"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def _row_to_permission(self, row: DatabaseRow) -> Permission:
        return Permission(
            id=str(row["id"]),
            key=row["key"],
            description=row["description"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
