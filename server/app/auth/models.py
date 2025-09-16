from pydantic import BaseModel

from .enums import UserRole


class RegisterRequest(BaseModel):
    username: str
    role: UserRole = UserRole.STUDENT
    public_key: str


class RegisterResponse(BaseModel):
    user_id: int


class ChallengeRequest(BaseModel):
    user_id: int


class ChallengeResponse(BaseModel):
    challenge: str


class SignatureRequest(BaseModel):
    username: str
    challenge: str
    signature: str


class SignatureResponse(BaseModel):
    is_success: bool
