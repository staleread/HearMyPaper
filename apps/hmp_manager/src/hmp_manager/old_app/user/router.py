import base64
from fastapi import APIRouter, HTTPException, Path, status
from app.shared.dependencies.db import PostgresRunnerDep
from .dto import UserCreateRequest, UserUpdateRequest, UserResponse
from . import service, repository

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(req: UserCreateRequest, db: PostgresRunnerDep):
    """Creates a new user and generates their stable pseudonym."""
    return await service.create_user(req, db=db)


@router.get("/{pseudonym}", response_model=UserResponse)
async def read_user(
    db: PostgresRunnerDep,
    pseudonym: str = Path(..., description="The user's pseudonym"),
):
    """Retrieves user details by pseudonym."""
    return await service.get_user_by_pseudonym(pseudonym, db=db)


@router.put("/{pseudonym}", response_model=UserResponse)
async def update_user(
    req: UserUpdateRequest,
    db: PostgresRunnerDep,
    pseudonym: str = Path(..., description="The user's pseudonym"),
):
    """Updates user details by pseudonym."""
    return await service.update_user(pseudonym, req, db=db)


@router.get("/{pseudonym}/public-key")
async def read_user_public_key(
    db: PostgresRunnerDep,
    pseudonym: str = Path(..., description="The user's pseudonym"),
):
    """
    Returns the public key for a given user pseudonym.
    Used by other workloads for Sealed Box encryption.
    """
    public_key_bytes = repository.get_public_key_by_pseudonym(pseudonym, db=db)
    if not public_key_bytes:
        raise HTTPException(status_code=404, detail="User not found")

    public_key_b64 = base64.b64encode(public_key_bytes).decode("utf-8")
    return {"pseudonym": pseudonym, "public_key": public_key_b64}
