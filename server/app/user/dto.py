from pydantic import BaseModel

from app.auth.enums import UserRole


class UserResponse(BaseModel):
    id: int
    username: str
    access_level: int
    access_rules: list[str]
    public_key: str


class UserCreateRequest(BaseModel):
    username: str
    role: UserRole
    public_key: bytes


class UserCreateResponse(BaseModel):
    id: int
