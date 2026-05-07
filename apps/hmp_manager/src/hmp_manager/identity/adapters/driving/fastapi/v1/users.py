from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from hmp_core.utils import to_b64, from_b64
from hmp_manager.dependencies import get_postgres

from hmp_manager.identity.domain.enums import AccessLevel
from hmp_manager.identity.domain.ports.incoming import (
    CreateUserPort,
    UserCreateCommand,
    GetUserPort,
    GetUserPublicKeyPort,
    UpdateUserPort,
    UserUpdateCommand,
)
from hmp_manager.identity.domain.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    IdentityCollisionError,
)
from hmp_manager.identity.domain.use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    GetUserPublicKeyUseCase,
    UpdateUserUseCase,
)
from hmp_manager.identity.adapters.driven.postgres import PostgresUserRepositoryAdapter
from hmp_manager.identity.adapters.driven.identity import (
    PseudonymIdentityProviderAdapter,
)

router = APIRouter()


class UserCreateRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    public_key_b64: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class UserUpdateRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class UserResponse(BaseModel):
    id: str
    name: str
    surname: str
    email: EmailStr
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    created_at: datetime


class PublicKeyResponse(BaseModel):
    public_key_b64: str


def create_user_adapter(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
) -> CreateUserPort:
    return CreateUserUseCase(
        users=PostgresUserRepositoryAdapter(postgres),
        id_provider=PseudonymIdentityProviderAdapter(),
    )


def get_user_adapter(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
) -> GetUserPort:
    return GetUserUseCase(
        users=PostgresUserRepositoryAdapter(postgres),
    )


def get_user_public_key_adapter(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
) -> GetUserPublicKeyPort:
    return GetUserPublicKeyUseCase(
        users=PostgresUserRepositoryAdapter(postgres),
    )


def update_user_adapter(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
) -> UpdateUserPort:
    return UpdateUserUseCase(
        users=PostgresUserRepositoryAdapter(postgres),
    )


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    req: UserCreateRequest,
    create_user_uc: Annotated[CreateUserPort, Depends(create_user_adapter)],
):
    try:
        cmd = UserCreateCommand(
            name=req.name,
            surname=req.surname,
            email=req.email,
            public_key=from_b64(req.public_key_b64),
            confidentiality_level=req.confidentiality_level,
            integrity_levels=req.integrity_levels,
        )
        user = await create_user_uc(cmd)
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
    get_user_uc: Annotated[GetUserPort, Depends(get_user_adapter)],
):
    try:
        user = await get_user_uc(user_id)
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
    get_user_public_key_uc: Annotated[
        GetUserPublicKeyPort, Depends(get_user_public_key_adapter)
    ],
):
    try:
        public_key = await get_user_public_key_uc(user_id)
        return PublicKeyResponse(public_key_b64=to_b64(public_key))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    req: UserUpdateRequest,
    update_user_uc: Annotated[UpdateUserPort, Depends(update_user_adapter)],
):
    try:
        cmd = UserUpdateCommand(
            name=req.name,
            surname=req.surname,
            email=req.email,
            confidentiality_level=req.confidentiality_level,
            integrity_levels=req.integrity_levels,
        )
        user = await update_user_uc(user_id, cmd)
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
