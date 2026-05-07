from hmp_core import crypto

from hmp_manager.identity.domain.exceptions import (
    UserNotFoundError,
    InvalidChallengeError,
    AuthenticationFailedError,
)
from hmp_manager.identity.domain.ports.incoming.finalize_login import (
    FinalizeLoginPort,
    LoginCommand,
    AuthToken,
)
from hmp_manager.identity.domain.ports.outgoing.auth_repository import (
    AuthRepositoryPort,
)
from hmp_manager.identity.domain.ports.outgoing.challenge_repository import (
    ChallengeRepositoryPort,
)
from hmp_manager.identity.domain.ports.outgoing.token_provider import TokenProviderPort


class FinalizeLoginUseCase(FinalizeLoginPort):
    def __init__(
        self,
        users: AuthRepositoryPort,
        challenges: ChallengeRepositoryPort,
        tokens: TokenProviderPort,
    ):
        self.users = users
        self.challenges = challenges
        self.tokens = tokens

    async def __call__(self, cmd: LoginCommand) -> AuthToken:
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
