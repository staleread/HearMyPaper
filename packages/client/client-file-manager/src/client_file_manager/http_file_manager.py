import httpx
from pathlib import Path
from typing import override
from client_core.models import FileInfo
from client_core.ports.outgoing.file_manager import FileManagerPort


class HttpFileManagerAdapter(FileManagerPort):
    @override
    def get_info(self, path: str) -> FileInfo:
        p = Path(path)
        return FileInfo(
            path=str(p.absolute()),
            name=p.stem,
            extension=p.suffix.lstrip("."),
        )

    @override
    async def download(
        self, url: str, folder: str, name: str, extension: str
    ) -> FileInfo:
        dest_folder = Path(folder).expanduser()
        dest_folder.mkdir(parents=True, exist_ok=True)

        filename = f"{name}.{extension}" if extension else name
        dest_path = dest_folder / filename

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            with open(dest_path, "wb") as f:
                f.write(response.content)

        return self.get_info(str(dest_path))

    @override
    async def upload(self, url: str, file: FileInfo) -> None:
        content = Path(file.path).read_bytes()

        # Use a clean client without potential shared session's Authorization header
        # MinIO/S3 presigned URLs fail if an extra Authorization header is provided.
        async with httpx.AsyncClient() as upload_client:
            headers = {"Content-Type": "application/octet-stream"}
            response = await upload_client.put(url, content=content, headers=headers)
            response.raise_for_status()

    @override
    def exists(self, file: FileInfo) -> bool:
        return Path(file.path).exists()
