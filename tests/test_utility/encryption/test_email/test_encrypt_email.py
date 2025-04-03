from utility.encryption import encrypt_email


def test_encrypt_email(sample_email):
    """Ensure encrypt_email returns an encrypted email"""
    encrypted_email = encrypt_email(sample_email)

    assert isinstance(encrypted_email, str)


def test_encrypt_email_non_empty(sample_email):
    """Ensure encrypt_email returns a non-empty string"""
    encrypted_email = encrypt_email(sample_email)
    assert len(encrypted_email) > 0


def test_encrypt_email_different(sample_email):
    """Ensure encrypt_email returns a different value than the original email"""
    encrypted_email = encrypt_email(sample_email)
    assert encrypted_email != sample_email


def test_encrypt_email_inconsistent(sample_email):
    """Ensure encrypt_email returns different values for the same input"""
    encrypted_email = encrypt_email(sample_email)
    assert encrypted_email != encrypt_email(sample_email)


def test_characters_not_in_encrypted_email(sample_email):
    """Ensure encrypt_email does not contain certain characters"""
    encrypted_email = encrypt_email(sample_email)
    assert "@" not in encrypted_email
    assert "." not in encrypted_email
