from fastapi.exceptions import HTTPException
from datetime import datetime
import base64

from app.shared.utils.db import SqlRunner

from .dto import (
    ChallengeRequest,
    ChallengeResponse,
    LoginRequest,
    LoginResponse,
    UserCreateRequest,
    UserCreateResponse,
    UserResponse,
    UserUpdateRequest,
)
from .utils import (
    generate_login_challenge,
    verify_login_challenge,
    encode_subject_token,
)
from .models import Subject, User
from .enums import AccessLevel, AccessType
from . import repository as auth_repo


def create_login_challenge(
    req: ChallengeRequest, *, db: SqlRunner
) -> ChallengeResponse:
    # Check if user exists and is not expired
    user = auth_repo.get_user_by_id(req.user_id, db=db)

    # Check if user account is expired
    expires_at = datetime.fromisoformat(user.expires_at)
    if expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="User account has expired")

    challenge = generate_login_challenge()
    return ChallengeResponse(challenge=challenge)


def login_user(req: LoginRequest, *, db: SqlRunner) -> LoginResponse:
    user = auth_repo.get_user_by_id(req.user_id, db=db)

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


def create_user(req: UserCreateRequest, *, db: SqlRunner) -> UserCreateResponse:
    user = User(
        name=req.name,
        surname=req.surname,
        email=req.email,
        confidentiality_level=req.confidentiality_level,
        integrity_levels=req.integrity_levels,
        public_key=base64.b64decode(req.public_key),
        expires_at=req.expires_at,
    )

    id = auth_repo.create_user(user, db=db)
    return UserCreateResponse(id=id)


def get_user_by_id(id: int, *, db: SqlRunner) -> UserResponse:
    user = auth_repo.get_user_by_id(id, db=db)

    return UserResponse(
        id=user.id,
        name=user.name,
        surname=user.surname,
        email=user.email,
        confidentiality_level=user.confidentiality_level,
        integrity_levels=user.integrity_levels,
        expires_at=user.expires_at,
    )


def update_user(id: int, req: UserUpdateRequest, *, db: SqlRunner) -> UserResponse:
    # Get existing user to preserve public_key
    existing_user = auth_repo.get_user_by_id(id, db=db)

    user = User(
        id=id,
        name=req.name,
        surname=req.surname,
        email=req.email,
        confidentiality_level=req.confidentiality_level,
        integrity_levels=req.integrity_levels,
        public_key=existing_user.public_key,  # Preserve existing public key
        expires_at=req.expires_at,
    )

    auth_repo.update_user(user, db=db)
    return get_user_by_id(id, db=db)


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
