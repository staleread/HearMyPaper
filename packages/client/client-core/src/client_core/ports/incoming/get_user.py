from typing import Protocol
from ...models import User


class GetUserPort(Protocol):
    async def __call__(self, user_id: str) -> User | None: ...
