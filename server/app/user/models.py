from pydantic import BaseModel

from app.auth.models import AccessRule
from app.auth.enums import AccessLevel


class User(BaseModel):
    id: int = 0
    username: str
    access_level: AccessLevel
    access_rules: list[AccessRule] = list()
    public_key: bytes
