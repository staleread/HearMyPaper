from pydantic import BaseModel, EmailStr
from hmp_core.auth.enums import AccessLevel
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class UserCreateRequest(UserBase):
    public_key: str  # Base64 encoded


class UserUpdateRequest(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    p_uuid: UUID
    pseudonym: str
    created_at: datetime
