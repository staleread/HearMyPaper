from pydantic import BaseModel, field_validator

from .enums import AccessLevel, AccessType


class ObjectId(BaseModel):
    resource_type: str
    id: int | None = None  # None means "any ID"

    def __str__(self) -> str:
        return f"{self.resource_type}:{'*' if self.id is None else self.id}"

    def format(self) -> str:
        return str(self)

    @classmethod
    def parse(cls, value: str) -> "ObjectId":
        try:
            resource_type, id_str = value.split(":", 1)
            id_val = None if id_str == "*" else int(id_str)

            return cls(resource_type=resource_type, id=id_val)
        except ValueError:
            raise ValueError(f"Invalid ObjectId format: {value!r}")

    @field_validator("resource_type")
    @classmethod
    def check_resource_type(cls, v: str) -> str:
        if not v or ":" in v:
            raise ValueError("resource_type must be a non-empty string without ':'")
        return v

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ObjectId):
            return NotImplemented

        if self.resource_type != other.resource_type:
            return False

        if self.id is None or other.id is None:
            return True

        return self.id == other.id


class AccessRule(BaseModel):
    object_id: ObjectId
    access: AccessType

    def __str__(self) -> str:
        return f"{self.object_id}:{self.access.to_unix()}"

    @classmethod
    def parse(cls, value: str) -> "AccessRule":
        try:
            resource_type, id_str, perm = value.split(":", 2)
            obj_id = ObjectId(
                resource_type=resource_type, id=None if id_str == "*" else int(id_str)
            )
            access = AccessType.from_unix(perm)
            return cls(object_id=obj_id, access=access)
        except Exception:
            raise ValueError(f"Invalid AccessRule format: {value!r}")


class Subject(BaseModel):
    id: int
    access_level: AccessLevel
    access_rules: list[AccessRule]
