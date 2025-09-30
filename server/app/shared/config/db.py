from enum import Enum
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from app.shared.exceptions import DataSourceNotFoundException

from .env import env_settings


class DataSource(Enum):
    POSTGRES = "postgres"


postgres_engine = create_engine(env_settings.postgres_url)


def get_db_engine(data_source: DataSource) -> Engine:
    match data_source:
        case DataSource.POSTGRES:
            return postgres_engine
        case _:
            raise DataSourceNotFoundException(data_source)
