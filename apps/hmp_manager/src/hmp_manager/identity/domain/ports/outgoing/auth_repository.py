from typing import Protocol
from ...models import AuthUser


class AuthRepositoryPort(Protocol):
    async def get_user_by_id(self, id: str) -> AuthUser | None: ...
