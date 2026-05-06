from typing import Protocol

from .models import AuthUser, AuthToken


class AuthRepository(Protocol):
    async def get_user_by_id(self, id: str) -> AuthUser | None: ...


class ChallengeRepository(Protocol):
    async def save_challenge(self, id: str, challenge: bytes, ttl: int) -> None: ...
    async def get_challenge(self, id: str) -> bytes | None: ...
    async def delete_challenge(self, id: str) -> None: ...


class TokenProvider(Protocol):
    def create_token(self, user: AuthUser) -> AuthToken: ...
