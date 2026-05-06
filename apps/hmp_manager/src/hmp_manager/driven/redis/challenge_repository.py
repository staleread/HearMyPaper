from typing import Any, override
import redis.asyncio as aioredis

from hmp_manager.domain.auth.ports import ChallengeRepository


class RedisChallengeRepository(ChallengeRepository):
    def __init__(self, client: aioredis.Redis[Any]):
        self._client = client

    @override
    async def save_challenge(self, id: str, challenge: bytes, ttl: int) -> None:
        _ = await self._client.setex(f"challenge:{id}", ttl, challenge)

    @override
    async def get_challenge(self, id: str) -> bytes | None:
        value = await self._client.get(f"challenge:{id}")
        if value is None:
            return None
        if isinstance(value, str):
            return value.encode()
        return value

    @override
    async def delete_challenge(self, id: str) -> None:
        _ = await self._client.delete(f"challenge:{id}")
