from dataclasses import dataclass
from datetime import datetime

from .enums import AccessLevel


@dataclass(frozen=True)
class AuthUser:
    id: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


@dataclass(frozen=True)
class User:
    id: str
    name: str
    surname: str
    email: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    created_at: datetime
