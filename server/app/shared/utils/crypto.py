import secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)


def load_server_private_key(key_path: str, password: str) -> Ed25519PrivateKey:
    """
    Load and decrypt the server's private key from encrypted file.

    Format: [salt(16B) | iv(12B) | ciphertext(N) | tag(16B)]
    """
    with open(key_path, "rb") as f:
        data = f.read()

    if len(data) < 16 + 12 + 16:
        raise ValueError("Corrupted key file: too short")

    salt = data[:16]
    iv = data[16:28]
    tag = data[-16:]
    ciphertext = data[28:-16]

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

    private_key_bytes = decryptor.update(ciphertext) + decryptor.finalize()

    return Ed25519PrivateKey.from_private_bytes(private_key_bytes)


def generate_aes_key() -> bytes:
    """Generate a 256-bit AES key (32 bytes)."""
    return secrets.token_bytes(32)


def encrypt_with_aes(data: bytes, key: bytes) -> bytes:
    """
    Encrypt data with AES-256-GCM.

    Returns: [iv(12B) | ciphertext(N) | tag(16B)]
    """
    iv = secrets.token_bytes(12)
    encryptor = Cipher(
        algorithms.AES(key), modes.GCM(iv), backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(data) + encryptor.finalize()

    return iv + ciphertext + encryptor.tag


def decrypt_with_aes(encrypted_data: bytes, key: bytes) -> bytes:
    """
    Decrypt AES-256-GCM encrypted data.

    Format: [iv(12B) | ciphertext(N) | tag(16B)]
    """
    if len(encrypted_data) < 12 + 16:
        raise ValueError("Invalid encrypted data: too short")

    iv = encrypted_data[:12]
    tag = encrypted_data[-16:]
    ciphertext = encrypted_data[12:-16]

    decryptor = Cipher(
        algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()
    ).decryptor()

    return decryptor.update(ciphertext) + decryptor.finalize()


def encrypt_with_ed25519_public_key(data: bytes, public_key_bytes: bytes) -> bytes:
    """
    Encrypt small data (like AES key) with Ed25519 public key.
    Note: Ed25519 is primarily for signing. For encryption compatibility,
    we use a derived key approach based on the public key.
    """
    # Derive encryption key from public key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=public_key_bytes[:16],
        iterations=65536,
        backend=default_backend(),
    )
    derived_key = kdf.derive(public_key_bytes)

    return encrypt_with_aes(data, derived_key)


def decrypt_with_ed25519_private_key(
    encrypted_data: bytes, private_key: Ed25519PrivateKey
) -> bytes:
    """
    Decrypt data that was encrypted with the corresponding public key.
    """
    public_key_bytes = private_key.public_key().public_bytes_raw()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=public_key_bytes[:16],
        iterations=65536,
        backend=default_backend(),
    )
    derived_key = kdf.derive(public_key_bytes)

    return decrypt_with_aes(encrypted_data, derived_key)
