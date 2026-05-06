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

    async def start_login(self, pseudonym: str) -> bytes:
        user = await self.users.get_user_by_pseudonym(pseudonym)

        if not user:
            raise UserNotFoundError(f"No user with pseudonym {pseudonym}")

        challenge = generate_challenge()
        await self.challenges.save_challenge(pseudonym, challenge, ttl=300)

        return challenge

    async def finalize_login(self, cmd: LoginCommand) -> AuthToken:
        user = await self.users.get_user_by_pseudonym(cmd.pseudonym)

        if not user:
            raise UserNotFoundError(f"No user with pseudonym {cmd.pseudonym}")

        challenge = await self.challenges.get_challenge(cmd.pseudonym)

        if not challenge or challenge != cmd.challenge:
            raise InvalidChallengeError()

        is_valid_signature = crypto.verify(
            challenge, signature=cmd.signature, public_key_bytes=user.public_key
        )

        if not is_valid_signature:
            raise AuthenticationFailedError()

        await self.challenges.delete_challenge(cmd.pseudonym)

        return self.tokens.create_token(user)
