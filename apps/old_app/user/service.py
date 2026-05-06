import base64
from fastapi import HTTPException
from hmp_core.storage import SqlRunner
from .dto import UserCreateRequest, UserUpdateRequest, UserResponse
from . import repository


async def create_user(req: UserCreateRequest, *, db: SqlRunner) -> UserResponse:
    try:
        public_key_bytes = base64.b64decode(req.public_key)
    except Exception:
        raise HTTPException(
            status_code=400, detail="Invalid public key format (expected base64)"
        )

    pseudonym = repository.create_user(req, public_key_bytes, db=db)
    user_data = repository.get_user_by_pseudonym(pseudonym, db=db)

    if not user_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve created user")

    return UserResponse(**user_data)


async def get_user_by_pseudonym(pseudonym: str, *, db: SqlRunner) -> UserResponse:
    user_data = repository.get_user_by_pseudonym(pseudonym, db=db)

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(**user_data)


async def update_user(
    pseudonym: str, req: UserUpdateRequest, *, db: SqlRunner
) -> UserResponse:
    repository.update_user_by_pseudonym(pseudonym, req, db=db)
    user_data = repository.get_user_by_pseudonym(pseudonym, db=db)

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found after update")
    return UserResponse(**user_data)
