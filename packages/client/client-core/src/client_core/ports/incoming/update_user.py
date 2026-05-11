from typing import Protocol
from ...models import User, AccessLevel


class UpdateUserPort(Protocol):
    async def __call__(
        self,
        user_id: str,
        name: str,
        surname: str,
        email: str,
        confidentiality_level: AccessLevel,
        integrity_levels: list[AccessLevel],
    ) -> User: ...
