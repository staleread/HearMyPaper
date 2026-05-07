from fastapi import APIRouter

from .login import router as login_router
from .users import router as users_router

router = APIRouter()

router.include_router(login_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])
