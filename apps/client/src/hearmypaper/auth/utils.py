import os
from typing import Tuple
from core import derive_key, encrypt, decrypt, generate_key


class CredentialsRepoError(Exception):
    """Raised when storing or retrieving user credentials fails."""


def save_user_credentials(
    user_id: str, token_path: str, private_key_bytes: bytes, password: str
) -> None:
    """
    Encrypt user_id and private_key_bytes with password (PBKDF2 + AES-256-GCM)
    and save to token_path as binary file.

    Format: [salt(16B) | iv(12B) | ciphertext(N) | tag(16B)]
    Plaintext: "user_id,hex(private_key_bytes)"
    """
    try:
        if not isinstance(token_path, str) or not token_path.strip():
            raise CredentialsRepoError("Invalid token_path: must be a non-empty string")

        plaintext = f"{user_id},{private_key_bytes.hex()}".encode("utf-8")

        salt = generate_key(16)
        key = derive_key(password.encode("utf-8"), salt)
        encrypted_data = encrypt(plaintext, key)

        with open(token_path, "wb") as f:
            f.write(salt + encrypted_data)

    except Exception:
        raise CredentialsRepoError("Failed to save credentials")


def get_user_credentials(token_path: str, password: str) -> Tuple[str, bytes]:
    """
    Decrypt the file at token_path using the provided password.
    Returns: (user_id: str, private_key_bytes: bytes)
    """
    if not os.path.exists(token_path):
        raise CredentialsRepoError("Invalid token_path: must be an existing file path")

    with open(token_path, "rb") as f:
        data = f.read()

    if len(data) < 16 + 12 + 16:  # salt + iv + tag at minimum
        raise CredentialsRepoError("Corrupted file: too short")

    salt = data[:16]
    encrypted_data = data[16:]

    try:
        key = derive_key(password.encode("utf-8"), salt)
        plaintext = decrypt(encrypted_data, key)
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
