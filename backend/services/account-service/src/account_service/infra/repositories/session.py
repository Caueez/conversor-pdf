from __future__ import annotations

from datetime import datetime
from uuid import UUID

from infra.database.implementations.postgres import Postgres
from infra.database.shared import DatabaseRow, Query

from account_service.application.interfaces.repository import SessionRepositoryPort
from account_service.domain.entities.session import Session


class PostgresSessionRepoAdapter(SessionRepositoryPort):
    def __init__(self, persistence: Postgres):
        self._db = persistence

    def _row_to_entity(self, row: DatabaseRow) -> Session:
        return Session(
            id=row["id"],
            user_id=row["user_id"],
            token_id=row["token_id"],
            expires_at=row["expires_at"],
            revoked=row["revoked"],
            created_at=row["created_at"],
        )

    async def create(self, session: Session) -> Session:
        query = Query.create(
            "INSERT",
            """
            INSERT INTO sessions (id, user_id, token_id, expires_at, revoked, created_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            [
                session.id,
                session.user_id,
                session.token_id,
                session.expires_at,
                session.revoked,
                session.created_at,
            ],
        )

        await self._db.execute(query)
        return session

    async def get(self, session_id: UUID) -> Session | None:
        query = Query.create(
            "SELECT",
            """
            SELECT id, user_id, token_id, expires_at, revoked, created_at
            FROM sessions
            WHERE id = $1
            """,
            [str(session_id)],
        )

        record = await self._db.fetch_one(query)
        if not record:
            return None
        return self._row_to_entity(record)

    async def rotate(self, session_id: UUID, token_id: str, expires_at: datetime) -> None:
        query = Query.create(
            "UPDATE",
            """
            UPDATE sessions
            SET token_id = $1, expires_at = $2
            WHERE id = $3
            """,
            [token_id, expires_at, str(session_id)],
        )

        await self._db.execute(query)

    async def revoke(self, session_id: UUID) -> None:
        query = Query.create(
            "UPDATE",
            """
            UPDATE sessions
            SET revoked = TRUE
            WHERE id = $1
            """,
            [str(session_id)],
        )

        await self._db.execute(query)
