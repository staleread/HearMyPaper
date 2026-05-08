from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class LoginCommand:
    id: str
    challenge: bytes
    signature: bytes


@dataclass(frozen=True)
class AuthToken:
    token: str
    expires_at: datetime


class FinalizeLoginPort(Protocol):
    async def __call__(self, cmd: LoginCommand) -> AuthToken: ...
