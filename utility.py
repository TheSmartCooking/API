import os
from contextlib import contextmanager
from re import match

from argon2 import PasswordHasher, exceptions
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


def hash_password_with_salt_and_pepper(password: str) -> tuple[str, bytes]:
    salt = os.urandom(16)
    seasoned_password = password.encode("utf-8") + salt + PEPPER
    return ph.hash(seasoned_password), salt


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


def verify_password(password, stored_password, salt):
    seasoned_password = password.encode("utf-8") + salt + PEPPER
    try:
        return ph.verify(stored_password, seasoned_password)
    except exceptions.VerifyMismatchError:
        return False
