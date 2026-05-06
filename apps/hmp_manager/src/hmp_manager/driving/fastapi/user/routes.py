from fastapi import APIRouter, HTTPException

from hmp_manager.domain.user.models import UserCreate, UserUpdate
from hmp_manager.domain.user.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    IdentityCollisionError,
)
from hmp_manager.driving.fastapi.utils import to_b64, from_b64
from .dependencies import UserServiceDep
from .dto import (
    UserCreateRequest,
    UserUpdateRequest,
    UserResponse,
    PublicKeyResponse,
)

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    req: UserCreateRequest,
    service: UserServiceDep,
):
    try:
        cmd = UserCreate(
            name=req.name,
            surname=req.surname,
            email=req.email,
            public_key=from_b64(req.public_key_b64),
            confidentiality_level=req.confidentiality_level,
            integrity_levels=req.integrity_levels,
        )
        user = await service.create_user(cmd)
        return UserResponse(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            confidentiality_level=user.confidentiality_level,
            integrity_levels=user.integrity_levels,
            created_at=user.created_at,
        )
    except (UserAlreadyExistsError, IdentityCollisionError) as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    service: UserServiceDep,
):
    try:
        user = await service.get_user(user_id)
        return UserResponse(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            confidentiality_level=user.confidentiality_level,
            integrity_levels=user.integrity_levels,
            created_at=user.created_at,
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{user_id}/public-key", response_model=PublicKeyResponse)
async def get_user_public_key(
    user_id: str,
    service: UserServiceDep,
):
    try:
        public_key = await service.get_user_public_key(user_id)
        return PublicKeyResponse(public_key_b64=to_b64(public_key))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    req: UserUpdateRequest,
    service: UserServiceDep,
):
    try:
        cmd = UserUpdate(
            name=req.name,
            surname=req.surname,
            email=req.email,
            confidentiality_level=req.confidentiality_level,
            integrity_levels=req.integrity_levels,
        )
        user = await service.update_user(user_id, cmd)
        return UserResponse(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            confidentiality_level=user.confidentiality_level,
            integrity_levels=user.integrity_levels,
            created_at=user.created_at,
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
