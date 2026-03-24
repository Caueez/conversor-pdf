from typing import Optional

import asyncpg
from asyncpg import Pool

from infra.database.shared import DatabaseRow, Query

class Postgres:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._pool: Optional[Pool] = None

    async def conect(self) -> None:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(dsn=self._dsn)
    
    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
    
    async def fetch_one(self, query: Query) -> Optional[DatabaseRow]:
        if self._pool is None:
            raise RuntimeError("Postgres not initialized")

        values = query.values or []
        record = await self._pool.fetchrow(query.query, *values)
        if record is None:
            return
        return DatabaseRow.create({**record})

    async def fetch_all(self, query: Query) -> list[DatabaseRow]:
        if self._pool is None:
            raise RuntimeError("Postgres not initialized")

        values = query.values or []
        records = await self._pool.fetch(query.query, *values)
        return [DatabaseRow.create({**record}) for record in records]

    async def execute(self, query: Query) -> str:
        if self._pool is None:
            raise RuntimeError("Postgres not initialized")
        
        values = query.values or []
        return await self._pool.execute(query.query, *values)
        
