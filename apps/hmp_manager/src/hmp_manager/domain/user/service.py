from datetime import datetime, UTC

from .models import User, UserCreate, UserUpdate
from .ports import UserRepository, IdentityProvider
from .exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    IdentityCollisionError,
)


class UserService:
    def __init__(self, users: UserRepository, id_provider: IdentityProvider):
        self.users = users
        self.id_provider = id_provider

    async def create_user(self, cmd: UserCreate) -> User:
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

    async def get_user(self, user_id: str) -> User:
        user = await self.users.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user

    async def get_user_public_key(self, user_id: str) -> bytes:
        public_key = await self.users.get_public_key_by_id(user_id)
        if not public_key:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return public_key

    async def update_user(self, user_id: str, cmd: UserUpdate) -> User:
        user = await self.users.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        if cmd.email != user.email:
            if await self.users.exists_with_email(cmd.email):
                raise UserAlreadyExistsError(
                    f"User with email {cmd.email} already exists"
                )

        return await self.users.update(user_id, cmd)
