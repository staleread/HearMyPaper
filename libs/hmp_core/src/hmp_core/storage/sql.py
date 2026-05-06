from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import Any, TypeVar
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

T = TypeVar("T")
RowDict = dict[str, Any]
SupportedData = str | int | float | bool | list[Any] | bytes | UUID | None


class SqlRunner:
    """
    Request-scoped runner wrapping an existing SQLAlchemy AsyncSession.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.kwargs: dict[str, Any] = {}
        self.sql: str = ""

    def query(self, sql: str) -> SqlRunner:
        self.sql = sql
        return self

    def bind(self, **kwargs: SupportedData) -> SqlRunner:
        self.kwargs = kwargs
        return self

    async def first(self, map_row: Callable[[RowDict], T]) -> T | None:
        result = await self.session.execute(text(self.sql), self.kwargs)
        row = result.mappings().first()
        if not row:
            return None
        return map_row(dict(row))

    async def first_row(self) -> RowDict | None:
        return await self.first(lambda x: x)

    async def one(self, map_row: Callable[[RowDict], T]) -> T:
        result = await self.session.execute(text(self.sql), self.kwargs)
        row = result.mappings().one()
        return map_row(dict(row))

    async def one_row(self) -> RowDict:
        return await self.one(lambda x: x)

    async def many(self, map_row: Callable[[RowDict], T]) -> list[T]:
        result = await self.session.execute(text(self.sql), self.kwargs)
        rows = result.mappings().all()
        return [map_row(dict(x)) for x in rows]

    async def many_rows(self) -> list[RowDict]:
        return await self.many(lambda x: x)

    async def scalar(self, map_value: Callable[[Any], T]) -> T:
        result = await self.session.execute(text(self.sql), self.kwargs)
        value = result.scalar()
        return map_value(value)

    async def execute(self) -> None:
        await self.session.execute(text(self.sql), self.kwargs)

    async def execute_unsafe(self) -> None:
        conn = await self.session.connection()
        await conn.exec_driver_sql(self.sql, self.kwargs)


class TransactionalSqlRunner:
    """
    Runner that opens a fresh AsyncEngine connection/transaction for each operation
    and commits it immediately. Use when you want the statement to be durable
    even if the request-scoped transaction is rolled back (e.g. audit logs).
    """

    def __init__(self, engine: AsyncEngine):
        self._engine = engine
        self.kwargs: dict[str, Any] = {}
        self.sql: str = ""

    @asynccontextmanager
    async def _temp_conn(self):
        async with self._engine.begin() as conn:
            yield conn

    def query(self, sql: str) -> TransactionalSqlRunner:
        self.sql = sql
        return self

    def bind(self, **kwargs: SupportedData) -> TransactionalSqlRunner:
        self.kwargs = kwargs
        return self

    async def execute(self) -> None:
        async with self._temp_conn() as conn:
            await conn.execute(text(self.sql), self.kwargs)

    async def execute_unsafe(self) -> None:
        async with self._temp_conn() as conn:
            await conn.exec_driver_sql(self.sql, self.kwargs)

    async def first(self, map_row: Callable[[RowDict], T]) -> T | None:
        async with self._temp_conn() as conn:
            result = await conn.execute(text(self.sql), self.kwargs)
            row = result.mappings().first()
            if not row:
                return None
            return map_row(dict(row))

    async def first_row(self) -> RowDict | None:
        return await self.first(lambda x: x)

    async def one(self, map_row: Callable[[RowDict], T]) -> T:
        async with self._temp_conn() as conn:
            result = await conn.execute(text(self.sql), self.kwargs)
            row = result.mappings().one()
            return map_row(dict(row))

    async def one_row(self) -> RowDict:
        return await self.one(lambda x: x)

    async def many(self, map_row: Callable[[RowDict], T]) -> list[T]:
        async with self._temp_conn() as conn:
            result = await conn.execute(text(self.sql), self.kwargs)
            rows = result.mappings().all()
            return [map_row(dict(x)) for x in rows]

    async def many_rows(self) -> list[RowDict]:
        return await self.many(lambda x: x)

    async def scalar(self, map_value: Callable[[Any], T]) -> T:
        async with self._temp_conn() as conn:
            result = await conn.execute(text(self.sql), self.kwargs)
            value = result.scalar()
            return map_value(value)
