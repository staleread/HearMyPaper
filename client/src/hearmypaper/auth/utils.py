import os
import secrets
from typing import Tuple
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


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

        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=65536,
            backend=default_backend(),
        )
        key = kdf.derive(password.encode("utf-8"))

        iv = secrets.token_bytes(12)
        encryptor = Cipher(
            algorithms.AES(key), modes.GCM(iv), backend=default_backend()
        ).encryptor()

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        encrypted_data = salt + iv + ciphertext + encryptor.tag

        with open(token_path, "wb") as f:
            f.write(encrypted_data)

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
    iv = data[16:28]
    tag = data[-16:]
    ciphertext = data[28:-16]

    try:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=65536,
            backend=default_backend(),
        )
        key = kdf.derive(password.encode("utf-8"))

        decryptor = Cipher(
            algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()
        ).decryptor()

        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        decoded = plaintext.decode("utf-8")
    except Exception:
        raise CredentialsRepoError("Failed to read credentials")

    try:
        user_id, hex_priv = decoded.split(",", 1)
    except ValueError:
        raise CredentialsRepoError("Invalid plaintext format inside token")

    return user_id, bytes.fromhex(hex_priv)


def encrypt_with_public_key(data: bytes, public_key_pem: bytes) -> bytes:
    """
    Шифрує дані за допомогою публічного ключа RSA.
    """
    public_key = serialization.load_pem_public_key(
        public_key_pem, backend=default_backend()
    )
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise ValueError("Expected RSA public key")
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return encrypted


def decrypt_with_private_key(encrypted_data: bytes, private_key_pem: bytes) -> bytes:
    """
    Розшифровує дані за допомогою приватного ключа RSA.
    """
    private_key = serialization.load_pem_private_key(
        private_key_pem, password=None, backend=default_backend()
    )
    if not isinstance(private_key, rsa.RSAPrivateKey):
        raise ValueError("Expected RSA private key")
    decrypted = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return decrypted


def load_private_key_from_flash(path: str) -> bytes:
    """
    Завантажує приватний ключ із файлу (наприклад, після авторизації користувача).
    """
    with open(path, "rb") as key_file:
        return key_file.read()
