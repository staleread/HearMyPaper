from ..shared.utils.session import ApiSession
from result import Result, Err
from pydantic import parse_obj_as

from .dto import (
    UserCreateRequest,
    UserCreateResponse,
    UserUpdateRequest,
    UserResponse,
    UserListResponse,
)
from ..shared.utils.api import check_response


def get_users(session: ApiSession) -> Result[list[UserListResponse], str]:
    try:
        r = session.get("/auth/users")
        result = check_response(r)
        return result.map(lambda data: parse_obj_as(list[UserListResponse], data))
    except Exception as e:
        return Err(f"Network error: {e}")


def get_user(session: ApiSession, user_id: int) -> Result[UserResponse, str]:
    try:
        r = session.get(f"/auth/users/{user_id}")
        result = check_response(r)
        return result.map(lambda data: parse_obj_as(UserResponse, data))
    except Exception as e:
        return Err(f"Network error: {e}")


def create_user(
    session: ApiSession, req: UserCreateRequest
) -> Result[UserCreateResponse, str]:
    try:
        r = session.post("/auth/users", json=req.model_dump())
        result = check_response(r)
        return result.map(lambda data: parse_obj_as(UserCreateResponse, data))
    except Exception as e:
        return Err(f"Network error: {e}")


def update_user(
    session: ApiSession, user_id: int, req: UserUpdateRequest
) -> Result[UserResponse, str]:
    try:
        r = session.put(f"/auth/users/{user_id}", json=req.model_dump())
        result = check_response(r)
        return result.map(lambda data: parse_obj_as(UserResponse, data))
    except Exception as e:
        return Err(f"Network error: {e}")
