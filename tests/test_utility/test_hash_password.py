import pytest
from argon2 import PasswordHasher

from utility import hash_password

ph = PasswordHasher()


@pytest.fixture
def sample_password():
    return "SecurePass123!"


def test_hash_password(sample_password):
    """Ensure hash_password returns a hashed password as a non-empty string"""
    hashed_password = hash_password(sample_password)
    assert isinstance(hashed_password, str)
    assert len(hashed_password) > 0
