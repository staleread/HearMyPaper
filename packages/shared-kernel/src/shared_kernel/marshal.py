import base64


def to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def from_b64(data: str) -> bytes:
    return base64.b64decode(data)
