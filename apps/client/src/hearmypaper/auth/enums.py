from enum import Enum


class AccessLevel(Enum):
    UNCLASSIFIED = 1
    CONTROLLED = 2
    RESTRICTED = 3
    CONFIDENTIAL = 4

    def __lt__(self, other):  # type: ignore
        if isinstance(other, AccessLevel):
            return self.value < other.value
        return NotImplemented

    @classmethod
    def get_display_options(cls) -> list[str]:
        """Get list of display strings for UI dropdowns"""
        return [f"{level.value} - {level.name.title()}" for level in cls]

    @classmethod
    def from_display_string(cls, display_string: str) -> "AccessLevel":
        """Convert display string back to AccessLevel"""
        value = int(display_string.split(" - ")[0])
        return cls(value)

    def to_display_string(self) -> str:
        """Convert AccessLevel to display string"""
        return f"{self.value} - {self.name.title()}"
