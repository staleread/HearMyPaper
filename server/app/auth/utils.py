import os
import jwt
import base64

from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

from app.shared.config.env import env_settings

from .models import Subject, AccessRule
from .enums import AccessLevel, UserRole


def generate_login_challenge() -> str:
    return base64.b64encode(os.urandom(256)).decode("utf-8")


def verify_login_challenge(
    *, signature_b64: str, challenge_b64: str, public_key_bytes: bytes
) -> bool:
    try:
        signature_bytes = base64.b64decode(signature_b64)
        challenge_bytes = base64.b64decode(challenge_b64)

        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
        public_key.verify(signature_bytes, challenge_bytes)

        return True
    except InvalidSignature:
        return False


def encode_subject_token(subject: Subject) -> str:
    moment = datetime.now(tz=timezone.utc) + timedelta(
        seconds=env_settings.jwt_lifetime_sec
    )

    data = {
        "exp": int(moment.timestamp()),
        "subject_id": subject.id,
        "access_level": subject.access_level.value,
        "access_rules": [str(rule) for rule in subject.access_rules],
    }
    return jwt.encode(
        data, env_settings.jwt_secret, algorithm=env_settings.jwt_algorithm
    )


def decode_subject_token(token: str) -> Subject | None:
    try:
        payload = jwt.decode(
            token, env_settings.jwt_secret, algorithms=[env_settings.jwt_algorithm]
        )
        return Subject(
            id=payload.subject_id,
            access_level=AccessLevel(payload.access_level),
            access_rules=[AccessRule.parse(rule) for rule in payload.access_rules],
        )
    except jwt.ExpiredSignatureError:
        return None


def get_access_level_by_role(role: UserRole) -> AccessLevel:
    match role:
        case UserRole.STUDENT:
            return AccessLevel.CONTROLLED
        case UserRole.CURATOR:
            return AccessLevel.CONTROLLED
        case UserRole.INSTRUCTOR:
            return AccessLevel.RESTRICTED
        case _:
            raise ValueError("Unknown user role")
