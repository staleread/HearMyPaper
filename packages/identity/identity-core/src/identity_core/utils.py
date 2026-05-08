import os


# TODO ChallengeGenerator port
def generate_challenge() -> bytes:
    return os.urandom(32)
