from typing import Protocol
from ...models import User, AccessLevel


class CreateUserPort(Protocol):
    async def __call__(
        self,
        name: str,
        surname: str,
        email: str,
        confidentiality_level: AccessLevel,
        integrity_levels: list[AccessLevel],
        credentials_path: str,
        credentials_password: str,
    ) -> User: ...
