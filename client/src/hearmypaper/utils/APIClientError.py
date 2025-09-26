import requests

class APIClientError(Exception):
    """Raised when the API returns an error response."""

session = requests.Session()
BASE_URL = "http://localhost:8000"

def _check_response(r: requests.Response) -> dict:
    try:
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        raise APIClientError(f"Network error: {e}") from e
    except ValueError as e:
        raise APIClientError(f"Invalid JSON response: {r.text}") from e

    return data


def set_jwt_token(token: str):
    session.headers.update({"Authorization": f"Bearer {token}"})


def register_user(username, role, public_key_b64) -> str:
    payload = {"username": username, "role": role.lower(), "public_key": public_key_b64}
    r = session.post(f"{BASE_URL}/auth/register", json=payload)
    return _check_response(r)["user_id"]


def request_challenge(user_id) -> str:
    payload = {"user_id": user_id}
    r = session.post(f"{BASE_URL}/auth/challenge", json=payload)
    return _check_response(r)["challenge"]


def submit_challenge(user_id, challenge_b64, signed_challenge_b64) -> str:
    payload = {
        "user_id": user_id,
        "challenge": challenge_b64,
        "signature": signed_challenge_b64,
    }
    r = session.post(f"{BASE_URL}/auth/signature", json=payload)
    data = _check_response(r)

    jwt_token = data.get("token")
    if not jwt_token:
        raise APIClientError("Authentication failed: no token returned")


    set_jwt_token(jwt_token)

    return jwt_token
