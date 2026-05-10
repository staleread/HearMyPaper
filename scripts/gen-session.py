#!/usr/bin/env python3

import sys
import asyncio
import getpass
import httpx
from pathlib import Path

from client_server_bridge import IdentityPortAdapter
from client_credentials import FileCredentialsStorageAdapter
from client_core.use_cases.login import LoginUseCase
from client_core.ports.outgoing.session import SessionProviderPort


class SimpleSessionProvider(SessionProviderPort):
    def __init__(self):
        self.token = None

    def get_token(self):
        return self.token

    def set_token(self, token: str):
        self.token = token

    def get_user_id(self):
        return None


async def gen_session(key_path: Path, port: int):
    base_url = f"http://localhost:{port}"

    async with httpx.AsyncClient(base_url=base_url) as client:
        identity_port = IdentityPortAdapter(client)
        credentials_port = FileCredentialsStorageAdapter()
        session_provider = SimpleSessionProvider()

        login_use_case = LoginUseCase(
            identity_port=identity_port,
            credentials_port=credentials_port,
            session_provider=session_provider,
        )

        password = getpass.getpass(f"Password for {key_path.name}: ")

        try:
            await login_use_case(str(key_path), password)
            print(session_provider.get_token())
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <key_path> [port]", file=sys.stderr)
        sys.exit(1)

    key_path = Path(sys.argv[1])
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    if not key_path.exists():
        print(f"Error: Key file not found at {key_path}", file=sys.stderr)
        sys.exit(1)

    asyncio.run(gen_session(key_path, port))


if __name__ == "__main__":
    main()
