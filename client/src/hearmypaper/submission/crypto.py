import secrets
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def encrypt_file_with_public_key(file_bytes: bytes, public_key_bytes: bytes) -> bytes:
    """
    Encrypt file with instructor's public key using AES-GCM.
    The AES key is derived from the public key for deterministic encryption.

    Format: [iv(12B) | ciphertext(N) | tag(16B)]
    """
    # Derive AES key from public key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=public_key_bytes[:16],
        iterations=65536,
        backend=default_backend(),
    )
    aes_key = kdf.derive(public_key_bytes)

    # Encrypt with AES-GCM
    iv = secrets.token_bytes(12)
    encryptor = Cipher(
        algorithms.AES(aes_key), modes.GCM(iv), backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(file_bytes) + encryptor.finalize()
    return iv + ciphertext + encryptor.tag


def decrypt_file_with_private_key(
    encrypted_bytes: bytes, private_key_bytes: bytes
) -> bytes:
    """
    Decrypt file with instructor's private key using AES-GCM.
    The AES key is derived from the public key.

    Format: [iv(12B) | ciphertext(N) | tag(16B)]
    """
    if len(encrypted_bytes) < 12 + 16:
        raise ValueError("Invalid encrypted data: too short")

    # Load private key and derive public key
    private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    public_key_bytes = private_key.public_key().public_bytes_raw()

    # Derive AES key from public key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=public_key_bytes[:16],
        iterations=65536,
        backend=default_backend(),
    )
    aes_key = kdf.derive(public_key_bytes)

    # Decrypt with AES-GCM
    iv = encrypted_bytes[:12]
    tag = encrypted_bytes[-16:]
    ciphertext = encrypted_bytes[12:-16]

    decryptor = Cipher(
        algorithms.AES(aes_key), modes.GCM(iv, tag), backend=default_backend()
    ).decryptor()

    return decryptor.update(ciphertext) + decryptor.finalize()


def decrypt_aes_key_with_private_key(
    encrypted_key_b64: str, private_key_bytes: bytes
) -> bytes:
    """
    Decrypt AES key that was encrypted with the public key.
    Uses the same derivation approach as the server.
    """
    encrypted_key = base64.b64decode(encrypted_key_b64)

    # Load private key
    private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    public_key_bytes = private_key.public_key().public_bytes_raw()

    # Derive decryption key from public key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=public_key_bytes[:16],
        iterations=65536,
        backend=default_backend(),
    )
    derived_key = kdf.derive(public_key_bytes)

    # Decrypt AES key
    if len(encrypted_key) < 12 + 16:
        raise ValueError("Invalid encrypted data: too short")

    iv = encrypted_key[:12]
    tag = encrypted_key[-16:]
    ciphertext = encrypted_key[12:-16]

    decryptor = Cipher(
        algorithms.AES(derived_key), modes.GCM(iv, tag), backend=default_backend()
    ).decryptor()

    return decryptor.update(ciphertext) + decryptor.finalize()


def encrypt_file_with_aes(file_bytes: bytes, aes_key: bytes) -> str:
    """
    Encrypt file with AES-256-GCM and return base64 encoded string.
    Format: [iv(12B) | ciphertext(N) | tag(16B)]
    """
    iv = secrets.token_bytes(12)
    encryptor = Cipher(
        algorithms.AES(aes_key), modes.GCM(iv), backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(file_bytes) + encryptor.finalize()
    encrypted_data = iv + ciphertext + encryptor.tag

    return base64.b64encode(encrypted_data).decode("utf-8")


def decrypt_file_with_aes(encrypted_data_b64: str, aes_key: bytes) -> bytes:
    """
    Decrypt AES-256-GCM encrypted file from base64 string.
    Format: [iv(12B) | ciphertext(N) | tag(16B)]
    """
    encrypted_data = base64.b64decode(encrypted_data_b64)

    if len(encrypted_data) < 12 + 16:
        raise ValueError("Invalid encrypted data: too short")

    iv = encrypted_data[:12]
    tag = encrypted_data[-16:]
    ciphertext = encrypted_data[12:-16]

    decryptor = Cipher(
        algorithms.AES(aes_key), modes.GCM(iv, tag), backend=default_backend()
    ).decryptor()

    return decryptor.update(ciphertext) + decryptor.finalize()


def encrypt_aes_key_with_server_public_key(
    aes_key: bytes, server_public_key_bytes: bytes
) -> str:
    """
    Encrypt AES key with server's public key and return base64 encoded string.
    Uses the same derivation approach as the server.
    """
    # Derive encryption key from server's public key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=server_public_key_bytes[:16],
        iterations=65536,
        backend=default_backend(),
    )
    derived_key = kdf.derive(server_public_key_bytes)

    # Encrypt AES key
    iv = secrets.token_bytes(12)
    encryptor = Cipher(
        algorithms.AES(derived_key), modes.GCM(iv), backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(aes_key) + encryptor.finalize()
    encrypted_data = iv + ciphertext + encryptor.tag

    return base64.b64encode(encrypted_data).decode("utf-8")
