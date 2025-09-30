#!/usr/bin/env python3
"""
Script to generate a SQL INSERT statement for creating an admin user.
This script generates a new Ed25519 key pair, prompts for user details,
and saves credentials to a binary file like the client does.
"""

import os
import re
import secrets
import sys
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def validate_email(email):
    """Validate email format using the same pattern as the User model."""
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_pattern, email) is not None


def save_user_credentials(
    user_id: str, token_path: str, private_key_bytes: bytes, password: str
) -> None:
    """
    Encrypt user_id and private_key_bytes with password (PBKDF2 + AES-256-GCM)
    and save to token_path as binary file.

    This function replicates the client's credentials_repo.py functionality.

    Format: [salt(16B) | iv(12B) | ciphertext(N) | tag(16B)]
    Plaintext: "user_id,hex(private_key_bytes)"
    """
    try:
        if not isinstance(token_path, str) or not token_path.strip():
            raise Exception("Invalid token_path: must be a non-empty string")

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

    except Exception as e:
        print(f"Error saving credentials: {e}")
        sys.exit(1)


def prompt_for_user_details():
    """Prompt the user for all required fields."""
    print("Creating Admin User - Please provide the following information:")
    print()

    # Ask for user ID
    try:
        user_id = int(input("User ID (integer): ").strip())
        if user_id <= 0:
            raise ValueError
    except ValueError:
        print("Error: User ID must be a positive integer")
        sys.exit(1)

    name = input("First Name: ").strip()
    if not name:
        print("Error: Name cannot be empty")
        sys.exit(1)

    surname = input("Last Name: ").strip()
    if not surname:
        print("Error: Surname cannot be empty")
        sys.exit(1)

    email = input("Email: ").strip()
    if not email or not validate_email(email):
        print("Error: Please provide a valid email address")
        sys.exit(1)

    # Default expiry to 1 year from now
    default_expiry = (datetime.now() + timedelta(days=365)).isoformat()
    expires_at = input(
        f"Account expiry (ISO format, default: {default_expiry}): "
    ).strip()
    if not expires_at:
        expires_at = default_expiry

    # Validate expiry format
    try:
        datetime.fromisoformat(expires_at)
    except ValueError:
        print("Error: Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS)")
        sys.exit(1)

    print()
    print("Access Levels:")
    print("1 = UNCLASSIFIED")
    print("2 = CONTROLLED")
    print("3 = RESTRICTED")
    print("4 = CONFIDENTIAL")
    print()

    try:
        conf_level = int(input("Confidentiality Level (1-4): ").strip())
        if conf_level not in [1, 2, 3, 4]:
            raise ValueError
    except ValueError:
        print("Error: Please enter a number between 1 and 4")
        sys.exit(1)

    print(
        "Integrity Levels (comma-separated, e.g., '3,4' for RESTRICTED and CONFIDENTIAL):"
    )
    integrity_input = input("Integrity Levels: ").strip()
    try:
        if integrity_input:
            integrity_levels = [int(x.strip()) for x in integrity_input.split(",")]
            for level in integrity_levels:
                if level not in [1, 2, 3, 4]:
                    raise ValueError
        else:
            integrity_levels = []
    except ValueError:
        print("Error: Please enter comma-separated numbers between 1 and 4")
        sys.exit(1)

    # Ask for credentials file path and password
    print()
    credentials_path = input(
        "Credentials file path (where to save admin credentials): "
    ).strip()
    if not credentials_path:
        print("Error: Credentials file path cannot be empty")
        sys.exit(1)

    # Check if credentials file already exists
    if os.path.exists(credentials_path):
        overwrite = (
            input(f"File '{credentials_path}' already exists. Overwrite? (y/N): ")
            .strip()
            .lower()
        )
        if overwrite != "y":
            print("Cancelled.")
            sys.exit(0)

    # Ensure directory exists
    credentials_dir = os.path.dirname(credentials_path)
    if credentials_dir and not os.path.exists(credentials_dir):
        try:
            os.makedirs(credentials_dir)
        except Exception as e:
            print(f"Error creating directory '{credentials_dir}': {e}")
            sys.exit(1)

    password = input("Password for credentials file: ").strip()
    if not password:
        print("Error: Password cannot be empty")
        sys.exit(1)

    return {
        "user_id": user_id,
        "name": name,
        "surname": surname,
        "email": email,
        "expires_at": expires_at,
        "confidentiality_level": conf_level,
        "integrity_levels": integrity_levels,
        "credentials_path": credentials_path,
        "password": password,
    }


def generate_key_pair():
    """Generate Ed25519 key pair and return private and public key bytes."""
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_key_bytes = private_key.private_bytes_raw()
    public_key_bytes = public_key.public_bytes_raw()

    return private_key_bytes, public_key_bytes


def generate_sql_statements(user_details, public_key_bytes):
    """Generate the SQL INSERT statement with setval for manual ID setting."""
    integrity_levels_sql = (
        f"ARRAY{user_details['integrity_levels']}"
        if user_details["integrity_levels"]
        else "ARRAY[]::INTEGER[]"
    )

    # First, update the sequence to ensure the next auto-generated ID is higher
    setval_sql = f"SELECT setval('users_id_seq', {user_details['user_id']}, true);"

    # Then, insert with explicit ID
    insert_sql = f"""INSERT INTO users (id, name, surname, email, confidentiality_level, integrity_levels, public_key, expires_at)
VALUES (
    {user_details["user_id"]},
    '{user_details["name"]}',
    '{user_details["surname"]}',
    '{user_details["email"]}',
    {user_details["confidentiality_level"]},
    {integrity_levels_sql},
    '\\x{public_key_bytes.hex()}',
    '{user_details["expires_at"]}'
);"""

    return setval_sql, insert_sql


def main():
    """Main function to orchestrate the admin user creation."""
    print("=" * 60)
    print("Admin User SQL Generator")
    print("=" * 60)
    print()

    # Get user details
    user_details = prompt_for_user_details()

    # Generate key pair
    print()
    print("Generating Ed25519 key pair...")
    private_key_bytes, public_key_bytes = generate_key_pair()

    # Save credentials to file (like the client does)
    print("Saving credentials to file...")
    save_user_credentials(
        str(user_details["user_id"]),
        user_details["credentials_path"],
        private_key_bytes,
        user_details["password"],
    )

    # Generate SQL
    setval_sql, insert_sql = generate_sql_statements(user_details, public_key_bytes)

    print()
    print("=" * 60)
    print("GENERATED SQL STATEMENTS:")
    print("=" * 60)
    print("-- Step 1: Update sequence")
    print(setval_sql)
    print()
    print("-- Step 2: Insert admin user")
    print(insert_sql)
    print()

    print("=" * 60)
    print("ADMIN CREDENTIALS INFORMATION:")
    print("=" * 60)
    print(f"User ID: {user_details['user_id']}")
    print(f"Credentials saved to: {user_details['credentials_path']}")
    print("Use password you provided to decrypt the credentials file")
    print()

    print("INSTRUCTIONS:")
    print("1. Run the SQL statements above against your database")
    print("2. Use the credentials file with the client application to authenticate")
    print("3. Keep the credentials file and password secure!")


if __name__ == "__main__":
    main()
