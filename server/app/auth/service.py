from sqlalchemy import Connection
from fastapi.exceptions import HTTPException

from app.shared.models import UserInfo
from app.user import service as user_service

from .models import (
    RegisterRequest,
    RegisterResponse,
    ChallengeResponse,
    LoginRequest,
    LoginResponse,
)
from .utils import generate_login_challenge, verify_login_challenge, encode_user_token

# TODO: remove this
public_keys = dict()


def register_user(req: RegisterRequest, *, connection: Connection) -> RegisterResponse:
    user_id = 1
    public_keys[user_id] = req.public_key

    return RegisterResponse(user_id=user_id)


def create_login_challenge() -> ChallengeResponse:
    challenge = generate_login_challenge()
    return ChallengeResponse(challenge=challenge)


def login_user(req: LoginRequest, *, connection: Connection) -> LoginResponse:
    public_key_b64 = public_keys[req.user_id]
    is_success = verify_login_challenge(
        signature_b64=req.signature,
        challenge_b64=req.challenge,
        public_key_b64=public_key_b64,
    )

    if not is_success:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user = user_service.get_user_by_id(req.user_id, connection=connection)

    payload = UserInfo(
        user_id=user.id, access_level=user.access_level, categories=user.categories
    )
    token = encode_user_token(payload)

    return LoginResponse(token=token)
