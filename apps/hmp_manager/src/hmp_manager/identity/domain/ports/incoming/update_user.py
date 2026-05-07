from typing import Protocol
from pydantic import BaseModel, EmailStr
from ...enums import AccessLevel
from ...models import User


class UserUpdateCommand(BaseModel):
    name: str
    surname: str
    email: EmailStr
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class UpdateUserPort(Protocol):
    async def __call__(self, user_id: str, cmd: UserUpdateCommand) -> User: ...
