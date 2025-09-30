import base64
import requests
from result import Result, Ok, Err
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .api import (
    request_challenge,
    submit_challenge,
    create_user,
)
from .utils import (
    save_user_credentials,
    get_user_credentials,
    CredentialsRepoError,
)
from .dto import ChallengeRequest, LoginRequest, UserCreateDto, UserCreateResponse


def create_user_with_credentials(
    session: requests.Session, user_dto: UserCreateDto
) -> Result[UserCreateResponse, str]:
    """
    Create a user with auto-generated key pair and save credentials to file.

    Args:
        session: HTTP session for API calls
        user_dto: UserCreateDto with all user data and credential info

    Returns:
        Result containing UserCreateResponse on success or error message on failure
    """
    try:
        # Generate key pair
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()

        public_key_bytes = public_key.public_bytes_raw()
        public_key_b64 = base64.b64encode(public_key_bytes).decode("utf-8")

        # Convert DTO to API request
        create_request = user_dto.to_request(public_key_b64)
        api_result = create_user(session, create_request)

        if api_result.is_err():
            return Err(api_result.unwrap_err())

        response = api_result.unwrap()

        # Save credentials to file
        private_key_bytes = private_key.private_bytes_raw()
        save_user_credentials(
            str(response.id),
            user_dto.credentials_path,
            private_key_bytes,
            user_dto.credentials_password,
        )

        return Ok(response)
    except CredentialsRepoError as e:
        return Err(str(e))
    except Exception as e:
        return Err(f"Unexpected error during user creation: {e}")


def login(
    session: requests.Session, token_path: str, password: str
) -> Result[None, str]:
    """
    Authenticate user with credentials file.

    Args:
        session: HTTP session for API calls

    Returns:
        Result containing None on success or error message on failure
    """
    try:
        user_id, private_key_bytes = get_user_credentials(token_path, password)

        # Create challenge request
        challenge_req = ChallengeRequest(user_id=int(user_id))
        challenge_result = request_challenge(session, challenge_req)

        if challenge_result.is_err():
            return Err(challenge_result.unwrap_err())

        challenge_resp = challenge_result.unwrap()
        challenge_bytes = base64.b64decode(challenge_resp.challenge)

        private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
        signed_challenge_bytes = private_key.sign(challenge_bytes)
        signed_challenge_b64 = base64.b64encode(signed_challenge_bytes).decode("utf-8")

        # Submit login request
        login_req = LoginRequest(
            user_id=int(user_id),
            challenge=challenge_resp.challenge,
            signature=signed_challenge_b64,
        )
        login_result = submit_challenge(session, login_req)

        if login_result.is_err():
            return Err(login_result.unwrap_err())

        return Ok(None)
    except CredentialsRepoError as e:
        return Err(str(e))
    except Exception as e:
        return Err(f"Unexpected error during login: {e}")
