import os
import base64


def generate_challenge() -> str:
    return base64.b64encode(os.urandom(256)).decode("utf-8")
