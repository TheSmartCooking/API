import pytest
from argon2 import PasswordHasher

from utils import validate_password

ph = PasswordHasher()


@pytest.fixture
def sample_password():
    return "SecurePass123!"


def test_valid_passwords():
    """Verify valid passwords pass"""
    assert validate_password("StrongPass1!") is True
    assert validate_password("Another$ecure123") is True
    assert validate_password("ValidPass99@#") is True


def test_too_short_password():
    """Ensure passwords that are too short fail"""
    assert validate_password("Short1!") is False


def test_missing_uppercase():
    """Ensure passwords missing uppercase letters fail"""
    assert validate_password("weakpassword1!") is False


def test_missing_lowercase():
    """Ensure passwords missing lowercase letters fail"""
    assert validate_password("WEAKPASSWORD1!") is False


def test_missing_digit():
    """Ensure passwords missing digits fail"""
    assert validate_password("NoDigitPass!") is False


def test_missing_special_character():
    """Ensure passwords missing special characters fail"""
    assert validate_password("NoSpecial12345") is False


def test_only_special_characters():
    """Ensure passwords with only special characters fail"""
    assert validate_password("!!!!!!@@@@@@") is False


def test_only_numbers():
    """Ensure passwords with only numbers fail"""
    assert validate_password("123456789012") is False


def test_only_letters():
    """Ensure passwords with only letters fail"""
    assert validate_password("JustLettersOnly") is False


def test_empty_string():
    """Ensure empty strings fail"""
    assert validate_password("") is False


def test_whitespace_only():
    """Ensure whitespace-only strings fail"""
    assert validate_password("            ") is False
