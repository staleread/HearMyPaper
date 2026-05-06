from typing import Annotated, Any
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from hmp_manager.dependencies import get_postgres, get_redis
from hmp_manager.identity.domain.services import AuthService
from hmp_manager.identity.adapters.driven.postgres import PostgresAuthRepository
from hmp_manager.identity.adapters.driven.redis import RedisChallengeRepository
from hmp_manager.identity.adapters.driven.jwt import JwtTokenProvider


def get_auth_service(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
    redis: Annotated[Redis[Any], Depends(get_redis)],
) -> AuthService:
    users = PostgresAuthRepository(postgres)
    challenges = RedisChallengeRepository(redis)
    tokens = JwtTokenProvider()

    return AuthService(users=users, challenges=challenges, tokens=tokens)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
