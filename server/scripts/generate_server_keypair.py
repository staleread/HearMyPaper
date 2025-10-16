#!/usr/bin/env python3
"""
Script to generate server-side Ed25519 key pair for secure file transfers.
The private key is encrypted with a password and stored in secrets folder.
The public key is saved to the client folder for encryption purposes.
"""

import os
import sys
import secrets
import argparse
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def save_encrypted_private_key(
    private_key_bytes: bytes, output_path: str, password: str
) -> None:
    """
    Encrypt private_key_bytes with password (PBKDF2 + AES-256-GCM)
    and save to output_path as binary file.

    Format: [salt(16B) | iv(12B) | ciphertext(N) | tag(16B)]
    """
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

    ciphertext = encryptor.update(private_key_bytes) + encryptor.finalize()

    encrypted_data = salt + iv + ciphertext + encryptor.tag

    with open(output_path, "wb") as f:
        f.write(encrypted_data)


def save_public_key(public_key_bytes: bytes, output_path: str) -> None:
    """Save raw public key bytes to file."""
    with open(output_path, "wb") as f:
        f.write(public_key_bytes)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Ed25519 key pair for server-side secure file transfers"
    )
    parser.add_argument(
        "--private-key-path",
        default="secrets/server_private_key.enc",
        help="Path to save encrypted private key (default: secrets/server_private_key.enc)",
    )
    parser.add_argument(
        "--public-key-path",
        required=True,
        help="Path to save public key (typically in client folder)",
    )
    parser.add_argument(
        "--password",
        help="Password to encrypt private key (if not provided, will prompt)",
    )

    args = parser.parse_args()

    # Generate Ed25519 key pair
    print("Generating Ed25519 key pair...")
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_key_bytes = private_key.private_bytes_raw()
    public_key_bytes = public_key.public_bytes_raw()

    # Get password
    if args.password:
        password = args.password
    else:
        import getpass

        password = getpass.getpass("Enter password to encrypt private key: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            print("Error: Passwords do not match")
            sys.exit(1)

    if not password:
        print("Error: Password cannot be empty")
        sys.exit(1)

    # Ensure directories exist
    private_key_dir = os.path.dirname(args.private_key_path)
    if private_key_dir and not os.path.exists(private_key_dir):
        os.makedirs(private_key_dir)

    public_key_dir = os.path.dirname(args.public_key_path)
    if public_key_dir and not os.path.exists(public_key_dir):
        os.makedirs(public_key_dir)

    # Save encrypted private key
    print(f"Saving encrypted private key to: {args.private_key_path}")
    save_encrypted_private_key(private_key_bytes, args.private_key_path, password)

    # Save public key
    print(f"Saving public key to: {args.public_key_path}")
    save_public_key(public_key_bytes, args.public_key_path)

    print()
    print("=" * 60)
    print("Key pair generated successfully!")
    print("=" * 60)
    print(f"Private key (encrypted): {args.private_key_path}")
    print(f"Public key: {args.public_key_path}")
    print()
    print("Next steps:")
    print("1. Add SERVER_PRIVATE_KEY_PASSWORD to your .env file")
    print("2. Add SERVER_PRIVATE_KEY_PASSWORD to docker-compose.yaml")
    print("3. Distribute the public key to clients for file encryption")


if __name__ == "__main__":
    main()
