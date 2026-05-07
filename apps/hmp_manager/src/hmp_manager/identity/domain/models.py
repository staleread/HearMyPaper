from datetime import datetime
from pydantic import BaseModel, EmailStr

from .enums import AccessLevel


class AuthUser(BaseModel):
    id: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    public_key: bytes


class User(BaseModel):
    id: str
    name: str
    surname: str
    email: EmailStr
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    created_at: datetime
