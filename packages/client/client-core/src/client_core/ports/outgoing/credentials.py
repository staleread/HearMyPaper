from typing import Protocol


class CredentialsStoragePort(Protocol):
    def save_credentials(
        self, user_id: str, path: str, private_key: bytes, password: str
    ) -> None: ...
    def load_credentials(self, path: str, password: str) -> tuple[str, bytes]: ...
