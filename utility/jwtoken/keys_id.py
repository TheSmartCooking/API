from jwtoken.exceptions import TokenError


def get_active_kid():
    with open("keys/active_kid.txt", "r") as f:
        return f.read().strip()


def load_private_key(kid):
    with open(f"keys/{kid}/private.pem", "rb") as f:
        return f.read()


def load_public_key(kid):
    try:
        with open(f"keys/{kid}/public.pem", "rb") as f:
            return f.read()
    except FileNotFoundError:
        raise TokenError("Unknown key ID", 401)
