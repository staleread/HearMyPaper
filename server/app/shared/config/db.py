from enum import Enum
from sqlalchemy import create_engine

from app.shared.exceptions import DataSourceNotFoundException

from .env import env_settings


class DataSource(Enum):
    POSTGRES = "postgres"


postgres_engine = create_engine(env_settings.postgres.url)


def get_db_engine(data_source: DataSource):
    match data_source:
        case DataSource.POSTGRES:
            return postgres_engine
        case _:
            raise DataSourceNotFoundException(data_source)
