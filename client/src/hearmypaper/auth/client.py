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


class APIClientError(Exception):
    """Raised when the API returns an error response."""


s = requests.Session()

# TODO: replace with relative path
s.verify = (
    "/home/mykola/edu/chnu/python-web/HearMyPaper/server/nginx/hearmypaper.edu.crt"
)


def _check_response(r: requests.Response) -> Result[dict, str]:
    try:
        data = r.json()
    except ValueError:
        return Err(f"{r.status_code}: Invalid response format")

    if r.status_code in [200, 201]:
        return Ok(data)
    elif r.status_code == 401:
        return Err("Authentication required. Please log in again.")
    elif r.status_code == 403:
        return Err("Access forbidden. You don't have permission for this operation.")
    elif r.status_code == 404:
        return Err("Resource not found.")
    elif r.status_code >= 500:
        return Err("Server error. Please try again later.")
    else:
        error_message = data.get("detail", "Something went wrong")
        return Err(f"{r.status_code}: {error_message}")


# Auth endpoints
def request_challenge(req: ChallengeRequest) -> Result[ChallengeResponse, str]:
    try:
        r = s.post("https://localhost/auth/challenge", json=req.model_dump())
        result = _check_response(r)
        return result.map(lambda data: ChallengeResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")


def submit_challenge(req: LoginRequest) -> Result[LoginResponse, str]:
    try:
        r = s.post("https://localhost/auth/login", json=req.model_dump())
        result = _check_response(r)
        if result.is_ok():
            response = LoginResponse(**result.unwrap())
            s.headers.update({"Authorization": f"Bearer {response.token}"})
            return Ok(response)
        return Err(result.unwrap_err())
    except Exception as e:
        return Err(f"Network error: {e}")


# User management endpoints
def get_users() -> Result[list[UserListResponse], str]:
    """Get list of users (id and full name only)"""
    try:
        r = s.get("https://localhost/auth/users")
        result = _check_response(r)
        return result.map(lambda data: [UserListResponse(**item) for item in data])
    except Exception as e:
        return Err(f"Network error: {e}")


def get_user(user_id: int) -> Result[UserResponse, str]:
    """Get full user details"""
    try:
        r = s.get(f"https://localhost/auth/users/{user_id}")
        result = _check_response(r)
        return result.map(lambda data: UserResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")


def create_user(req: UserCreateRequest) -> Result[UserCreateResponse, str]:
    """Create a new user"""
    try:
        r = s.post("https://localhost/auth/users", json=req.model_dump())
        result = _check_response(r)
        return result.map(lambda data: UserCreateResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")


def update_user(user_id: int, req: UserUpdateRequest) -> Result[UserResponse, str]:
    """Update an existing user"""
    try:
        r = s.put(f"https://localhost/auth/users/{user_id}", json=req.model_dump())
        result = _check_response(r)
        return result.map(lambda data: UserResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")
