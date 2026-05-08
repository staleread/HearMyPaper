from datetime import datetime, UTC
from typing import override

from ..models import User
from ..exceptions import (
    UserAlreadyExistsError,
    IdentityCollisionError,
)
from ..ports.incoming.create_user import (
    CreateUserPort,
    UserCreateCommand,
)
from ..ports.outgoing.user_repository import (
    UserRepositoryPort,
)
from ..ports.outgoing.identity_provider import (
    IdentityProviderPort,
)


class CreateUserUseCase(CreateUserPort):
    def __init__(self, users: UserRepositoryPort, id_provider: IdentityProviderPort):
        self.users = users
        self.id_provider = id_provider

    @override
    async def __call__(self, cmd: UserCreateCommand) -> User:
        if await self.users.exists_with_email(cmd.email):
            raise UserAlreadyExistsError(f"User with email {cmd.email} already exists")

        user_id = self.id_provider.generate()

        # Check for ID collisions
        if await self.users.get_by_id(user_id):
            raise IdentityCollisionError(
                f"Identity collision for generated ID: {user_id}"
            )

        user = User(
            id=user_id,
            name=cmd.name,
            surname=cmd.surname,
            email=cmd.email,
            confidentiality_level=cmd.confidentiality_level,
            integrity_levels=cmd.integrity_levels,
            created_at=datetime.now(UTC),
        )

        await self.users.save(user, cmd.public_key)
        return user
