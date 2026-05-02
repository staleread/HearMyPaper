from ..shared.utils.session import ApiSession
from result import Result, Err

from . import api
from .dto import UserUpdateDto, UserResponse, UserListResponse, UserView


def get_user(session: ApiSession, user_id: int) -> Result[UserView, str]:
    return api.get_user(session, user_id).map(UserView.from_response)


def get_users(session: ApiSession) -> Result[list[UserListResponse], str]:
    return api.get_users(session)


def update_user(
    session: ApiSession, user_id: int, user_dto: UserUpdateDto
) -> Result[UserResponse, str]:
    try:
        update_request = user_dto.to_request()

        return api.update_user(session, user_id, update_request)
    except Exception as e:
        return Err(f"Unexpected error during user update: {e}")
