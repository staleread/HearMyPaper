from typing import Protocol
from uuid import UUID


class FilePathResolverPort(Protocol):
    def get_source_path(self, conversion_id: UUID) -> str: ...
    def get_result_path(self, conversion_id: UUID) -> str: ...
