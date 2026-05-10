from typing import override
from ..exceptions import (
    UserNotFoundError,
    InvalidChallengeError,
    AuthenticationFailedError,
)
from ..ports.incoming import (
    FinalizeLoginPort,
    LoginCommand,
    AuthToken,
)
from ..ports.outgoing.auth_repository import (
    AuthRepositoryPort,
)
from ..ports.outgoing.challenge_repository import (
    ChallengeRepositoryPort,
)
from ..ports.outgoing.token_provider import TokenProviderPort
from ..ports.outgoing.signature_verifier import SignatureVerifierPort


class FinalizeLoginUseCase(FinalizeLoginPort):
    def __init__(
        self,
        users: AuthRepositoryPort,
        challenges: ChallengeRepositoryPort,
        signature_verifier: SignatureVerifierPort,
        tokens: TokenProviderPort,
    ):
        self.users = users
        self.challenges = challenges
        self.signature_verifier = signature_verifier
        self.tokens = tokens

    @override
    async def __call__(self, cmd: LoginCommand) -> AuthToken:
        user = await self.users.get_user_by_id(cmd.user_id)

        if not user:
            raise UserNotFoundError(f"No user with id {cmd.user_id}")

        challenge = await self.challenges.get_challenge(cmd.user_id)

        if not challenge or challenge != cmd.challenge:
            raise InvalidChallengeError()

        is_valid_signature = self.signature_verifier.verify(
            challenge, signature=cmd.signature, public_key=user.public_key
        )

        if not is_valid_signature:
            raise AuthenticationFailedError()

        await self.challenges.delete_challenge(cmd.user_id)

        token = self.tokens.create_token(user)

        return AuthToken(token=token.token, expires_at=token.expires_at)
