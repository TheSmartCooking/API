import pytest

from utility import hash_email


@pytest.fixture
def sample_email():
    return "sample.email@example.com"


def test_hash_email_type(sample_email):
    """Ensure hash_email returns a string"""
    hashed_email = hash_email(sample_email)
    assert isinstance(hashed_email, str)


def test_hash_email_non_empty(sample_email):
    """Ensure hash_email returns a non-empty string"""
    hashed_email = hash_email(sample_email)
    assert len(hashed_email) > 0


def test_hash_email_different(sample_email):
    """Ensure hash_email returns a different value than the original email"""
    hashed_email = hash_email(sample_email)
    assert hashed_email != sample_email


def test_hash_email_consistent(sample_email):
    """Ensure hash_email returns the same value for the same input"""
    hashed_email = hash_email(sample_email)
    assert hashed_email == hash_email(sample_email)
