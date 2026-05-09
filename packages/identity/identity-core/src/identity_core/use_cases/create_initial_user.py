from datetime import datetime, UTC
from typing import override

from ..enums import AccessLevel
from ..models import User
from ..ports.incoming.create_initial_user import (
    CreateInitialUserPort,
    InitialUserCreateCommand,
)
from ..ports.outgoing.user_repository import (
    UserRepositoryPort,
)


class CreateInitialUserUseCase(CreateInitialUserPort):
    def __init__(self, users: UserRepositoryPort):
        self.users = users

    @override
    async def __call__(self, cmd: InitialUserCreateCommand) -> bool:
        if await self.users.has_any_users():
            return False

        user = User(
            id=cmd.id,
            name=cmd.name,
            surname=cmd.surname,
            email=cmd.email,
            confidentiality_level=AccessLevel.CONFIDENTIAL,
            integrity_levels=[AccessLevel.CONFIDENTIAL],
            created_at=datetime.now(UTC),
        )

        await self.users.save(user, cmd.public_key)
        return True
