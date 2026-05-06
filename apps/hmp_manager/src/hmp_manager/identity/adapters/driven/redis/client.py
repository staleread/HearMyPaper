import redis.asyncio as aioredis
from typing import Any
from collections.abc import AsyncGenerator


class RedisClient:
    def __init__(self, url: str):
        self._client: aioredis.Redis[Any] = aioredis.from_url(
            url, decode_responses=True
        )

    async def get_client(self) -> AsyncGenerator[aioredis.Redis[Any], None]:
        yield self._client

    async def close(self):
        await self._client.close()
