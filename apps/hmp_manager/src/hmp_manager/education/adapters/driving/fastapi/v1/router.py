from fastapi import APIRouter

from .projects import router as projects_router
from .students import router as students_router

router = APIRouter()

router.include_router(projects_router, prefix="/projects", tags=["projects"])
router.include_router(
    students_router, prefix="/projects", tags=["project students"]
)
