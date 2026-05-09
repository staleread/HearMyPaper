from typing import override

from education_core.ports.outgoing import IdentityServicePort
from identity_core.ports.outgoing.user_repository import UserRepositoryPort


class IdentityServiceAdapter(IdentityServicePort):
    def __init__(self, users: UserRepositoryPort):
        self._users = users

    @override
    async def verify_student_exists(self, student_id: str) -> bool:
        user = await self._users.get_by_id(student_id)
        return user is not None
