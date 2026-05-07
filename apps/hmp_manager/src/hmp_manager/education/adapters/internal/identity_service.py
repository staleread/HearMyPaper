from typing import override

from hmp_manager.education.domain.ports.outgoing import IdentityServicePort
from hmp_manager.identity.domain.ports.outgoing import UserRepositoryPort


class IdentityServiceAdapter(IdentityServicePort):
    def __init__(self, users: UserRepositoryPort):
        self._users = users

    @override
    async def verify_student_exists(self, student_id: str) -> bool:
        user = await self._users.get_by_id(student_id)
        return user is not None
