from sqlalchemy import text
from sqlalchemy.engine import Connection
from typing import TypeVar, Callable, Any


T = TypeVar("T")


class SqlQueryRunner:
    def __init__(self, *, connection: Connection):
        self.connection = connection
        self.kwargs: dict[str, Any] = {}

    def query(self, sql: str):
        self.sql = sql
        return self

    def bind(self, **kwargs: str | int | float | bool | None):
        self.kwargs = kwargs
        return self

    def first(self, map_row: Callable[[dict], T]) -> T | None:
        row = self.connection.execute(text(self.sql), self.kwargs).first()

        if not row:
            return None
        return map_row(dict(row._mapping))

    def first_row(self) -> dict | None:
        return self.first(lambda x: x)

    def one(self, map_row: Callable[[dict], T]) -> T:
        row = self.connection.execute(text(self.sql), self.kwargs).one()
        return map_row(dict(row._mapping))

    def one_row(self) -> dict:
        return self.one(lambda x: x)

    def many(self, map_row: Callable[[dict], T]) -> list[T]:
        rows = self.connection.execute(text(self.sql), self.kwargs).all()
        return list(map(lambda x: map_row(dict(x._mapping)), rows))

    def many_rows(self) -> list[dict]:
        return self.many(lambda x: x)

    def scalar(self) -> Any:
        return self.connection.execute(text(self.sql), self.kwargs).scalar()


class SqlRunner(SqlQueryRunner):
    def __init__(self, *, connection: Connection):
        super().__init__(connection=connection)

    def execute(self):
        self.connection.execute(text(self.sql), self.kwargs)

    def execute_unsafe(self):
        self.connection.exec_driver_sql(self.sql, self.kwargs)
