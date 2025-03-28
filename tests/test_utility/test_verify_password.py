import pytest
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError

from utility import hash_password, verify_password

ph = PasswordHasher()


@pytest.fixture
def sample_password():
    return "SecurePass123!"


def test_verify_password(sample_password):
    """Verify correct password"""
    hashed_password = hash_password(sample_password)
    assert verify_password(sample_password, hashed_password) is True


def test_verify_wrong_password(sample_password):
    """Ensure wrong password fails"""
    hashed_password = hash_password(sample_password)
    with pytest.raises(VerifyMismatchError):
        verify_password("WrongPass123!", hashed_password) is False


def test_verify_empty_password():
    """Ensure empty password fails"""
    hashed_password = hash_password("SomePass123!")
    with pytest.raises(VerifyMismatchError):
        verify_password("", hashed_password) is False


def test_verify_password_tampered():
    """Ensure tampered password fails"""
    hashed_password = hash_password("AnotherPass!123")
    tampered_hash = hashed_password[:-5] + "xyz"  # Modify the hash slightly
    with pytest.raises(VerificationError):
        assert verify_password("AnotherPass!123", tampered_hash)
