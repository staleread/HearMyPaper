from hmp_manager.identity.domain.exceptions import UserNotFoundError
from hmp_manager.identity.domain.ports.incoming.get_user_public_key import (
    GetUserPublicKeyPort,
)
from hmp_manager.identity.domain.ports.outgoing.user_repository import (
    UserRepositoryPort,
)


class GetUserPublicKeyUseCase(GetUserPublicKeyPort):
    def __init__(self, users: UserRepositoryPort):
        self.users = users

    async def __call__(self, user_id: str) -> bytes:
        public_key = await self.users.get_public_key_by_id(user_id)
        if not public_key:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return public_key
