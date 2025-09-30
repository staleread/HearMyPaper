from enum import Enum, Flag, auto


class AccessLevel(Enum):
    UNCLASSIFIED = 1
    CONTROLLED = 2
    RESTRICTED = 3
    CONFIDENTIAL = 4

    def __lt__(self, other):  # type: ignore
        if isinstance(other, AccessLevel):
            return self.value < other.value
        return NotImplemented


class AccessType(Flag):
    NONE = 0
    READ = auto()
    WRITE = auto()
