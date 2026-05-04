from enum import Enum, Flag, auto


class AccessLevel(int, Enum):
    UNCLASSIFIED = 1
    CONTROLLED = 2
    RESTRICTED = 3
    CONFIDENTIAL = 4


class AccessType(Flag):
    NONE = 0
    READ = auto()
    WRITE = auto()
