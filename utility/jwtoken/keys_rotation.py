"""
Rotate the keys used for JWT signing.
Run the script with: `python3 -m utility.jwtoken.keys_rotation`
"""

import secrets
import subprocess
from datetime import datetime, timezone

from config.jwtoken import (
    ACTIVE_KID_FILE,
    CREATED_AT_FILE,
    KEY_DIR,
    PRIVATE_KEY_FILE,
    PUBLIC_KEY_FILE,
)


def rotate_keys():
    new_kid = secrets.token_hex(8)
    new_key_dir = KEY_DIR / new_kid
    new_key_dir.mkdir(parents=True, exist_ok=False)

    private_key_path = new_key_dir / PRIVATE_KEY_FILE
    public_key_path = new_key_dir / PUBLIC_KEY_FILE
    created_at_path = new_key_dir / CREATED_AT_FILE

    # Generate private key
    subprocess.run(
        [
            "openssl",
            "genpkey",
            "-algorithm",
            "RSA",
            "-out",
            str(private_key_path),
            "-pkeyopt",
            "rsa_keygen_bits:2048",
        ],
        check=True,
    )

    # Extract public key
    subprocess.run(
        [
            "openssl",
            "rsa",
            "-pubout",
            "-in",
            str(private_key_path),
            "-out",
            str(public_key_path),
        ],
        check=True,
    )

    # Set new active KID
    ACTIVE_KID_FILE.write_text(new_kid)

    # Save creation time
    created_at_path.write_text(datetime.now(timezone.utc).isoformat())


if __name__ == "__main__":
    rotate_keys()
