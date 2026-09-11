import base64
import hashlib
import os

from cryptography.fernet import Fernet, InvalidToken


def _get_fernet():
    """
    Create a Fernet encryption instance from the application key.
    """

    key = os.getenv("CAREER_APP_ENCRYPTION_KEY")

    if not key:
        raise RuntimeError(
            "CAREER_APP_ENCRYPTION_KEY is not configured."
        )

    key_bytes = key.encode("utf-8")

    # Convert the configured application secret into
    # a valid 32-byte Fernet key.
    derived_key = hashlib.sha256(key_bytes).digest()

    fernet_key = base64.urlsafe_b64encode(
        derived_key
    )

    return Fernet(fernet_key)


def encrypt_text(plaintext):
    """
    Encrypt text using Fernet authenticated encryption.
    """

    if plaintext is None:
        return ""

    if not isinstance(plaintext, str):
        raise TypeError(
            "Plaintext must be a string."
        )

    if not plaintext:
        return ""

    fernet = _get_fernet()

    encrypted_data = fernet.encrypt(
        plaintext.encode("utf-8")
    )

    return encrypted_data.decode("utf-8")


def decrypt_text(encrypted_value):
    """
    Decrypt text using Fernet authenticated encryption.
    """

    if encrypted_value is None:
        return ""

    if not isinstance(encrypted_value, str):
        raise TypeError(
            "Encrypted value must be a string."
        )

    if not encrypted_value:
        return ""

    fernet = _get_fernet()

    try:
        decrypted_data = fernet.decrypt(
            encrypted_value.encode("utf-8")
        )

        return decrypted_data.decode("utf-8")

    except InvalidToken as error:
        raise ValueError(
            "Encrypted data failed authentication."
        ) from error

    except UnicodeDecodeError as error:
        raise ValueError(
            "Encrypted data could not be decoded."
        ) from error