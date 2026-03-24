

from infra.database.implementations.postgres import Postgres

from infra.database.shared import Query


class Migrations:

    USERS_TABLE = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL
        );
    """

    SESSION_TABLE = """
        CREATE TABLE IF NOT EXISTS sessions (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL,
            token_id TEXT NOT NULL UNIQUE,
            expires_at TIMESTAMPTZ NOT NULL,
            revoked BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ NOT NULL
        );
    """

    def __init__(self, persistence: Postgres) -> None:
        self.db = persistence

        self.tables = [
            self.USERS_TABLE,
            self.SESSION_TABLE
        ]

    def create_query(self, query: str) -> Query:
        return Query(query, [])
        
    async def ensure_schema(self) -> None:
        for table in self.tables:
            await self.db.execute(self.create_query(table))
    
    async def run(self) -> None:
        await self.ensure_schema()