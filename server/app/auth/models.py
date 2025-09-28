from pydantic import BaseModel, field_validator

from .enums import AccessLevel, AccessType


class ObjectId(BaseModel):
    resource_type: str
    id: int

    def __str__(self) -> str:
        return f"{self.resource_type}:{self.id}"

    def format(self) -> str:
        return str(self)

    @classmethod
    def parse(cls, value: str) -> "ObjectId":
        try:
            resource_type, id_str = value.split(":", 1)
            return cls(resource_type=resource_type, id=int(id_str))
        except ValueError:
            raise ValueError(f"Invalid ObjectId format: {value!r}")

    @field_validator("resource_type")
    @classmethod
    def check_resource_type(cls, v: str) -> str:
        if not v or ":" in v:
            raise ValueError("resource_type must be a non-empty string without ':'")
        return v


class AccessRule(BaseModel):
    object_id: ObjectId
    access: AccessType

    def __str__(self) -> str:
        return f"{self.object_id}:{self.access.to_unix()}"

    @classmethod
    def parse(cls, value: str) -> "AccessRule":
        try:
            resource_type, id_str, perm = value.split(":", 2)
            return cls(
                object_id=ObjectId(resource_type=resource_type, id=int(id_str)),
                access=AccessType.from_unix(perm),
            )
        except Exception:
            raise ValueError(f"Invalid AccessRule format: {value!r}")


class Subject(BaseModel):
    id: int
    access_level: AccessLevel
    access_rules: list[AccessRule]
