from functools import lru_cache
from ..storage import RedisClient

from hmp_manager.config import get_settings


@lru_cache
def get_redis_service() -> RedisClient:
    return RedisClient(get_settings().redis.url)


async def get_redis():
    service = get_redis_service()
    async for client in service.get_client():
        yield client
