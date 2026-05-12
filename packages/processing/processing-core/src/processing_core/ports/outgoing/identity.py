from typing import Protocol


class IdentityPort(Protocol):
    async def get_public_key(self, user_id: str) -> bytes:
        """Returns the public key of the user."""
        ...
