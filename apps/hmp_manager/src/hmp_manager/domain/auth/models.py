from datetime import datetime
from enum import IntEnum
from pydantic import BaseModel


class LoginCommand(BaseModel):
    pseudonym: str
    challenge: bytes
    signature: bytes


class AccessLevel(IntEnum):
    UNCLASSIFIED = 1
    CONTROLLED = 2
    RESTRICTED = 3
    CONFIDENTIAL = 4


class AuthUser(BaseModel):
    pseudonym: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    public_key: bytes


class AuthToken(BaseModel):
    token: str
    expires_at: datetime
