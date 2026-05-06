from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel


class LoginCommand(BaseModel):
    pseudonym: str
    challenge: bytes
    signature: bytes


class AccessLevel(StrEnum):
    UNCLASSIFIED = "UNCLASSIFIED"
    CONTROLLED = "CONTROLLED"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"


class AuthUser(BaseModel):
    pseudonym: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    public_key: bytes


class AuthToken(BaseModel):
    token: str
    expires_at: datetime
