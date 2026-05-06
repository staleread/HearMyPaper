from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from hmp_manager.dependencies import UserIdDep
from hmp_manager.education.domain.exceptions import (
    ProjectNotFoundError,
    StudentNotFoundError,
    StudentAlreadyAssignedError,
    StudentNotAssignedError,
)
from .dependencies import ProjectServiceDep
from .dto import (
    ProjectResponse,
    StudentAssignmentRequest,
    ProjectStudentsResponse,
)

router = APIRouter()


@router.get("/projects", response_model=list[ProjectResponse])
async def get_projects(
    user_id: UserIdDep,
    service: ProjectServiceDep,
):
    projects = await service.get_projects(user_id)
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


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    service: ProjectServiceDep,
):
    try:
        p = await service.get_project(project_id)
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


@router.get("/projects/{project_id}/students", response_model=ProjectStudentsResponse)
async def get_project_students(
    project_id: UUID,
    service: ProjectServiceDep,
):
    try:
        student_ids = await service.get_project_students(project_id)
        return ProjectStudentsResponse(student_ids=student_ids)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/projects/{project_id}/students", status_code=status.HTTP_201_CREATED)
async def add_student_to_project(
    project_id: UUID,
    req: StudentAssignmentRequest,
    service: ProjectServiceDep,
):
    try:
        await service.add_student_to_project(project_id, req.student_id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except StudentAlreadyAssignedError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete(
    "/projects/{project_id}/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_student_from_project(
    project_id: UUID,
    student_id: str,
    service: ProjectServiceDep,
):
    try:
        await service.remove_student_from_project(project_id, student_id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except StudentNotAssignedError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
