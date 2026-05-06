from hmp_core import crypto

from .models import AuthToken, LoginCommand
from .ports import AuthRepository, ChallengeRepository, TokenProvider
from .utils import generate_challenge
from .exceptions import (
    UserNotFoundError,
    InvalidChallengeError,
    AuthenticationFailedError,
)


class AuthService:
    def __init__(
        self,
        users: AuthRepository,
        challenges: ChallengeRepository,
        tokens: TokenProvider,
    ):
        self.users = users
        self.challenges = challenges
        self.tokens = tokens

    async def start_login(self, id: str) -> bytes:
        user = await self.users.get_user_by_id(id)

        if not user:
            raise UserNotFoundError(f"No user with id {id}")

        challenge = generate_challenge()
        await self.challenges.save_challenge(id, challenge, ttl=300)

        return challenge

    async def finalize_login(self, cmd: LoginCommand) -> AuthToken:
        user = await self.users.get_user_by_id(cmd.id)

        if not user:
            raise UserNotFoundError(f"No user with id {cmd.id}")

        challenge = await self.challenges.get_challenge(cmd.id)

        if not challenge or challenge != cmd.challenge:
            raise InvalidChallengeError()

        is_valid_signature = crypto.verify(
            challenge, signature=cmd.signature, public_key_bytes=user.public_key
        )

        if not is_valid_signature:
            raise AuthenticationFailedError()

        await self.challenges.delete_challenge(cmd.id)

        return self.tokens.create_token(user)
