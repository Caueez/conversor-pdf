

from infra.database.implementations.postgres import Postgres

from infra.database.shared import Query


class Migrations:

    ROLES_TABLE = ("CREATE", """
        CREATE TABLE IF NOT EXISTS roles (
            id UUID PRIMARY KEY,
            key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL
        );
    """)

    PERMISSIONS_TABLE = ("CREATE", """
        CREATE TABLE IF NOT EXISTS permissions (
            id UUID PRIMARY KEY,
            key TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL
        );
    """)

    ROLE_PERMISSIONS_TABLE = ("CREATE", """
        CREATE TABLE IF NOT EXISTS role_permissions (
            role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
            permission_id UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
            created_at TIMESTAMPTZ NOT NULL,
            PRIMARY KEY (role_id, permission_id)
        );
    """)

    USERS_TABLE = ("CREATE", """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL
        );
    """)

    USERS_ROLE_COLUMN = ("ALTER", """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS role TEXT NOT NULL DEFAULT 'user';
    """)

    SESSION_TABLE = ("CREATE", """
        CREATE TABLE IF NOT EXISTS sessions (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL,
            token_id TEXT NOT NULL UNIQUE,
            expires_at TIMESTAMPTZ NOT NULL,
            revoked BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ NOT NULL
        );
    """)

    def __init__(self, persistence: Postgres) -> None:
        self.db = persistence

        self.tables = [
            self.ROLES_TABLE,
            self.PERMISSIONS_TABLE,
            self.ROLE_PERMISSIONS_TABLE,
            self.USERS_TABLE,
            self.USERS_ROLE_COLUMN,
            self.SESSION_TABLE
        ]

    def create_query(self, query: tuple[str]) -> Query:
        return Query(query[0], query[1], [])
        
    async def ensure_schema(self) -> None:
        for table in self.tables:
            await self.db.execute(self.create_query(table))
    
    async def run(self) -> None:
        await self.ensure_schema()
