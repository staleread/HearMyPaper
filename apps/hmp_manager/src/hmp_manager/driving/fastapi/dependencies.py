from functools import lru_cache

from hmp_manager.config import get_settings
from hmp_manager.driven.postgres.engine import PostgresEngine
from hmp_manager.driven.redis.client import RedisClient


@lru_cache
def get_postgres_engine() -> PostgresEngine:
    return PostgresEngine(get_settings().postgres_url)


async def get_postgres():
    engine = get_postgres_engine()

    async for session in engine.get_session():
        yield session


@lru_cache
def get_redis_service() -> RedisClient:
    return RedisClient(get_settings().redis_url)


async def get_redis():
    """FastAPI Dependency"""
    service = get_redis_service()
    async for client in service.get_client():
        yield client
