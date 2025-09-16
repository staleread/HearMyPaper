import requests
import base64
import json

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

print("########### 1. Registration Stage ##############")
print("1.1. Generating private-public key pair")
private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

public_key_bytes = public_key.public_bytes(
    encoding=Encoding.Raw, format=PublicFormat.Raw
)
public_key_b64 = base64.b64encode(public_key_bytes).decode("utf-8")

print("Public key below:")
print(public_key_b64)

print("\n1.2. Registering user")
payload = {"username": "nicolas442", "public_key": public_key_b64}

r1 = requests.post("http://localhost:8000/auth/register", json=payload)
user_id = r1.json()["user_id"]

print(f"User ID: {user_id}")

print("\n############### 2. Login Stage ##################")
print("2.1. Requesting a challenge")

challenge_payload = {"user_id": user_id}
r2 = requests.post("http://localhost:8000/auth/challenge", json=challenge_payload)

challenge_b64 = r2.json()["challenge"]

print(f"Challenge: {challenge_b64}")

print("\n2.2. Signing a challenge")

challenge_bytes = base64.b64decode(challenge_b64)

signed_challenge_bytes = private_key.sign(challenge_bytes)
signed_challenge_b64 = base64.b64encode(signed_challenge_bytes).decode("utf-8")

print(f"Signed challenge: {signed_challenge_b64}")

print("\n2.3. Submitting signed challenge")

signature_payload = {
    "user_id": user_id,
    "challenge": challenge_b64,
    "signature": signed_challenge_b64,
}
r3 = requests.post("http://localhost:8000/auth/signature", json=signature_payload)

is_success = r3.json()["is_success"]

print(f"Signature by server verified: {is_success}")
