from pydantic import BaseModel, field_validator
import re
from datetime import datetime

from .enums import AccessLevel


class Subject(BaseModel):
    id: int
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class User(BaseModel):
    id: int = 0
    name: str
    surname: str
    email: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    public_key: bytes
    expires_at: str  # ISO date string

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("expires_at")
    @classmethod
    def validate_expires_at(cls, v: str) -> str:
        try:
            datetime.fromisoformat(v)
        except ValueError:
            raise ValueError("expires_at must be a valid ISO date string")
        return v
