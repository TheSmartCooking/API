from re import match

__all__ = ["validate_email", "validate_password"]


def validate_email(email: str) -> bool:
    """Validates an email address using a regex pattern."""
    pattern = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$"
    return bool(match(pattern, email))


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
