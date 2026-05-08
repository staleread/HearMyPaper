from dataclasses import dataclass
from typing import Protocol

from ...enums import AccessLevel
from ...models import User


@dataclass(frozen=True)
class UserCreateCommand:
    name: str
    surname: str
    email: str
    public_key: bytes
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class CreateUserPort(Protocol):
    async def __call__(self, cmd: UserCreateCommand) -> User: ...
