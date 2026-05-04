from fastapi import APIRouter, Depends
from app.shared.dependencies.db import PostgresRunnerDep
from app.shared.dependencies.redis import get_redis
from redis import asyncio as aioredis
from .dto import ChallengeRequest, ChallengeResponse, LoginRequest, LoginResponse
from . import service

router = APIRouter()


@router.post("/challenge", response_model=ChallengeResponse)
async def create_challenge(
    req: ChallengeRequest,
    db: PostgresRunnerDep,
    redis: aioredis.Redis = Depends(get_redis),
):
    """Generates a login challenge for the user."""
    return await service.create_challenge(req, redis=redis, db=db)


@router.post("/login", response_model=LoginResponse)
async def execute_login(
    req: LoginRequest, db: PostgresRunnerDep, redis: aioredis.Redis = Depends(get_redis)
):
    """Verifies the challenge signature and issues a JWT."""
    return await service.login(req, redis=redis, db=db)
