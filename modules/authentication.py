from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError


# Argon2id password hasher.
# PasswordHasher uses Argon2id by default.
password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


def hash_password(password):
    """
    Securely hash a password using Argon2id.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        raise ValueError("Password cannot be empty.")

    return password_hasher.hash(password)


def verify_password(password, password_hash):
    """
    Verify a password against an Argon2id password hash.

    Returns:
        True  -> password is correct
        False -> password is incorrect or hash is invalid
    """
    if not isinstance(password, str):
        return False

    if not isinstance(password_hash, str):
        return False

    if not password or not password_hash:
        return False

    try:
        return password_hasher.verify(password_hash, password)

    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def needs_rehash(password_hash):
    """
    Check whether an existing password hash should be upgraded
    to the current Argon2id configuration.
    """
    if not isinstance(password_hash, str) or not password_hash:
        return False

    try:
        return password_hasher.check_needs_rehash(password_hash)

    except (VerificationError, InvalidHashError):
        return False


def authenticate_user(password, password_hash):
    """
    Authenticate a user using secure password verification.

    Returns:
        True  -> authentication successful
        False -> authentication failed
    """
    return verify_password(password, password_hash)