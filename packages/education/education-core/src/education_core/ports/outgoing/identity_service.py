from typing import Protocol


class IdentityServicePort(Protocol):
    async def verify_student_exists(self, student_id: str) -> bool: ...
