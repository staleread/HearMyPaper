from enum import Enum, StrEnum


class ConfidentialityLevel(Enum):
    UNCLASSIFIED = 1
    CONTROLLED = 2
    RESTRICTED = 3


class SubjectAction(StrEnum):
    READ = "read"
    WRITE = "write"
