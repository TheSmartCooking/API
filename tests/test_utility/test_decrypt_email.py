import pytest

from utility import decrypt_email, encrypt_email


@pytest.fixture
def sample_email():
    return "sample.email@example.com"


def test_decrypt_email_type(sample_email):
    """Ensure decrypt_email returns a string"""
    encrypted_email = encrypt_email(sample_email)
    decrypted_email = decrypt_email(encrypted_email)
    assert isinstance(decrypted_email, str)


def test_decrypt_email_value(sample_email):
    """Ensure decrypt_email returns the original email"""
    encrypted_email = encrypt_email(sample_email)
    decrypted_email = decrypt_email(encrypted_email)
    assert decrypted_email == sample_email
