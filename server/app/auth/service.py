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
from .models import Subject, ObjectId
from .enums import AccessLevel, AccessType


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
        id=user.id, access_level=user.access_level, access_rules=user.access_rules
    )
    token = encode_subject_token(subject)

    return LoginResponse(token=token)


def authorize_subject(
    *,
    subject: Subject,
    access_type: AccessType,
    object_id: ObjectId,
    object_access_level: AccessLevel,
) -> Subject:
    """Authorize subject to access an object using Bell–LaPadula rules + explicit access rules."""

    matching_rule = next(
        (rule for rule in subject.access_rules if rule.object_id == object_id),
        None,
    )
    if not matching_rule:
        raise HTTPException(status_code=403, detail="No access rule for this object")

    # Ensure the requested access_type is allowed by the rule
    if not (matching_rule.access & access_type):
        raise HTTPException(status_code=403, detail="Access type not permitted")

    # Enforce Bell–LaPadula rules
    if AccessType.READ in access_type and subject.access_level < object_access_level:
        raise HTTPException(
            status_code=403, detail="Read access forbidden (no read up)"
        )

    if AccessType.WRITE in access_type and subject.access_level > object_access_level:
        raise HTTPException(
            status_code=403, detail="Write access forbidden (no write down)"
        )

    return subject
