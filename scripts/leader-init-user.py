#!/usr/bin/env python3

import sys
import getpass
from pathlib import Path

import uidgen
from shared_kernel.crypto import generate_keypair, encrypt_symmetric
from shared_kernel.marshal import to_b64


def get_ui_stream():
    """Returns the stream for UI (prompts, info).
    If stdout is redirected (not a TTY), we MUST use stderr for UI to keep stdout clean.
    If stdout is a TTY, we use it to avoid writing to stderr 'without a need'.
    """
    return sys.stdout if sys.stdout.isatty() else sys.stderr


def print_ui(msg: str = "", end: str = "\n"):
    print(msg, file=get_ui_stream(), end=end, flush=True)


def ask(msg: str, default: str | None = None) -> str:
    prompt_msg = f"{msg} [{default}]: " if default else f"{msg}: "
    print_ui(prompt_msg, end="")
    val = sys.stdin.readline().strip()

    return val if val else default


def main():
    try:
        print_ui("╔══════════════════════════════════════════════════════╗")
        print_ui("║       HearMyPaper - Initial User Configuration       ║")
        print_ui("╚══════════════════════════════════════════════════════╝")
        print_ui()

        suggested_id = uidgen.generate()

        user_id = ask("User ID", default=suggested_id)
        name = ask("First Name")
        surname = ask("Surname")
        email = ask("Email")

        password = getpass.getpass(
            "Password for private key encryption: ", stream=get_ui_stream()
        )

        key_path_str = ask("Path to save encrypted private key", default="admin.key")
        key_path = Path(key_path_str)

        private_key, public_key = generate_keypair()
        # Format: user_id,hex_private_key (matches client file_storage)
        plaintext = f"{user_id},{private_key.hex()}".encode("utf-8")
        encrypted_data = encrypt_symmetric(plaintext, password=password.encode())

        # Save the private key
        if key_path.parent:
            key_path.parent.mkdir(parents=True, exist_ok=True)

        with open(key_path, "wb") as f:
            f.write(encrypted_data)

        print_ui(f"\n[SUCCESS] Private key saved to: {key_path.absolute()}")
        print_ui(
            "[INFO] Configuration generated below. If you redirected stdout to a file,"
        )
        print_ui(
            "[INFO] (e.g. .env.local) it will contain only the environment variable lines.\n"
        )

        # The actual environment variables go to STDOUT
        # If redirected, only these lines will be in the file.
        print(f"INIT_USER__ID={user_id}")
        print(f"INIT_USER__NAME={name}")
        print(f"INIT_USER__SURNAME={surname}")
        print(f"INIT_USER__EMAIL={email}")
        print(f"INIT_USER__PUBLIC_KEY_B64={to_b64(public_key)}")

    except KeyboardInterrupt:
        print_ui("\n\n[ABORTED] Configuration cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_ui(f"\n[ERROR] An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
