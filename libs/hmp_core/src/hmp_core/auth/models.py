from pydantic import BaseModel

from .enums import AccessLevel


class AccessClaims(BaseModel):
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
