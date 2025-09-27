from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    access_level: int
    categories: set[str]
    public_key: bytes


class UserDto(BaseModel):
    id: int
    username: str
    access_level: int
    categories: list[str]
    public_key: bytes


class UserCreateDto(BaseModel):
    username: str
    access_level: int
    categories: set[str]
    public_key: bytes
