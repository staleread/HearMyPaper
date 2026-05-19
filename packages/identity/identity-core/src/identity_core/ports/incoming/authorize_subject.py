from typing import Protocol
from ...models import AuthUser
from ...enums import AccessLevel, AccessType


class AuthorizeSubjectPort(Protocol):
    def __call__(
        self,
        subject: AuthUser,
        *,
        access_type: AccessType,
        object_access_level: AccessLevel,
    ) -> None: ...
