import pytest

from utility import validate_email


@pytest.fixture
def sample_email():
    return "sample.email@example.com"


def test_valid_emails():
    """Verify valid emails pass"""
    assert validate_email("good.email@example.com") is True
    assert validate_email("good.with+subdomain@example.com") is True
    assert validate_email("goodemail@mockda.ta")


def test_invalid_emails():
    """Ensure invalid emails fail"""
    assert validate_email("plainaddress") is False
    assert validate_email("@") is False
    assert validate_email("@.com") is False
    assert validate_email("@missingusername.com") is False
    assert validate_email("username@.com") is False
    assert validate_email("username@domain..com") is False
    assert validate_email("username@domain.c") is False
    assert validate_email("username@domain.c@om") is False
    assert validate_email("username@domain.c#om") is False


def test_empty_email():
    """Ensure empty email fails"""
    assert validate_email("") is False
    assert validate_email(" ") is False
    assert validate_email("  ") is False
