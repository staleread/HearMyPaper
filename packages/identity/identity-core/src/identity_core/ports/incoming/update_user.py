from dataclasses import dataclass
from typing import Protocol

from ...enums import AccessLevel
from ...models import User


@dataclass(frozen=True)
class UserUpdateCommand:
    name: str
    surname: str
    email: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class UpdateUserPort(Protocol):
    async def __call__(self, user_id: str, cmd: UserUpdateCommand) -> User: ...
