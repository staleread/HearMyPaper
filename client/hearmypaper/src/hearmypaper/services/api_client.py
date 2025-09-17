import requests


class APIClientError(Exception):
    """Raised when the API returns an error response."""


def _check_response(r: requests.Response) -> dict:
    try:
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        raise APIClientError(f"Network error: {e}") from e
    except ValueError as e:
        raise APIClientError(f"Invalid JSON response: {r.text}") from e

    return data


def register_user(username, role, public_key_b64) -> str:
    payload = {"username": username, "role": role.lower(), "public_key": public_key_b64}
    r = requests.post("http://localhost:8000/auth/register", json=payload)

    return _check_response(r)["user_id"]


def request_challenge(user_id) -> str:
    payload = {"user_id": user_id}
    r = requests.post("http://localhost:8000/auth/challenge", json=payload)

    return _check_response(r)["challenge"]


def submit_challenge(user_id, challenge_b64, signed_challenge_b64) -> bool:
    payload = {
        "user_id": user_id,
        "challenge": challenge_b64,
        "signature": signed_challenge_b64,
    }
    r = requests.post("http://localhost:8000/auth/signature", json=payload)

    return _check_response(r)["is_success"]

