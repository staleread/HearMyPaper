from pydantic import BaseModel

from .enums import AccessLevel


class Subject(BaseModel):
    id: int
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
