"""
Rotate the keys used for JWT signing.
Run the script with: `python3 -m utility.jwtoken.keys_rotation`
"""

import os
import secrets
import subprocess
from datetime import datetime, timezone

from config.jwtoken import ACTIVE_KID_FILE, KEY_DIR, PRIVATE_KEY_FILE, PUBLIC_KEY_FILE


def rotate_keys():
    new_kid = secrets.token_hex(8)
    new_key_dir = f"{KEY_DIR}/{new_kid}"
    os.makedirs(new_key_dir, exist_ok=False)

    # Use OpenSSL to generate keys
    subprocess.run(
        [
            "openssl",
            "genpkey",
            "-algorithm",
            "RSA",
            "-out",
            f"{new_key_dir}/{PRIVATE_KEY_FILE}",
            "-pkeyopt",
            "rsa_keygen_bits:2048",
        ],
        check=True,
    )
    subprocess.run(
        [
            "openssl",
            "rsa",
            "-pubout",
            "-in",
            f"{new_key_dir}/{PRIVATE_KEY_FILE}",
            "-out",
            f"{new_key_dir}/{PUBLIC_KEY_FILE}",
        ],
        check=True,
    )

    # Update active_kid
    with open(ACTIVE_KID_FILE, "w") as f:
        f.write(new_kid)

    # Save the kid creation time for cleanup purposes
    with open(ACTIVE_KID_FILE, "w") as f:
        f.write(datetime.now(timezone.utc).isoformat())
