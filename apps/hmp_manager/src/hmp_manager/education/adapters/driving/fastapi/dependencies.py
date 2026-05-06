from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hmp_manager.dependencies import get_postgres
from hmp_manager.education.domain.services import ProjectService
from hmp_manager.education.adapters.driven.postgres import (
    PostgresProjectRepository,
    PostgresProjectStudentRepository,
)
from hmp_manager.education.adapters.internal import IdentityServiceAdapter
from hmp_manager.identity.adapters.driven.postgres import PostgresUserRepository


def get_project_service(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
) -> ProjectService:
    projects = PostgresProjectRepository(postgres)
    project_students = PostgresProjectStudentRepository(postgres)

    # Internal adapter for identity validation
    user_repo = PostgresUserRepository(postgres)
    identity = IdentityServiceAdapter(user_repo)

    return ProjectService(
        projects=projects,
        project_students=project_students,
        identity=identity,
    )


ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]
