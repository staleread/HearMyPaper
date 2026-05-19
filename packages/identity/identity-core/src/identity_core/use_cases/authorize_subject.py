from typing import override
from ..models import AuthUser
from ..enums import AccessLevel, AccessType
from ..exceptions import AuthorizationError
from ..ports.incoming.authorize_subject import AuthorizeSubjectPort

LEVEL_WEIGHTS = {
    AccessLevel.UNCLASSIFIED: 1,
    AccessLevel.CONTROLLED: 2,
    AccessLevel.RESTRICTED: 3,
    AccessLevel.CONFIDENTIAL: 4,
}


class AuthorizeSubjectUseCase(AuthorizeSubjectPort):
    @override
    def __call__(
        self,
        subject: AuthUser,
        *,
        access_type: AccessType,
        object_access_level: AccessLevel,
    ) -> None:
        """Authorize subject using Bell–LaPadula rules with confidentiality and integrity levels."""

        subject_level = LEVEL_WEIGHTS[subject.confidentiality_level]
        object_level = LEVEL_WEIGHTS[object_access_level]

        # Bell-LaPadula No Read Up rule
        if AccessType.READ in access_type and subject_level < object_level:
            raise AuthorizationError(
                f"Read access forbidden: subject confidentiality level {subject.confidentiality_level} < object level {object_access_level}"
            )

        # Bell-LaPadula No Write Down rule
        if AccessType.WRITE in access_type and subject_level > object_level:
            raise AuthorizationError(
                f"Write access forbidden (no write down): subject confidentiality level {subject.confidentiality_level} > object level {object_access_level}"
            )

        # Integrity level check - subject can only write to levels they are authorized for
        if (
            AccessType.WRITE in access_type
            and object_access_level not in subject.integrity_levels
        ):
            raise AuthorizationError(
                f"Write access forbidden: subject not authorized to write at {object_access_level} level"
            )
