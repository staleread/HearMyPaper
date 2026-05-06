from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hmp_manager.identity.domain.services import UserService
from hmp_manager.identity.adapters.driven.postgres.user_repository import (
    PostgresUserRepository,
)
from hmp_manager.identity.adapters.driven.identity import PseudonymIdentityProvider
from hmp_manager.identity.adapters.driving.fastapi.dependencies import get_postgres


def get_user_service(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
) -> UserService:
    users = PostgresUserRepository(postgres)
    id_provider = PseudonymIdentityProvider()

    return UserService(users=users, id_provider=id_provider)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
