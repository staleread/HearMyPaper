from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from ...models import AuthUser


@dataclass(frozen=True)
class AuthToken:
    token: str
    expires_at: datetime


class TokenProviderPort(Protocol):
    def create_token(self, user: AuthUser) -> AuthToken: ...
