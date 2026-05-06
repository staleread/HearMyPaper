from functools import lru_cache
from hmp_core.storage import PostgresEngine, RedisClient

from hmp_manager.config import get_settings


@lru_cache
def get_postgres_engine() -> PostgresEngine:
    return PostgresEngine(get_settings().postgres.url)


async def get_postgres():
    engine = get_postgres_engine()

    async for session in engine.get_session():
        yield session


@lru_cache
def get_redis_service() -> RedisClient:
    return RedisClient(get_settings().redis.url)


async def get_redis():
    service = get_redis_service()
    async for client in service.get_client():
        yield client
