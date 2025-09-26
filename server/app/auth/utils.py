import os
import jwt
import base64

from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

from app.shared.config.env import env_settings
from app.shared.models import UserInfo


def generate_login_challenge() -> str:
    return base64.b64encode(os.urandom(256)).decode("utf-8")


def verify_login_challenge(
    *, signature_b64: str, challenge_b64: str, public_key_b64: str
) -> bool:
    try:
        signature_bytes = base64.b64decode(signature_b64)
        challenge_bytes = base64.b64decode(challenge_b64)
        public_key_bytes = base64.b64decode(public_key_b64)

        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
        public_key.verify(signature_bytes, challenge_bytes)

        return True
    except InvalidSignature:
        return False


def encode_user_token(payload: UserInfo) -> str:
    moment = datetime.now(tz=timezone.utc) + timedelta(
        seconds=env_settings.jwt.lifetime
    )

    data = {
        "exp": int(moment.timestamp()),
        **payload.model_dump(),
    }
    return jwt.encode(
        data, env_settings.jwt.secret, algorithm=env_settings.jwt.algorithm
    )


def decode_user_token(token: str) -> UserInfo | None:
    try:
        payload = jwt.decode(
            token, env_settings.jwt.secret, algorithms=[env_settings.jwt.algorithm]
        )
        return UserInfo(
            user_id=payload.user_id,
            role=payload.role,
            access_level=payload.access_level,
            categories=set(payload.categories),
        )
    except jwt.ExpiredSignatureError:
        return None
