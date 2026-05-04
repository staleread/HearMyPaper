import os
import base64
import jwt
from datetime import datetime, timedelta, timezone
from hmp_core.crypto import crypto
from app.shared.config.env import get_env_settings


def generate_challenge() -> str:
    """Generates a random 32-byte challenge encoded in base64."""
    return base64.b64encode(os.urandom(32)).decode("utf-8")


def verify_challenge(
    signature_b64: str, challenge_b64: str, public_key_bytes: bytes
) -> bool:
    """Verifies an Ed25519 signature over a challenge."""
    try:
        signature = base64.b64decode(signature_b64)
        challenge = base64.b64decode(challenge_b64)
        return crypto.verify(
            challenge, signature=signature, public_key_bytes=public_key_bytes
        )
    except Exception:
        return False


def create_access_token(data: dict) -> str:
    """Creates a JWT access token."""
    settings = get_env_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.jwt_lifetime_sec)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
