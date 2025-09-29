from pydantic import BaseModel

from app.auth.enums import AccessLevel


class User(BaseModel):
    id: int = 0
    username: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    public_key: bytes
