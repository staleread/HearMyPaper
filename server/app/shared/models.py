from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: int
    access_level: int
    categories: set[str]
