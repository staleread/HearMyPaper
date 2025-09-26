from fastapi import APIRouter

from .models import User

router = APIRouter()


@router.get("/")
async def get_user() -> User:
    return User(id=1, username="Nicolas")
