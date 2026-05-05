import os
import jwt
from datetime import datetime, timedelta, timezone
from hmp_core import crypto
from app.shared.config.env import get_env_settings


def generate_challenge() -> bytes:
    return os.urandom(32)


def verify_signature(signature: bytes, challenge: bytes, public_key: bytes) -> bool:
    return crypto.verify(challenge, signature=signature, public_key_bytes=public_key)


def create_access_token(data: dict) -> str:
    """Creates a JWT access token."""
    settings = get_env_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.jwt_lifetime_sec)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
