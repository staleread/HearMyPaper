from typing import Protocol

from .models import AuthUser, AuthToken


class AuthRepository(Protocol):
    async def get_user_by_pseudonym(self, pseudonym: str) -> AuthUser | None: ...


class ChallengeRepository(Protocol):
    async def save_challenge(
        self, pseudonym: str, challenge: bytes, ttl: int
    ) -> None: ...
    async def get_challenge(self, pseudonym: str) -> bytes | None: ...
    async def delete_challenge(self, pseudonym: str) -> None: ...


class TokenProvider(Protocol):
    def create_token(self, user: AuthUser) -> AuthToken: ...
