from typing import Protocol
from ...models import User, AccessLevel


class IdentityPort(Protocol):
    async def get_user(self, user_id: str) -> User | None: ...
    async def get_public_key(self, user_id: str) -> bytes: ...
    async def init_login(self, user_id: str) -> bytes: ...
    async def finalize_login(
        self, user_id: str, challenge: bytes, signature: bytes
    ) -> str: ...

    async def create_user(
        self,
        name: str,
        surname: str,
        email: str,
        public_key: bytes,
        confidentiality_level: AccessLevel,
        integrity_levels: list[AccessLevel],
    ) -> User: ...

    async def update_user(
        self,
        user_id: str,
        name: str,
        surname: str,
        email: str,
        confidentiality_level: AccessLevel,
        integrity_levels: list[AccessLevel],
    ) -> User: ...
