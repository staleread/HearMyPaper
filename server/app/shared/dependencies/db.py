from typing import Annotated
from fastapi import Depends
from sqlalchemy import Connection
from collections.abc import Callable, Generator

from app.shared.config.db import get_db_engine, DataSource

from app.shared.utils.db import SqlRunner


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
