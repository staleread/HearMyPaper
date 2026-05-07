from typing import Protocol
from ...models import AuthUser
from ..incoming.finalize_login import AuthToken


class TokenProviderPort(Protocol):
    def create_token(self, user: AuthUser) -> AuthToken: ...
