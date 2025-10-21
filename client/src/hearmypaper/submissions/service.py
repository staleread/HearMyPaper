from result import Ok, Err
from ..auth.utils import (
    encrypt_with_public_key,
    decrypt_with_private_key,
    load_private_key_from_flash,
)


def encrypt_submission(file_path: str, public_key: bytes):
    """
    Шифрує файл за допомогою публічного ключа інструктора.

    Параметри:
    - file_path: шлях до локального файлу
    - public_key: публічний ключ інструктора

    Повертає:
    - Ok(encrypted_bytes) при успіху
    - Err(error_message) при помилці
    """
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        encrypted = encrypt_with_public_key(content, public_key)
        return Ok(encrypted)
    except Exception as e:
        return Err(str(e))


def decrypt_submission(encrypted_bytes: bytes, save_path: str, key_path: str):
    try:
        private_key = load_private_key_from_flash(path=key_path)
        decrypted = decrypt_with_private_key(private_key, encrypted_bytes)
        with open(save_path, "wb") as f:
            f.write(decrypted)
        return Ok(None)
    except Exception as e:
        return Err(str(e))
