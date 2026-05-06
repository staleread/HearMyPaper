from pydantic import BaseModel


class ChallengeRequest(BaseModel):
    pseudonym: str


class ChallengeResponse(BaseModel):
    challenge_b64: str


class LoginRequest(BaseModel):
    pseudonym: str
    challenge_b64: str
    signature_b64: str


class LoginResponse(BaseModel):
    token: str
