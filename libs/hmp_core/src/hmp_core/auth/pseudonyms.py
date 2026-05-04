import hashlib

from uidgen import adjectives, nouns


def get_stable_pseudonym(seed: str) -> str:
    """
    Generates a stable adjective-noun ID from a seed (e.g., email).
    Ensures user@university.edu is always shimmering-falcon across all microservices.
    """
    # Normalize the seed (email or UUID) to ensure stability
    normalized_seed = seed.lower().strip().encode()
    hash_hex = hashlib.sha256(normalized_seed).hexdigest()

    # Use different slices of the hash for adj, noun, and number to reduce coupling
    adj_index = int(hash_hex[:8], 16) % len(adjectives)
    noun_index = int(hash_hex[8:16], 16) % len(nouns)
    suffix_num = int(hash_hex[16:24], 16) % 1000  # 0-999

    return f"{adjectives[adj_index]}-{nouns[noun_index]}-{suffix_num}"
