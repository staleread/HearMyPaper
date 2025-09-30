import requests
from result import Result, Ok, Err

from .api import get_user, get_users, update_user
from .dto import UserUpdateDto, UserResponse, UserListResponse


def get_user_as_response(
    session: requests.Session, user_id: int
) -> Result[UserResponse, str]:
    """
    Get a user by ID.

    Args:
        session: HTTP session for API calls
        user_id: ID of the user to retrieve

    Returns:
        Result containing UserResponse on success or error message on failure
    """
    try:
        api_result = get_user(session, user_id)

        if api_result.is_err():
            return Err(api_result.unwrap_err())

        return Ok(api_result.unwrap())
    except Exception as e:
        return Err(f"Unexpected error retrieving user: {e}")


def get_users_list(session: requests.Session) -> Result[list[UserListResponse], str]:
    """
    Get list of all users.

    Args:
        session: HTTP session for API calls

    Returns:
        Result containing list of UserListResponse on success or error message on failure
    """
    try:
        api_result = get_users(session)

        if api_result.is_err():
            return Err(api_result.unwrap_err())

        return Ok(api_result.unwrap())
    except Exception as e:
        return Err(f"Unexpected error retrieving users: {e}")


def update_user_with_dto(
    session: requests.Session, user_id: int, user_dto: UserUpdateDto
) -> Result[UserResponse, str]:
    """
    Update a user using the form DTO.

    Args:
        session: HTTP session for API calls
        user_id: ID of the user to update
        user_dto: UserUpdateDto with updated user data

    Returns:
        Result containing UserResponse on success or error message on failure
    """
    try:
        update_request = user_dto.to_request()
        api_result = update_user(session, user_id, update_request)

        if api_result.is_err():
            return Err(api_result.unwrap_err())

        return Ok(api_result.unwrap())
    except Exception as e:
        return Err(f"Unexpected error during user update: {e}")
