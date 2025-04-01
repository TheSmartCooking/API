import pytest

from utility import mask_email


@pytest.mark.parametrize(
    "input_email, expected_output",
    [
        ("john.doe@example.com", "j**n.d*e@e*****e.c*m"),
        ("a@b.com", "a@b.c*m"),  # Short local and domain names remain unchanged
        ("alice.smith@domain.org", "a***e.s***h@d****n.o*g"),
        ("test1234@gmail.com", "t******4@g***l.c*m"),
        ("user.name@sub.example.co.uk", "u**r.n**e@s*b.e*****e.co.uk"),
        ("m@xyz.net", "m@x*z.n*t"),  # Masked single-character domain name
    ],
)
def test_mask_email_valid(input_email, expected_output):
    assert mask_email(input_email) == expected_output
