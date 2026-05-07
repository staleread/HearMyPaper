from hmp_manager.identity.domain.utils import generate_challenge
from hmp_manager.identity.domain.exceptions import UserNotFoundError
from hmp_manager.identity.domain.ports.incoming.init_login import InitLoginPort
from hmp_manager.identity.domain.ports.outgoing.auth_repository import (
    AuthRepositoryPort,
)
from hmp_manager.identity.domain.ports.outgoing.challenge_repository import (
    ChallengeRepositoryPort,
)


class InitLoginUseCase(InitLoginPort):
    def __init__(
        self,
        users: AuthRepositoryPort,
        challenges: ChallengeRepositoryPort,
    ):
        self.users = users
        self.challenges = challenges

    async def __call__(self, id: str) -> bytes:
        user = await self.users.get_user_by_id(id)

        if not user:
            raise UserNotFoundError(f"No user with id {id}")

        challenge = generate_challenge()
        await self.challenges.save_challenge(id, challenge, ttl=300)

        return challenge
