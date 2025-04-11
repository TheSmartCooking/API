from datetime import datetime, timedelta, timezone

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.exceptions import InvalidKeyError

from jwtoken.exceptions import TokenError
from jwtoken.tokens import generate_access_token, verify_token
from utility.jwtoken.common import get_active_kid


@pytest.fixture
def active_kid():
    return get_active_kid()


@pytest.fixture
def fake_private_key():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


@pytest.fixture
def public_key(active_kid):
    with open(f"keys/{active_kid}/public.pem", "rb") as f:
        return f.read()


@pytest.fixture
def sample_payload(sample_person_id):
    return {
        "person_id": sample_person_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
        "iat": datetime.now(timezone.utc),
        "token_type": "access",
    }


def test_hs256_forged_token_rejected(sample_person_id, public_key, active_kid):
    headers = {"kid": active_kid, "alg": "HS256"}
    payload = {
        "person_id": sample_person_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
        "iat": datetime.now(timezone.utc),
        "token_type": "access",
    }

    with pytest.raises(InvalidKeyError, match="asymmetric key.*HMAC"):
        jwt.encode(payload, public_key, algorithm="HS256", headers=headers)


def test_tampered_token_expiry_extension(sample_person_id, fake_private_key):
    original_token = generate_access_token(sample_person_id)
    original_payload = jwt.decode(original_token, options={"verify_signature": False})
    original_header = jwt.get_unverified_header(original_token)

    modified_payload = original_payload.copy()
    modified_payload["exp"] = datetime.now(timezone.utc) + timedelta(days=365)

    forged_token = jwt.encode(
        modified_payload, fake_private_key, algorithm="RS256", headers=original_header
    )

    with pytest.raises(TokenError, match="Invalid token"):
        verify_token(forged_token, "access")


def test_unknown_kid_rejected(fake_private_key, sample_payload):
    headers = {"kid": "fake123456"}

    fake_token = jwt.encode(
        sample_payload, fake_private_key, algorithm="RS256", headers=headers
    )

    with pytest.raises(TokenError, match="Unknown key ID"):
        verify_token(fake_token, "access")
