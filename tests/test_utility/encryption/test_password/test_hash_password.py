from argon2 import PasswordHasher

from utility.encryption import hash_password

ph = PasswordHasher()


def test_hash_password_type(sample_password):
    """Ensure hash_password returns a string"""
    hashed_password = hash_password(sample_password)
    assert isinstance(hashed_password, str)


def test_hash_password_non_empty(sample_password):
    """Ensure hash_password returns a non-empty string"""
    hashed_password = hash_password(sample_password)
    assert len(hashed_password) > 0
