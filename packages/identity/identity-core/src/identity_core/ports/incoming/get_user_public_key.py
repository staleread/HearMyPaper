from typing import Protocol


class GetUserPublicKeyPort(Protocol):
    async def __call__(self, user_id: str) -> bytes: ...
