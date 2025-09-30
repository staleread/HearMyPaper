from pydantic import BaseModel

from .enums import AccessLevel


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


class UserCreateRequest(BaseModel):
    name: str
    surname: str
    email: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    public_key: str  # base64 encoded
    expires_at: str  # ISO date string


class UserCreateResponse(BaseModel):
    id: int


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    expires_at: str


class UserListResponse(BaseModel):
    id: int
    full_name: str


class UserUpdateRequest(BaseModel):
    name: str
    surname: str
    email: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    expires_at: str  # ISO date string
