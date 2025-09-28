from enum import Enum, StrEnum, Flag, auto


class UserRole(StrEnum):
    STUDENT = "student"
    CURATOR = "curator"
    INSTRUCTOR = "instructor"


class AccessLevel(Enum):
    UNCLASSIFIED = 1
    CONTROLLED = 2
    RESTRICTED = 3
    CONFIDENTIAL = 4

    def __lt__(self, other):  # type: ignore
        if other is AccessLevel:
            return self.value < other.value
        return NotImplemented


class AccessType(Flag):
    NONE = 0
    READ = auto()
    WRITE = auto()

    def to_unix(self) -> str:
        r = "r" if AccessType.READ in self else "-"
        w = "w" if AccessType.WRITE in self else "-"
        return r + w

    @classmethod
    def from_unix(cls, value: str) -> "AccessType":
        if len(value) != 2:
            raise ValueError(f"Invalid permission string: {value!r}")

        access = cls.NONE
        if value[0] == "r":
            access |= cls.READ
        elif value[0] != "-":
            raise ValueError(f"Invalid read flag in: {value!r}")

        if value[1] == "w":
            access |= cls.WRITE
        elif value[1] != "-":
            raise ValueError(f"Invalid write flag in: {value!r}")

        return access
