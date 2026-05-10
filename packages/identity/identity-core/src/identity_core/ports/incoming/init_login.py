from typing import Protocol


class InitLoginPort(Protocol):
    async def __call__(self, user_id: str) -> bytes: ...
