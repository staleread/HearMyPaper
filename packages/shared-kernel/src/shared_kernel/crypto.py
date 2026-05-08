import nacl.exceptions
import nacl.public
import nacl.secret
import nacl.signing
import nacl.utils
from nacl.pwhash import argon2id


def generate_keypair():
    signing_key = nacl.signing.SigningKey.generate()

    private_key_bytes = bytes(signing_key)
    public_key_bytes = bytes(signing_key.verify_key)

    return private_key_bytes, public_key_bytes


def encrypt_symmetric(data: bytes, *, password: bytes) -> bytes:
    salt = nacl.utils.random(argon2id.SALTBYTES)
    key = argon2id.kdf(nacl.secret.SecretBox.KEY_SIZE, password, salt)

    box = nacl.secret.SecretBox(key)
    encrypted = box.encrypt(data)

    return salt + encrypted


def decrypt_symmetric(payload: bytes, *, password: bytes) -> bytes:
    salt = payload[: argon2id.SALTBYTES]
    encrypted_data = payload[argon2id.SALTBYTES :]

    key = argon2id.kdf(nacl.secret.SecretBox.KEY_SIZE, password, salt)
    box = nacl.secret.SecretBox(key)

    return box.decrypt(encrypted_data)


def seal(data: bytes, *, public_key_bytes: bytes) -> bytes:
    """
    Encrypt data for a recipient using their public key.
    Uses an ephemeral sender key for Forward Secrecy.
    """
    # Convert Ed25519 public key to X25519 for encryption
    signing_pk = nacl.signing.VerifyKey(public_key_bytes)
    encryption_pk = signing_pk.to_curve25519_public_key()

    box = nacl.public.SealedBox(encryption_pk)
    return box.encrypt(data)


def unseal(data: bytes, *, private_key_bytes: bytes) -> bytes:
    """Decrypt data using the recipient's private key."""
    # Convert Ed25519 private key to X25519 for decryption
    signing_sk = nacl.signing.SigningKey(private_key_bytes)
    encryption_sk = signing_sk.to_curve25519_private_key()

    box = nacl.public.SealedBox(encryption_sk)
    return box.decrypt(data)


def sign(data: bytes, *, private_key_bytes: bytes) -> bytes:
    signing_key = nacl.signing.SigningKey(private_key_bytes)
    signed = signing_key.sign(data)

    return signed.signature


def verify(data: bytes, *, signature: bytes, public_key_bytes: bytes) -> bool:
    verify_key = nacl.signing.VerifyKey(public_key_bytes)
    try:
        _ = verify_key.verify(data, signature)
        return True
    except nacl.exceptions.BadSignatureError:
        return False
