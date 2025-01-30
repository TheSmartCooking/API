import os
from contextlib import contextmanager
from re import match

from argon2 import PasswordHasher
from dotenv import load_dotenv

from db import get_db_connection

load_dotenv()
ph = PasswordHasher()
PEPPER = os.getenv("PEPPER", "SuperSecretPepper").encode("utf-8")


@contextmanager
def database_cursor():
    db = get_db_connection()
    try:
        yield db.cursor()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def extract_error_message(message):
    try:
        return message.split(", ")[1].strip("()'")
    except IndexError:
        return "An unknown error occurred"


def hash_password(password: str) -> tuple[str, bytes]:
    peppered_password = password.encode("utf-8") + PEPPER
    return ph.hash(peppered_password)  # Argon2 applies salt automatically


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
