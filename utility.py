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
    """Extracts a user-friendly error message from a database error message."""
    try:
        cleaner_message = message.split(", ")[1].strip("()'")
        return cleaner_message if "SQL" not in cleaner_message else "Database error"
    except IndexError:
        return "An unknown error occurred"


def hash_email(email: str) -> str:
    """Generate a SHA-256 hash of the email (used for fast lookup)."""
    return hashlib.sha256(email.encode()).hexdigest()


def hash_password(password: str) -> tuple[str, bytes]:
    peppered_password = password.encode("utf-8") + PEPPER
    return ph.hash(peppered_password)  # Argon2 applies salt automatically


def mask_email(email: str) -> str:
    local, domain = email.split("@")
    domain_parts = domain.split(".")

    def mask_part(part: str) -> str:
        if len(part) <= 2:
            return part
        return part[0] + "*" * (len(part) - 2) + part[-1]

    masked_local = re.sub(
        r"(\w)(\w+)(\w)",
        lambda m: m.group(1) + "*" * len(m.group(2)) + m.group(3),
        local,
    )
    masked_domain = ".".join(mask_part(part) for part in domain_parts)

    return masked_local + "@" + masked_domain


def validate_email(email: str) -> bool:
    """Validates an email address using a regex pattern."""
    pattern = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password) -> bool:
    """
    Validates a password based on the following criteria:
    - At least 12 characters long.
    - Contains at least one uppercase letter (A-Z).
    - Contains at least one lowercase letter (a-z).
    - Contains at least one digit (0-9).
    - Contains at least one special character (any non-alphanumeric character).
    """
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$"
    return bool(match(pattern, password))


def verify_password(password, stored_password):
    peppered_password = password.encode("utf-8") + PEPPER
    return ph.verify(stored_password, peppered_password)
