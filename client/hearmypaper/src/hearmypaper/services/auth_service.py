import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .api_client import (
    register_user,
    request_challenge,
    submit_challenge,
    APIClientError,
)
from .credentials_repo import (
    save_user_credentials,
    get_user_credentials,
    CredentialsRepoError,
)


def register(username, role, token_path, password) -> str | None:
    try:
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()

        public_key_bytes = public_key.public_bytes_raw()
        public_key_b64 = base64.b64encode(public_key_bytes).decode("utf-8")

        user_id = register_user(username, role, public_key_b64)

        private_key_bytes = private_key.private_bytes_raw()
        save_user_credentials(user_id, token_path, private_key_bytes, password)

        return None
    except (APIClientError, CredentialsRepoError) as e:
        return str(e)
    except Exception as e:
        return f"Unexpected error during registration: {e}"


def login(token_path, password) -> str | None:
    try:
        user_id, private_key_bytes = get_user_credentials(token_path, password)

        challenge_b64 = request_challenge(user_id)
        challenge_bytes = base64.b64decode(challenge_b64)

        private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
        signed_challenge_bytes = private_key.sign(challenge_bytes)
        signed_challenge_b64 = base64.b64encode(signed_challenge_bytes).decode("utf-8")

        success = submit_challenge(user_id, challenge_b64, signed_challenge_b64)

        if not success:
            return "Authentication failed: invalid signature"

        return None
    except (APIClientError, CredentialsRepoError) as e:
        return str(e)
    except Exception as e:
        return f"Unexpected error during login: {e}"
