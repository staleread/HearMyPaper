from datetime import datetime
from pydantic import BaseModel, EmailStr
from ..auth.models import AccessLevel


class User(BaseModel):
    id: str  # Generated via IdentityProvider
    name: str
    surname: str
    email: EmailStr
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    created_at: datetime


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    public_key: bytes
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class UserUpdate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
