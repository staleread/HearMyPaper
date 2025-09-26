from fastapi import HTTPException, Header
from typing import Annotated

from app.shared.models import UserInfo
from app.auth.utils import decode_user_token


def get_authorized_user(*, access_level=int, categories: set[str]):
    def get_user(authorization: Annotated[str | None, Header()] = None) -> UserInfo:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split(" ")[1]
        user = decode_user_token(token=token)

        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if user.access_level < access_level or not user.categories & categories:
            raise HTTPException(status_code=403, detail="Forbidden")

        return user

    return get_user
