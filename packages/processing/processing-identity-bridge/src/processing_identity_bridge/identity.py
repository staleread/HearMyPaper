from typing import override
from processing_core.ports.outgoing.identity import IdentityPort
from identity_core.ports.incoming.get_user_public_key import GetUserPublicKeyPort


class IdentityAdapter(IdentityPort):
    def __init__(self, identity_service: GetUserPublicKeyPort):
        self._identity_service = identity_service

    @override
    async def get_public_key(self, user_id: str) -> bytes:
        return await self._identity_service(user_id)
