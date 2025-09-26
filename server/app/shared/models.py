from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: int
    role: str
    access_level: int
    categories: set[str]
