import requests
from result import Result, Ok, Err

from .dto import (
    ChallengeRequest,
    ChallengeResponse,
    LoginRequest,
    LoginResponse,
    UserCreateRequest,
    UserCreateResponse,
    UserUpdateRequest,
    UserResponse,
    UserListResponse,
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


def get_users(session: requests.Session) -> Result[list[UserListResponse], str]:
    """Get list of users (id and full name only)"""
    try:
        r = session.get("https://localhost/auth/users")
        result = check_response(r)
        return result.map(lambda data: [UserListResponse(**item) for item in data])
    except Exception as e:
        return Err(f"Network error: {e}")


def get_user(session: requests.Session, user_id: int) -> Result[UserResponse, str]:
    """Get full user details"""
    try:
        r = session.get(f"https://localhost/auth/users/{user_id}")
        result = check_response(r)
        return result.map(lambda data: UserResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")


def create_user(
    session: requests.Session, req: UserCreateRequest
) -> Result[UserCreateResponse, str]:
    """Create a new user"""
    try:
        r = session.post("https://localhost/auth/users", json=req.model_dump())
        result = check_response(r)
        return result.map(lambda data: UserCreateResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")


def update_user(
    session: requests.Session, user_id: int, req: UserUpdateRequest
) -> Result[UserResponse, str]:
    """Update an existing user"""
    try:
        r = session.put(
            f"https://localhost/auth/users/{user_id}", json=req.model_dump()
        )
        result = check_response(r)
        return result.map(lambda data: UserResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")
