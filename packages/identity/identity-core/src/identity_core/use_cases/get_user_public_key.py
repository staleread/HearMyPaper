from typing import override
from ..exceptions import UserNotFoundError
from ..ports.incoming.get_user_public_key import (
    GetUserPublicKeyPort,
)
from ..ports.outgoing.user_repository import (
    UserRepositoryPort,
)


class GetUserPublicKeyUseCase(GetUserPublicKeyPort):
    def __init__(self, users: UserRepositoryPort):
        self.users = users

    @override
    async def __call__(self, user_id: str) -> bytes:
        public_key = await self.users.get_public_key_by_id(user_id)
        if not public_key:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return public_key
