from datetime import datetime
from pydantic import BaseModel, EmailStr
from hmp_manager.domain.auth.models import AccessLevel


class UserCreateRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    public_key_b64: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class UserUpdateRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class UserResponse(BaseModel):
    id: str
    name: str
    surname: str
    email: EmailStr
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    created_at: datetime


class PublicKeyResponse(BaseModel):
    public_key_b64: str
