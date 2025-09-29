from pydantic import BaseModel

from app.auth.enums import UserRole


class UserResponse(BaseModel):
    id: int
    username: str
    confidentiality_level: int
    integrity_levels: list[int]
    public_key: str


class UserCreateRequest(BaseModel):
    username: str
    role: UserRole
    public_key: bytes


class UserCreateResponse(BaseModel):
    id: int
