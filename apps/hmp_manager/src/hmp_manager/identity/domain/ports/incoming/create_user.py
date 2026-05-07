from typing import Protocol
from pydantic import BaseModel, EmailStr
from ...enums import AccessLevel
from ...models import User


class UserCreateCommand(BaseModel):
    name: str
    surname: str
    email: EmailStr
    public_key: bytes
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class CreateUserPort(Protocol):
    async def __call__(self, cmd: UserCreateCommand) -> User: ...
