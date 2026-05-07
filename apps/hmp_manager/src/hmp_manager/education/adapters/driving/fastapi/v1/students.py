from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hmp_manager.dependencies import get_postgres
from hmp_manager.education.domain.ports.incoming import (
    GetProjectStudentsPort,
    AssignStudentToProjectPort,
    AssignStudentToProjectCommand,
    RemoveStudentFromProjectPort,
    RemoveStudentFromProjectCommand,
)
from hmp_manager.education.domain.use_cases import (
    GetProjectStudentsUseCase,
    AssignStudentToProjectUseCase,
    RemoveStudentFromProjectUseCase,
)
from hmp_manager.education.adapters.driven.postgres import (
    PostgresProjectRepositoryAdapter,
    PostgresProjectStudentRepositoryAdapter,
)
from hmp_manager.education.adapters.internal import IdentityServiceAdapter
from hmp_manager.identity.adapters.driven.postgres import PostgresUserRepositoryAdapter
from hmp_manager.education.domain.exceptions import (
    ProjectNotFoundError,
    StudentNotFoundError,
    StudentAlreadyAssignedError,
    StudentNotAssignedError,
)

router = APIRouter()


# DTOs
class StudentAssignmentRequest(BaseModel):
    student_id: str


class ProjectStudentsResponse(BaseModel):
    student_ids: list[str]


# Adapters
def get_project_students_adapter(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
) -> GetProjectStudentsPort:
    return GetProjectStudentsUseCase(
        projects=PostgresProjectRepositoryAdapter(postgres),
        project_students=PostgresProjectStudentRepositoryAdapter(postgres),
    )


def assign_student_to_project_adapter(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
) -> AssignStudentToProjectPort:
    projects = PostgresProjectRepositoryAdapter(postgres)
    project_students = PostgresProjectStudentRepositoryAdapter(postgres)
    identity = IdentityServiceAdapter(PostgresUserRepositoryAdapter(postgres))

    return AssignStudentToProjectUseCase(
        projects=projects,
        project_students=project_students,
        identity=identity,
    )


def remove_student_from_project_adapter(
    postgres: Annotated[AsyncSession, Depends(get_postgres)],
) -> RemoveStudentFromProjectPort:
    return RemoveStudentFromProjectUseCase(
        projects=PostgresProjectRepositoryAdapter(postgres),
        project_students=PostgresProjectStudentRepositoryAdapter(postgres),
    )


# Routes
@router.get("/{project_id}/students", response_model=ProjectStudentsResponse)
async def get_project_students(
    project_id: UUID,
    use_case: Annotated[GetProjectStudentsPort, Depends(get_project_students_adapter)],
):
    try:
        student_ids = await use_case(project_id)
        return ProjectStudentsResponse(student_ids=student_ids)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{project_id}/students", status_code=status.HTTP_201_CREATED)
async def add_student_to_project(
    project_id: UUID,
    req: StudentAssignmentRequest,
    use_case: Annotated[
        AssignStudentToProjectPort, Depends(assign_student_to_project_adapter)
    ],
):
    cmd = AssignStudentToProjectCommand(
        project_id=project_id, student_id=req.student_id
    )
    try:
        await use_case(cmd)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except StudentAlreadyAssignedError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete(
    "/{project_id}/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_student_from_project(
    project_id: UUID,
    student_id: str,
    use_case: Annotated[
        RemoveStudentFromProjectPort, Depends(remove_student_from_project_adapter)
    ],
):
    cmd = RemoveStudentFromProjectCommand(project_id=project_id, student_id=student_id)
    try:
        await use_case(cmd)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except StudentNotAssignedError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
