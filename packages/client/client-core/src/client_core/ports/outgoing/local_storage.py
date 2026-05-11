from typing import Protocol
from ...models import FileInfo


class LocalStoragePort(Protocol):
    def read(self, file: FileInfo) -> bytes:
        """Reads raw bytes from the local file described by FileInfo."""
        ...

    def write(self, info: FileInfo, data: bytes) -> FileInfo:
        """Writes raw bytes to a local file described by FileInfo and returns its complete FileInfo."""
        ...

    def get_info(self, path: str) -> FileInfo:
        """Creates a FileInfo model from a raw path string."""
        ...

    def exists(self, file: FileInfo) -> bool:
        """Checks if the file described by the FileInfo exists."""
        ...
