from typing import Protocol
from datetime import datetime
from pydantic import BaseModel


class LoginCommand(BaseModel):
    id: str
    challenge: bytes
    signature: bytes


class AuthToken(BaseModel):
    token: str
    expires_at: datetime


class FinalizeLoginPort(Protocol):
    async def __call__(self, cmd: LoginCommand) -> AuthToken: ...
