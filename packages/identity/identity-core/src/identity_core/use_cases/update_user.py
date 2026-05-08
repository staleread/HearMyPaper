from typing import override
from ..models import User
from ..exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
)
from ..ports.incoming.update_user import (
    UpdateUserPort,
    UserUpdateCommand,
)
from ..ports.outgoing.user_repository import (
    UserRepositoryPort,
    UserUpdateCommand as OutgoingUserUpdateCommand,
)


class UpdateUserUseCase(UpdateUserPort):
    def __init__(self, users: UserRepositoryPort):
        self.users = users

    @override
    async def __call__(self, user_id: str, cmd: UserUpdateCommand) -> User:
        user = await self.users.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        if cmd.email != user.email:
            if await self.users.exists_with_email(cmd.email):
                raise UserAlreadyExistsError(
                    f"User with email {cmd.email} already exists"
                )

        outgoing_cmd = OutgoingUserUpdateCommand(
            name=cmd.name,
            surname=cmd.surname,
            email=cmd.email,
            confidentiality_level=cmd.confidentiality_level,
            integrity_levels=cmd.integrity_levels,
        )

        return await self.users.update(user_id, outgoing_cmd)
