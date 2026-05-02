import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519

from core import decrypt, derive_key, encrypt, generate_key, seal, sign, unseal, verify


def test_symmetric_encryption() -> None:
    key = generate_key()
    data = b"secret message"
    encrypted = encrypt(data, key)
    assert encrypted != data
    decrypted = decrypt(encrypted, key)
    assert decrypted == data


def test_key_derivation() -> None:
    secret = b"password"
    salt = b"staticsalt123456"
    key1 = derive_key(secret, salt)
    key2 = derive_key(secret, salt)
    assert key1 == key2
    assert len(key1) == 32


def test_asymmetric_sealing() -> None:
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_key_bytes = private_key.private_bytes_raw()
    public_key_bytes = private_key.public_key().public_bytes_raw()

    data = b"confidential data"
    sealed = seal(data, public_key_bytes)
    assert sealed != data

    unsealed = unseal(sealed, private_key_bytes)
    assert unsealed == data


def test_signing() -> None:
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_key_bytes = private_key.private_bytes_raw()
    public_key_bytes = private_key.public_key().public_bytes_raw()

    data = b"important document"
    signature = sign(data, private_key_bytes)

    assert verify(data, signature, public_key_bytes) is True
    assert verify(b"tampered document", signature, public_key_bytes) is False


def test_invalid_decrypt() -> None:
    key = generate_key()
    with pytest.raises(ValueError, match="Invalid encrypted data format"):
        decrypt(b"short", key)
