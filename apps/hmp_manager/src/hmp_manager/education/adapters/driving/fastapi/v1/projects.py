from datetime import datetime
from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hmp_manager.dependencies import UserIdDep, get_postgres
from hmp_manager.education.domain.ports.incoming import (
    GetUserProjectsPort,
    GetProjectPort,
)
from hmp_manager.education.domain.use_cases import (
    GetUserProjectsUseCase,
    GetProjectUseCase,
)
from hmp_manager.education.adapters.driven.postgres import (
    PostgresProjectRepositoryAdapter,
)
from hmp_manager.education.domain.exceptions import ProjectNotFoundError

router = APIRouter()


# DTOs
class ProjectResponse(BaseModel):
    id: UUID
    title: str
    description: str
    instructor_id: str
    deadline: datetime
    created_at: datetime


# Adapters
def get_user_projects_adapter(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
) -> GetUserProjectsPort:
    return GetUserProjectsUseCase(projects=PostgresProjectRepositoryAdapter(postgres))


def get_project_adapter(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
) -> GetProjectPort:
    return GetProjectUseCase(projects=PostgresProjectRepositoryAdapter(postgres))


# Routes
@router.get("/", response_model=list[ProjectResponse])
async def get_projects(
    user_id: UserIdDep,
    use_case: Annotated[GetUserProjectsPort, Depends(get_user_projects_adapter)],
):
    projects = await use_case(user_id)
    return [
        ProjectResponse(
            id=p.id,
            title=p.title,
            description=p.description,
            instructor_id=p.instructor_id,
            deadline=p.deadline,
            created_at=p.created_at,
        )
        for p in projects
    ]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    use_case: Annotated[GetProjectPort, Depends(get_project_adapter)],
):
    try:
        p = await use_case(project_id)
        return ProjectResponse(
            id=p.id,
            title=p.title,
            description=p.description,
            instructor_id=p.instructor_id,
            deadline=p.deadline,
            created_at=p.created_at,
        )
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
