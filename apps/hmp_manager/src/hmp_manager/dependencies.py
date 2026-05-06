import jwt
from functools import lru_cache
from typing import Annotated
from hmp_core.storage import PostgresEngine, RedisClient
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from hmp_manager.config import get_settings

security = HTTPBearer()


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> str:
    try:
        settings = get_settings().jwt
        payload = jwt.decode(
            credentials.credentials, settings.secret, algorithms=settings.algorithm
        )
        user_id: str | None = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing subject (sub)",
            )
        return user_id

    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


UserIdDep = Annotated[str, Depends(get_current_user_id)]


@lru_cache
def get_postgres_engine() -> PostgresEngine:
    return PostgresEngine(get_settings().postgres.url)


async def get_postgres():
    engine = get_postgres_engine()

    async for session in engine.get_session():
        yield session


@lru_cache
def get_redis_service() -> RedisClient:
    return RedisClient(get_settings().redis.url)


async def get_redis():
    service = get_redis_service()
    async for client in service.get_client():
        yield client
