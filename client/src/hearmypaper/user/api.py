import requests
from result import Result, Err

from .dto import (
    UserCreateRequest,
    UserCreateResponse,
    UserUpdateRequest,
    UserResponse,
    UserListResponse,
)
from ..shared.utils.api import check_response


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
