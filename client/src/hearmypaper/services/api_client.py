import requests


class APIClientError(Exception):
    """Raised when the API returns an error response."""


s = requests.Session()

# TODO: replace with relative path
s.verify = (
    "/home/mykola/edu/chnu/python-web/HearMyPaper/server/nginx/hearmypaper.edu.crt"
)


def _check_response(r: requests.Response) -> dict:
    data = r.json()

    if r.status_code == 200:
        return data

    raise APIClientError(f"{r.status_code}: {data['detail'] or 'Something went wrong'}")


def register_user(username, role, public_key_b64) -> str:
    payload = {"username": username, "role": role.lower(), "public_key": public_key_b64}
    r = s.post("https://localhost/user/register", json=payload)

    return _check_response(r)["id"]


def request_challenge(user_id) -> str:
    payload = {"user_id": user_id}
    r = s.post("https://localhost/auth/challenge", json=payload)

    return _check_response(r)["challenge"]


def submit_challenge(user_id, challenge_b64, signed_challenge_b64):
    payload = {
        "user_id": user_id,
        "challenge": challenge_b64,
        "signature": signed_challenge_b64,
    }
    r = s.post("https://localhost/auth/login", json=payload)

    token = _check_response(r)["token"]

    # TODO: remove this
    print(f'Token: "{token}"')

    s.headers.update({"Authorization": f"Bearer {token}"})
