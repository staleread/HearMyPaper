from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from ..shared.enums import AccessLevel


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
    p_uuid: UUID
    pseudonym: str
    created_at: datetime
