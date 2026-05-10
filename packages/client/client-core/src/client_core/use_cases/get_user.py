from ..ports.incoming.get_user import GetUserPort
from ..ports.outgoing.identity import IdentityPort
from ..models import User


class GetUserUseCase(GetUserPort):
    def __init__(self, identity_port: IdentityPort):
        self.identity_port = identity_port

    async def __call__(self, user_id: str) -> User | None:
        return await self.identity_port.get_user(user_id)
