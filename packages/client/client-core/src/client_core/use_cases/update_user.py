from ..ports.incoming.update_user import UpdateUserPort
from ..ports.outgoing.identity import IdentityPort
from ..models import User, AccessLevel


class UpdateUserUseCase(UpdateUserPort):
    def __init__(self, identity_port: IdentityPort):
        self.identity_port = identity_port

    async def __call__(
        self,
        user_id: str,
        name: str,
        surname: str,
        email: str,
        confidentiality_level: AccessLevel,
        integrity_levels: list[AccessLevel],
    ) -> User:
        return await self.identity_port.update_user(
            user_id=user_id,
            name=name,
            surname=surname,
            email=email,
            confidentiality_level=confidentiality_level,
            integrity_levels=integrity_levels,
        )
