import base64
from fastapi.exceptions import HTTPException

from app.shared.models import UserInfo
from app.user import repository as user_repo
from app.user.models import UserCreateDto
from app.shared.utils.db import SqlRunner
from app.auth.models import UserRole

from .models import (
    RegisterRequest,
    RegisterResponse,
    ChallengeResponse,
    LoginRequest,
    LoginResponse,
)
from .utils import (
    generate_login_challenge,
    verify_login_challenge,
    encode_user_token,
    decode_user_token,
)
from .enums import ConfidentialityLevel, SubjectAction


def register_user(req: RegisterRequest, *, db: SqlRunner) -> RegisterResponse:
    dto = UserCreateDto(
        username=req.username,
        access_level=_resolve_access_level(req.role),
        categories=_resolve_subject_categories(req.role),
        public_key=base64.b64decode(req.public_key),
    )
    user_id = user_repo.create_user(dto, db=db)

    return RegisterResponse(user_id=user_id)


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

    payload = UserInfo(
        user_id=user.id, access_level=user.access_level, categories=user.categories
    )
    token = encode_user_token(payload)

    return LoginResponse(token=token)


def authorize_subject(
    *,
    auth_header: str | None,
    subject_action: SubjectAction,
    confidentiality_level: ConfidentialityLevel,
    object_categories: set[str],
) -> UserInfo:
    if not auth_header:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = auth_header.split(" ")[1]
    user = decode_user_token(token=token)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not user.categories & object_categories:
        raise HTTPException(status_code=403, detail="No matching category")

    if (
        subject_action == SubjectAction.READ
        and user.access_level < confidentiality_level.value
    ):
        raise HTTPException(status_code=403, detail="Read access forbidden")

    if (
        subject_action == SubjectAction.WRITE
        and user.access_level > confidentiality_level.value
    ):
        raise HTTPException(status_code=403, detail="Write access forbidden")

    return user


def _resolve_access_level(role: UserRole) -> int:
    match role:
        case UserRole.STUDENT:
            return 2
        case UserRole.CURATOR:
            return 2
        case UserRole.INSTRUCTOR:
            return 3
        case _:
            raise ValueError("Unknown user role")


def _resolve_subject_categories(role: UserRole) -> set[str]:
    match role:
        case UserRole.STUDENT:
            return {"submission"}
        case UserRole.CURATOR:
            return {"preparation"}
        case UserRole.INSTRUCTOR:
            return {"review"}
        case _:
            raise ValueError("Unknown user role")
