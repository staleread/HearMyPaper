from pathlib import Path
from typing import override
from client_core.models import FileInfo
from client_core.ports.outgoing.local_storage import LocalStoragePort


class LocalStorageAdapter(LocalStoragePort):
    def __init__(self, download_folder: str):
        self._download_folder = Path(download_folder).expanduser()
        self._download_folder.mkdir(parents=True, exist_ok=True)

    @override
    def read(self, file: FileInfo) -> bytes:
        return Path(file.path).read_bytes()

    @override
    def write(self, info: FileInfo, data: bytes) -> FileInfo:
        filename = f"{info.name}.{info.extension}" if info.extension else info.name
        dest_path = self._download_folder / filename

        dest_path.write_bytes(data)

        return self.get_info(str(dest_path))

    @override
    def get_info(self, path: str) -> FileInfo:
        p = Path(path)
        return FileInfo(
            path=str(p.absolute()),
            name=p.stem,
            extension=p.suffix.lstrip("."),
        )

    @override
    def exists(self, file: FileInfo) -> bool:
        return Path(file.path).exists()
