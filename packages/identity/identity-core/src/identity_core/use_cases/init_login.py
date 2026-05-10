from typing import override

from ..ports.outgoing.challenge_generator import ChallengeGeneratorPort
from ..exceptions import UserNotFoundError
from ..ports.incoming.init_login import InitLoginPort
from ..ports.outgoing.auth_repository import (
    AuthRepositoryPort,
)
from ..ports.outgoing.challenge_repository import (
    ChallengeRepositoryPort,
)


class InitLoginUseCase(InitLoginPort):
    def __init__(
        self,
        users: AuthRepositoryPort,
        challenges: ChallengeRepositoryPort,
        challenge_gen: ChallengeGeneratorPort,
    ):
        self.users = users
        self.challenges = challenges
        self.challenge_gen = challenge_gen

    @override
    async def __call__(self, user_id: str) -> bytes:
        user = await self.users.get_user_by_id(user_id)

        if not user:
            raise UserNotFoundError(f"No user with id {user_id}")

        challenge = self.challenge_gen.generate()
        await self.challenges.save_challenge(user_id, challenge, ttl=300)

        return challenge
