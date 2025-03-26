import base64
import hashlib
import os
import re
from contextlib import contextmanager
from re import match

from argon2 import PasswordHasher
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from dotenv import load_dotenv

from db import get_db_connection

__all__ = [
    "database_cursor",
    "decrypt_email",
    "encrypt_email",
    "hash_email",
    "hash_password",
    "mask_email",
    "validate_password",
    "verify_password",
]

load_dotenv()
ph = PasswordHasher()
AES_KEY = bytes.fromhex(os.getenv("AES_SECRET_KEY", os.urandom(32).hex()))
PEPPER = os.getenv("PEPPER", "SuperSecretPepper").encode("utf-8")


@contextmanager
def database_cursor():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        yield cursor
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()


def decrypt_email(encrypted_email: str) -> str:
    """Decrypts an AES-256 encrypted email."""
    encrypted_data = base64.b64decode(encrypted_email)
    iv, ciphertext = encrypted_data[:16], encrypted_data[16:]

    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_email = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_email.strip().decode()


def encrypt_email(email: str) -> str:
    """Encrypts an email using AES-256."""
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad email to 16-byte blocks
    padded_email = email + (16 - len(email) % 16) * " "
    ciphertext = encryptor.update(padded_email.encode()) + encryptor.finalize()

    # Store IV + ciphertext (Base64 encoded)
    return base64.b64encode(iv + ciphertext).decode()


def extract_error_message(message):
    try:
        cleaner_message = message.split(", ")[1].strip("()'")
        return cleaner_message if not "SQL" in cleaner_message else "Database error"
    except IndexError:
        return "An unknown error occurred"


def hash_email(email: str) -> str:
    """Generate a SHA-256 hash of the email (used for fast lookup)."""
    return hashlib.sha256(email.encode()).hexdigest()


def hash_password(password: str) -> tuple[str, bytes]:
    peppered_password = password.encode("utf-8") + PEPPER
    return ph.hash(peppered_password)  # Argon2 applies salt automatically


def mask_email(email: str) -> str:
    """Masks the email address to protect user privacy."""
    match = re.match(r"^([\w.+-]+)@([\w-]+)\.([a-zA-Z]{2,})$", email)
    if not match:
        raise ValueError("Invalid email format")

    local_part, domain_name, domain_extension = match.groups()

    # Mask the local part
    if len(local_part) > 2:
        local_part = local_part[0] + "*" * (len(local_part) - 2) + local_part[-1]

    # Mask the domain name
    if len(domain_name) > 2:
        domain_name = domain_name[0] + "*" * (len(domain_name) - 2) + domain_name[-1]

    return f"{local_part}@{domain_name}.{domain_extension}"


def validate_password(password):
    """
    Validates a password based on the following criteria:
    - At least 12 characters long.
    - Contains at least one uppercase letter (A-Z).
    - Contains at least one lowercase letter (a-z).
    - Contains at least one digit (0-9).
    - Contains at least one special character (any non-alphanumeric character).
    """
    return bool(
        match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$", password)
    )


def verify_password(password, stored_password):
    peppered_password = password.encode("utf-8") + PEPPER
    return ph.verify(stored_password, peppered_password)
