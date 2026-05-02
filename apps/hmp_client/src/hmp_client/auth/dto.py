from pydantic import BaseModel


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
