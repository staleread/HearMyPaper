from fastapi.exceptions import HTTPException

from hmp_core.blp.enums import AccessLevel, AccessType
from hmp_core.blp.models import Subject


def authorize_subject(
    subject: Subject,
    *,
    access_type: AccessType,
    object_access_level: AccessLevel,
) -> None:
    """Authorize subject using Bell–LaPadula rules."""

    # Bell-La Padula "no read up" rule
    if (
        AccessType.READ in access_type
        and subject.confidentiality_level < object_access_level
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                f"Read access forbidden: subject confidentiality level "
                f"{subject.confidentiality_level.name} < object level "
                f"{object_access_level.name}"
            ),
        )

    # Bell-La Padula "no write down" rule
    if (
        AccessType.WRITE in access_type
        and subject.confidentiality_level > object_access_level
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "Write access forbidden (no write down): subject confidentiality "
                f"level {subject.confidentiality_level.name} > object level "
                f"{object_access_level.name}"
            ),
        )

    # Integrity level check - subject can only write to levels they are authorized for
    if (
        AccessType.WRITE in access_type
        and object_access_level not in subject.integrity_levels
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                f"Write access forbidden: subject not authorized to write at "
                f"{object_access_level.name} level"
            ),
        )
