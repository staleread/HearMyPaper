import secrets

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- Internal Configuration ---
_ITERATIONS = 65536
_KEY_LENGTH = 32
_SALT_LENGTH = 16
_IV_LENGTH = 12
_TAG_LENGTH = 16


# --- Key Management ---


def generate_key(length: int = _KEY_LENGTH) -> bytes:
    """Generate a random key of specified length."""
    return secrets.token_bytes(length)


def derive_key(
    secret: bytes,
    salt: bytes,
    length: int = _KEY_LENGTH,
    iterations: int = _ITERATIONS,
) -> bytes:
    """
    Derive a cryptographic key from a secret (e.g., password or public key)
    using PBKDF2.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    return kdf.derive(secret)


# --- Symmetric Operations ---


def encrypt(data: bytes, key: bytes) -> bytes:
    """
    Encrypt data using a symmetric key.
    The resulting bytes include all necessary metadata for decryption
    (IV and authentication tag).
    """
    iv = secrets.token_bytes(_IV_LENGTH)

    encryptor = Cipher(
        algorithms.AES(key), modes.GCM(iv), backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(data) + encryptor.finalize()
    return iv + ciphertext + encryptor.tag


def decrypt(data: bytes, key: bytes) -> bytes:
    """
    Decrypt data previously encrypted with 'encrypt'.
    """
    if len(data) < _IV_LENGTH + _TAG_LENGTH:
        raise ValueError("Invalid encrypted data format")

    iv = data[:_IV_LENGTH]
    tag = data[-_TAG_LENGTH:]
    ciphertext = data[_IV_LENGTH:-_TAG_LENGTH]

    decryptor = Cipher(
        algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()
    ).decryptor()

    return decryptor.update(ciphertext) + decryptor.finalize()


# --- Asymmetric Operations (Seal/Unseal) ---


def seal(data: bytes, public_key_bytes: bytes) -> bytes:
    """
    Encrypt data for a specific recipient using their public key.
    Internally derives a symmetric key for efficient encryption.
    """
    # Deterministic salt derived from the public key itself
    derived_key = derive_key(
        secret=public_key_bytes, salt=public_key_bytes[:_SALT_LENGTH]
    )
    return encrypt(data, derived_key)


def unseal(data: bytes, private_key_bytes: bytes) -> bytes:
    """
    Decrypt data intended for this recipient using their private key.
    """
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    public_key_bytes = private_key.public_key().public_bytes_raw()

    derived_key = derive_key(
        secret=public_key_bytes, salt=public_key_bytes[:_SALT_LENGTH]
    )
    return decrypt(data, derived_key)


# --- Identity & Verification (Sign/Verify) ---


def sign(data: bytes, private_key_bytes: bytes) -> bytes:
    """Sign data using a private key to prove identity and integrity."""
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    return private_key.sign(data)


def verify(data: bytes, signature: bytes, public_key_bytes: bytes) -> bool:
    """Verify that a signature is valid for the given data and public key."""
    try:
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
        public_key.verify(signature, data)
        return True
    except Exception:
        return False
