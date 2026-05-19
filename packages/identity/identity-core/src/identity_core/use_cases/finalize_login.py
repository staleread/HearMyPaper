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
from ..ports.outgoing.user_repository import (
    UserRepositoryPort,
)
from ..ports.outgoing.challenge_repository import (
    ChallengeRepositoryPort,
)
from ..ports.outgoing.token_provider import TokenProviderPort
from ..ports.outgoing.signature_verifier import SignatureVerifierPort


class FinalizeLoginUseCase(FinalizeLoginPort):
    def __init__(
        self,
        auth_repo: AuthRepositoryPort,
        user_repo: UserRepositoryPort,
        challenges: ChallengeRepositoryPort,
        signature_verifier: SignatureVerifierPort,
        tokens: TokenProviderPort,
    ):
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        self.challenges = challenges
        self.signature_verifier = signature_verifier
        self.tokens = tokens

    @override
    async def __call__(self, cmd: LoginCommand) -> AuthToken:
        user = await self.auth_repo.get_user_by_id(cmd.user_id)

        if not user:
            raise UserNotFoundError(f"No user with id {cmd.user_id}")

        public_key = await self.user_repo.get_public_key_by_id(cmd.user_id)
        if not public_key:
            raise UserNotFoundError(f"Public key for user {cmd.user_id} not found")

        challenge = await self.challenges.get_challenge(cmd.user_id)

        if not challenge or challenge != cmd.challenge:
            raise InvalidChallengeError()

        is_valid_signature = self.signature_verifier.verify(
            challenge, signature=cmd.signature, public_key=public_key
        )

        if not is_valid_signature:
            raise AuthenticationFailedError()

        await self.challenges.delete_challenge(cmd.user_id)

        token = self.tokens.create_token(user)

        return AuthToken(token=token.token, expires_at=token.expires_at)
