import os
from hmp_core import crypto


class CredentialsRepoError(Exception):
    """Raised when storing or retrieving user credentials fails."""


def save_user_credentials(
    user_id: str, token_path: str, private_key_bytes: bytes, password: str
) -> None:
    """
    Encrypt user_id and private_key_bytes with password (Argon2id + XSalsa20-Poly1305)
    and save to token_path as binary file.
    """
    try:
        if not token_path.strip():
            raise CredentialsRepoError("Invalid token_path: must be a non-empty string")

        plaintext = f"{user_id},{private_key_bytes.hex()}".encode("utf-8")

        encrypted_data = crypto.encrypt_symmetric(
            plaintext, password=password.encode("utf-8")
        )

        with open(token_path, "wb") as f:
            f.write(encrypted_data)

    except Exception:
        raise CredentialsRepoError("Failed to save credentials")


def get_user_credentials(token_path: str, password: str) -> tuple[str, bytes]:
    """
    Decrypt the file at token_path using the provided password.
    Returns: (user_id: str, private_key_bytes: bytes)
    """
    if not os.path.exists(token_path):
        raise CredentialsRepoError("Invalid token_path: must be an existing file path")

    with open(token_path, "rb") as f:
        data = f.read()

    try:
        plaintext = crypto.decrypt_symmetric(data, password=password.encode("utf-8"))
        decoded = plaintext.decode("utf-8")
    except Exception:
        raise CredentialsRepoError("Failed to read credentials")

    try:
        user_id, hex_priv = decoded.split(",", 1)
    except ValueError:
        raise CredentialsRepoError("Invalid plaintext format inside token")

    return user_id, bytes.fromhex(hex_priv)


def load_private_key_from_flash(path: str) -> bytes:
    """
    Завантажує приватний ключ із файлу (наприклад, після авторизації користувача).
    """
    with open(path, "rb") as key_file:
        return key_file.read()
