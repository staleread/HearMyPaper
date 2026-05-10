import redis.asyncio as aioredis


class RedisClient:
    def __init__(self, url: str):
        self._client: aioredis.Redis = aioredis.from_url(url, decode_responses=False)

    @property
    def client(self) -> aioredis.Redis:
        return self._client

    async def close(self):
        await self._client.close()
