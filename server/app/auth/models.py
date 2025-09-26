from pydantic import BaseModel
from enum import StrEnum


class UserRole(StrEnum):
    STUDENT = "student"
    CURATOR = "curator"
    INSTRUCTOR = "instructor"


class RegisterRequest(BaseModel):
    username: str
    role: UserRole
    public_key: str


class RegisterResponse(BaseModel):
    user_id: int


class ChallengeRequest(BaseModel):
    user_id: int


class ChallengeResponse(BaseModel):
    challenge: str


class LoginRequest(BaseModel):
    user_id: int
    challenge: str
    signature: str


class LoginResponse(BaseModel):
    token: str
