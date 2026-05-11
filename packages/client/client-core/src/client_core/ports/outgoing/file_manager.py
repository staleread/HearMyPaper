from typing import Protocol


from ...models import FileInfo


class FileManagerPort(Protocol):
    def get_info(self, path: str) -> FileInfo:
        """Creates a FileInfo model from a raw path string."""
        ...

    async def download(
        self, url: str, folder: str, name: str, extension: str
    ) -> FileInfo:
        """
        Downloads content from the given URL and saves it to the specified folder.
        Returns the FileInfo for the saved file.
        """
        ...

    async def upload(self, url: str, file: FileInfo) -> None:
        """Uploads the file described by the FileInfo to the given URL."""
        ...

    def exists(self, file: FileInfo) -> bool:
        """Checks if the file described by the FileInfo exists."""
        ...
