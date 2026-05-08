from typing import override
from ..models import User
from ..exceptions import UserNotFoundError
from ..ports.incoming.get_user import GetUserPort
from ..ports.outgoing.user_repository import (
    UserRepositoryPort,
)


class GetUserUseCase(GetUserPort):
    def __init__(self, users: UserRepositoryPort):
        self.users = users

    @override
    async def __call__(self, user_id: str) -> User:
        user = await self.users.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user
