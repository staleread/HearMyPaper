import nacl.exceptions
import pytest

from hmp_core.crypto import crypto


def test_generate_keypair() -> None:
    priv, pub = crypto.generate_keypair()
    assert len(priv) == 32
    assert len(pub) == 32
    assert priv != pub


def test_symmetric_encryption() -> None:
    password = b"strong-password"
    data = b"secret message"

    encrypted = crypto.encrypt_symmetric(data, password=password)
    assert encrypted != data

    decrypted = crypto.decrypt_symmetric(encrypted, password=password)
    assert decrypted == data


def test_symmetric_encryption_wrong_password() -> None:
    password = b"strong-password"
    wrong_password = b"wrong-password"
    data = b"secret message"

    encrypted = crypto.encrypt_symmetric(data, password=password)

    with pytest.raises(nacl.exceptions.CryptoError):
        crypto.decrypt_symmetric(encrypted, password=wrong_password)


def test_asymmetric_sealing() -> None:
    priv, pub = crypto.generate_keypair()
    data = b"confidential data"

    sealed = crypto.seal(data, public_key_bytes=pub)
    assert sealed != data

    unsealed = crypto.unseal(sealed, private_key_bytes=priv)
    assert unsealed == data


def test_signing() -> None:
    priv, pub = crypto.generate_keypair()
    data = b"important document"

    signature = crypto.sign(data, private_key_bytes=priv)
    assert len(signature) == 64

    assert crypto.verify(data, signature=signature, public_key_bytes=pub) is True
    assert (
        crypto.verify(b"tampered document", signature=signature, public_key_bytes=pub)
        is False
    )


def test_invalid_decrypt() -> None:
    password = b"password"
    with pytest.raises(nacl.exceptions.CryptoError):
        crypto.decrypt_symmetric(b"short", password=password)
