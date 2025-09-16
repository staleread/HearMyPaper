import os
import base64

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature


def generate_challenge() -> str:
    return base64.b64encode(os.urandom(256)).decode("utf-8")


def verify_signed_challenge(
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
