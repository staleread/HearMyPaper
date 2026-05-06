from enum import Enum
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from .env import get_env_settings


class DataSource(Enum):
    POSTGRES = "postgres"


def get_db_engine(data_source: DataSource) -> Engine:
    match data_source:
        case DataSource.POSTGRES:
            return create_engine(get_env_settings().postgres_url)
