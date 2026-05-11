from typing import override
import redis.asyncio as aioredis

from identity_core.ports.outgoing.challenge_repository import ChallengeRepositoryPort


class RedisChallengeRepositoryAdapter(ChallengeRepositoryPort):
    def __init__(self, client: aioredis.Redis):
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
