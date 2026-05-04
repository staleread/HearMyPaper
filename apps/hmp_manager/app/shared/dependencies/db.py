from typing import Annotated
from fastapi import Depends
from sqlalchemy import Connection
from collections.abc import Callable, Generator, AsyncGenerator
from contextlib import asynccontextmanager

from app.shared.config.db import get_db_engine, DataSource
from hmp_core.storage import SqlRunner


def get_db_connection(
    data_source: DataSource,
) -> Callable[[], Generator[Connection, None, None]]:
    def get_connection() -> Generator[Connection, None, None]:
        with get_db_engine(data_source).begin() as connection:
            yield connection

    return get_connection


PostgresConnectionDep = Annotated[
    Connection, Depends(get_db_connection(DataSource.POSTGRES))
]


def get_postgres_runner(connection: PostgresConnectionDep) -> SqlRunner:
    return SqlRunner(connection=connection)


PostgresRunnerDep = Annotated[SqlRunner, Depends(get_postgres_runner)]

@asynccontextmanager
async def get_db_runner_context() -> AsyncGenerator[SqlRunner, None]:
    """Provides a SqlRunner for background tasks or non-FastAPI contexts."""
    engine = get_db_engine(DataSource.POSTGRES)
    with engine.begin() as connection:
        yield SqlRunner(connection=connection)
