from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    access_level: int
    categories: set[str]
