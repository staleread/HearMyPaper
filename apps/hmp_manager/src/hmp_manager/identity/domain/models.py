from datetime import datetime
from pydantic import BaseModel, EmailStr

from .enums import AccessLevel


class LoginCommand(BaseModel):
    id: str
    challenge: bytes
    signature: bytes


class AuthUser(BaseModel):
    id: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    public_key: bytes


class AuthToken(BaseModel):
    token: str
    expires_at: datetime


class User(BaseModel):
    id: str
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
