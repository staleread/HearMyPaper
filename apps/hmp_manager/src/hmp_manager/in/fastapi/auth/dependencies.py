from typing import Annotated, Any
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from hmp_manager.domain.auth.service import AuthService
from hmp_manager.out.postgres import PostgresAuthRepository
from hmp_manager.out.redis import RedisChallengeRepository
from hmp_manager.out.jwt import JwtTokenProvider

from ..dependencies import get_postgres, get_redis


def get_auth_service(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
    redis: Annotated[Redis[Any], Depends(get_redis)],
) -> AuthService:
    users = PostgresAuthRepository(postgres)
    challenges = RedisChallengeRepository(redis)
    tokens = JwtTokenProvider()

    return AuthService(users=users, challenges=challenges, tokens=tokens)
