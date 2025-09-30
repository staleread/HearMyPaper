import requests
from result import Result, Ok, Err

from .dto import (
    ChallengeRequest,
    ChallengeResponse,
    LoginRequest,
    LoginResponse,
)
from ..shared.utils.api import check_response


def request_challenge(
    session: requests.Session, req: ChallengeRequest
) -> Result[ChallengeResponse, str]:
    try:
        r = session.post("https://localhost/auth/challenge", json=req.model_dump())
        result = check_response(r)
        return result.map(lambda data: ChallengeResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")


def submit_challenge(
    session: requests.Session, req: LoginRequest
) -> Result[LoginResponse, str]:
    try:
        r = session.post("https://localhost/auth/login", json=req.model_dump())
        result = check_response(r)
        if result.is_ok():
            response = LoginResponse(**result.unwrap())
            session.headers.update({"Authorization": f"Bearer {response.token}"})
            return Ok(response)
        return Err(result.unwrap_err())
    except Exception as e:
        return Err(f"Network error: {e}")
