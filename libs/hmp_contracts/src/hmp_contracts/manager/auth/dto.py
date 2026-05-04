from pydantic import BaseModel


class ChallengeRequest(BaseModel):
    pseudonym: str


class ChallengeResponse(BaseModel):
    challenge: str  # Base64 encoded random bytes


class LoginRequest(BaseModel):
    pseudonym: str
    challenge: str
    signature: str  # Base64 encoded signature


class LoginResponse(BaseModel):
    token: str
