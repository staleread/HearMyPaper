from dataclasses import dataclass
from typing import Protocol

from ...models import User
from ...enums import AccessLevel


@dataclass(frozen=True)
class UserUpdateCommand:
    name: str
    surname: str
    email: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class UserRepositoryPort(Protocol):
    async def save(self, user: User, public_key: bytes) -> None: ...
    async def get_by_id(self, id: str) -> User | None: ...
    async def get_public_key_by_id(self, id: str) -> bytes | None: ...
    async def update(self, id: str, user_update: UserUpdateCommand) -> User: ...
    async def exists_with_email(self, email: str) -> bool: ...
