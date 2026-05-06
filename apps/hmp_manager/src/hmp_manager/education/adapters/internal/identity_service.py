from typing import override

from hmp_manager.education.domain.ports import IdentityService
from hmp_manager.identity.domain.ports import UserRepository


class IdentityServiceAdapter(IdentityService):
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    @override
    async def verify_student_exists(self, student_id: str) -> bool:
        user = await self._user_repo.get_by_id(student_id)
        return user is not None
