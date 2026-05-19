from enum import StrEnum, IntFlag


class AccessLevel(StrEnum):
    UNCLASSIFIED = "UNCLASSIFIED"
    CONTROLLED = "CONTROLLED"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"


class AccessType(IntFlag):
    READ = 1
    WRITE = 2
