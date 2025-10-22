from result import Result, Ok, Err
from pydantic import parse_obj_as

from .dto import (
    ChallengeRequest,
    ChallengeResponse,
    LoginRequest,
    LoginResponse,
)
from ..shared.utils.api import check_response
from ..shared.utils.session import ApiSession


def request_challenge(
    session: ApiSession, req: ChallengeRequest
) -> Result[ChallengeResponse, str]:
    try:
        r = session.post("/auth/challenge", json=req.model_dump())
        result = check_response(r)
        return result.map(lambda data: parse_obj_as(ChallengeResponse, data))
    except Exception as e:
        return Err(f"Network error: {e}")


def submit_challenge(
    session: ApiSession, req: LoginRequest
) -> Result[LoginResponse, str]:
    try:
        r = session.post("/auth/login", json=req.model_dump())
        result = check_response(r)
        if result.is_ok():
            response = parse_obj_as(LoginResponse, result.unwrap())
            session.headers.update({"Authorization": f"Bearer {response.token}"})
            return Ok(response)
        return Err(result.unwrap_err())
    except Exception as e:
        return Err(f"Network error: {e}")
