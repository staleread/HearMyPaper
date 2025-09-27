from sqlalchemy import text
from sqlalchemy.engine import Connection
from typing import TypeVar, Callable, Any


T = TypeVar("T")
RowDict = dict[str, Any]
SupportedData = str | int | float | bool | list[Any] | bytes | None


class SqlRunner:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.kwargs: dict[str, Any] = {}
        self.sql: str = ""

    def query(self, sql: str) -> "SqlRunner":
        self.sql = sql
        return self

    def bind(self, **kwargs: SupportedData) -> "SqlRunner":
        self.kwargs = kwargs
        return self

    def first(self, map_row: Callable[[RowDict], T]) -> T | None:
        row = self.connection.execute(text(self.sql), self.kwargs).first()
        if not row:
            return None
        return map_row(dict(row._mapping))

    def first_row(self) -> RowDict | None:
        return self.first(lambda x: x)

    def one(self, map_row: Callable[[RowDict], T]) -> T:
        row = self.connection.execute(text(self.sql), self.kwargs).one()
        return map_row(dict(row._mapping))

    def one_row(self) -> RowDict:
        return self.one(lambda x: x)

    def many(self, map_row: Callable[[RowDict], T]) -> list[T]:
        rows = self.connection.execute(text(self.sql), self.kwargs).all()
        return [map_row(dict(x._mapping)) for x in rows]

    def many_rows(self) -> list[RowDict]:
        return self.many(lambda x: x)

    def scalar(self, map_value: Callable[[Any], T]) -> T:
        value = self.connection.execute(text(self.sql), self.kwargs).scalar()
        return map_value(value)

    def execute(self) -> None:
        self.connection.execute(text(self.sql), self.kwargs)

    def execute_unsafe(self) -> None:
        self.connection.exec_driver_sql(self.sql, self.kwargs)
