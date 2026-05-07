from typing import Annotated, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from hmp_core.utils import to_b64, from_b64
from hmp_manager.dependencies import get_postgres, get_redis

from hmp_manager.identity.domain.ports.incoming import (
    InitLoginPort,
    FinalizeLoginPort,
    LoginCommand,
)
from hmp_manager.identity.domain.exceptions import (
    UserNotFoundError,
    InvalidChallengeError,
    AuthenticationFailedError,
)
from hmp_manager.identity.domain.use_cases import InitLoginUseCase, FinalizeLoginUseCase
from hmp_manager.identity.adapters.driven.postgres import PostgresAuthRepositoryAdapter
from hmp_manager.identity.adapters.driven.redis import RedisChallengeRepositoryAdapter
from hmp_manager.identity.adapters.driven.jwt import JwtTokenProviderAdapter


router = APIRouter()


class ChallengeRequest(BaseModel):
    id: str


class ChallengeResponse(BaseModel):
    challenge_b64: str


class LoginRequest(BaseModel):
    id: str
    challenge_b64: str
    signature_b64: str


class LoginResponse(BaseModel):
    token: str


def init_login_adapter(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
    redis: Annotated[Redis[Any], Depends(get_redis)],
) -> InitLoginPort:
    return InitLoginUseCase(
        users=PostgresAuthRepositoryAdapter(postgres),
        challenges=RedisChallengeRepositoryAdapter(redis),
    )


def finalize_login_adapter(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
    redis: Annotated[Redis[Any], Depends(get_redis)],
) -> FinalizeLoginPort:
    return FinalizeLoginUseCase(
        users=PostgresAuthRepositoryAdapter(postgres),
        challenges=RedisChallengeRepositoryAdapter(redis),
        tokens=JwtTokenProviderAdapter(),
    )


@router.post("/challenge", response_model=ChallengeResponse)
async def create_challenge(
    req: ChallengeRequest,
    init_login: Annotated[InitLoginPort, Depends(init_login_adapter)],
):
    try:
        challenge_bytes = await init_login(req.id)
        return ChallengeResponse(challenge_b64=to_b64(challenge_bytes))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def execute_login(
    req: LoginRequest,
    finalize_login: Annotated[FinalizeLoginPort, Depends(finalize_login_adapter)],
):
    cmd = LoginCommand(
        id=req.id,
        challenge=from_b64(req.challenge_b64),
        signature=from_b64(req.signature_b64),
    )

    try:
        auth_token = await finalize_login(cmd)
        return LoginResponse(token=auth_token.token)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidChallengeError, AuthenticationFailedError:
        raise HTTPException(
            status_code=401,
            detail="Invalid challenge or signature",
        )
