import os
from client_core.ports.outgoing.credentials import CredentialsStoragePort
from shared_kernel import crypto


class FileCredentialsStorageAdapter(CredentialsStoragePort):
    def save_credentials(
        self, user_id: str, path: str, private_key: bytes, password: str
    ) -> None:
        """
        Encrypt user_id and private_key with password and save to path.
        """
        try:
            plaintext = f"{user_id},{private_key.hex()}".encode("utf-8")
            encrypted_data = crypto.encrypt_symmetric(
                plaintext, password=password.encode("utf-8")
            )

            with open(path, "wb") as f:
                f.write(encrypted_data)
        except Exception as e:
            raise RuntimeError(f"Failed to save credentials: {e}")

    def load_credentials(self, path: str, password: str) -> tuple[str, bytes]:
        """
        Decrypt the file at path using the provided password.
        Returns: (user_id: str, private_key: bytes)
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Credentials file not found: {path}")

        try:
            with open(path, "rb") as f:
                data = f.read()

            plaintext = crypto.decrypt_symmetric(
                data, password=password.encode("utf-8")
            )
            decoded = plaintext.decode("utf-8")

            user_id, hex_priv = decoded.split(",", 1)
            return user_id, bytes.fromhex(hex_priv)
        except Exception as e:
            raise RuntimeError(f"Failed to load credentials: {e}")
