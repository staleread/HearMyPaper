from typing import Annotated
from fastapi import Depends
from sqlalchemy import Connection

from app.shared.config.db import get_db_engine, DataSource

from app.shared.utils.db import SqlQueryRunner


def get_db_connection(data_source: DataSource):
    def get_connection():
        with get_db_engine(data_source).begin() as connection:
            yield connection

    return get_connection


PostgresConnectionDep = Annotated[
    Connection, Depends(get_db_connection(DataSource.POSTGRES))
]


def get_postgres_query_runner(connection: PostgresConnectionDep) -> SqlQueryRunner:
    return SqlQueryRunner(connection=connection)


PostgresQueryRunnerDep = Annotated[SqlQueryRunner, Depends(get_postgres_query_runner)]
