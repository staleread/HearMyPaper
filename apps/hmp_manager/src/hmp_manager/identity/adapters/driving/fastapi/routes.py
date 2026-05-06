from fastapi import APIRouter

from .auth.routes import router as auth_router
from .user.routes import router as users_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(users_router)
