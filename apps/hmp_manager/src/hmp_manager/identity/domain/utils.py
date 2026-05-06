import os


def generate_challenge() -> bytes:
    return os.urandom(32)
