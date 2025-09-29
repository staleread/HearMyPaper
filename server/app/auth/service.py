from fastapi.exceptions import HTTPException

from app.user import repository as user_repo
from app.shared.utils.db import SqlRunner

from .dto import (
    ChallengeResponse,
    LoginRequest,
    LoginResponse,
)
from .utils import (
    generate_login_challenge,
    verify_login_challenge,
    encode_subject_token,
)
from .models import Subject
from .enums import AccessLevel, AccessType, UserRole


def get_access_by_role(role: UserRole) -> tuple[AccessLevel, list[AccessLevel]]:
    """
    Define security policy: confidentiality level and integrity levels for each role.
    Business logic that determines what each role can read and write.
    """
    match role:
        case UserRole.STUDENT:
            # Students can read up to CONTROLLED and can write submissions at RESTRICTED level
            return (
                AccessLevel.CONTROLLED,
                [AccessLevel.RESTRICTED],
            )
        case UserRole.CURATOR:
            # Curators can read up to CONTROLLED and can write course-project info at CONTROLLED level
            return (
                AccessLevel.CONTROLLED,
                [AccessLevel.CONTROLLED],
            )
        case UserRole.INSTRUCTOR:
            # Instructors can read up to RESTRICTED but cannot write anything (read-only)
            return (
                AccessLevel.RESTRICTED,
                [],
            )
        case _:
            raise ValueError("Unknown user role")


def create_login_challenge() -> ChallengeResponse:
    challenge = generate_login_challenge()
    return ChallengeResponse(challenge=challenge)


def login_user(req: LoginRequest, *, db: SqlRunner) -> LoginResponse:
    user = user_repo.get_user_by_id(req.user_id, db=db)

    is_success = verify_login_challenge(
        signature_b64=req.signature,
        challenge_b64=req.challenge,
        public_key_bytes=user.public_key,
    )

    if not is_success:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    subject = Subject(
        id=user.id,
        confidentiality_level=user.confidentiality_level,
        integrity_levels=user.integrity_levels,
    )
    token = encode_subject_token(subject)

    return LoginResponse(token=token)


def authorize_subject(
    subject: Subject,
    *,
    access_type: AccessType,
    object_access_level: AccessLevel,
) -> None:
    """Authorize subject using Bell–LaPadula rules with confidentiality and integrity levels."""

    # Bell-LaPadula No Read Up rule
    if (
        AccessType.READ in access_type
        and subject.confidentiality_level < object_access_level
    ):
        raise HTTPException(
            status_code=403,
            detail=f"Read access forbidden: subject confidentiality level {subject.confidentiality_level.name} < object level {object_access_level.name}",
        )

    # Bell-LaPadula No Write Down rule
    if (
        AccessType.WRITE in access_type
        and subject.confidentiality_level > object_access_level
    ):
        raise HTTPException(
            status_code=403,
            detail=f"Write access forbidden (no write down): subject confidentiality level {subject.confidentiality_level.name} > object level {object_access_level.name}",
        )

    # Integrity level check - subject can only write to levels they are authorized for
    if (
        AccessType.WRITE in access_type
        and object_access_level not in subject.integrity_levels
    ):
        raise HTTPException(
            status_code=403,
            detail=f"Write access forbidden: subject not authorized to write at {object_access_level.name} level",
        )
