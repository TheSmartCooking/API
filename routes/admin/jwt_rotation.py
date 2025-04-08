import os
import secrets
import subprocess
from datetime import datetime, timezone

from flask import Blueprint, abort, jsonify, request

from config.ratelimit import limiter

jwt_rotation_blueprint = Blueprint("jwt_rotation", __name__)


@jwt_rotation_blueprint.route("/rotate", methods=["POST"])
@limiter.limit("1 per day")
def rotate_keys():
    """
    Rotate the keys used for JWT signing.
    This endpoint is protected and should only be accessible from localhost.
    """
    if request.remote_addr != "127.0.0.1":
        abort(403)

    new_kid = secrets.token_hex(8)
    key_dir = f"keys/{new_kid}"
    os.makedirs(key_dir, exist_ok=False)

    # Use OpenSSL to generate keys
    subprocess.run(
        [
            "openssl",
            "genpkey",
            "-algorithm",
            "RSA",
            "-out",
            f"{key_dir}/private.pem",
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
            f"{key_dir}/private.pem",
            "-out",
            f"{key_dir}/public.pem",
        ],
        check=True,
    )

    # Update active_kid
    with open("keys/active_kid.txt", "w") as f:
        f.write(new_kid)

    # Save the kid creation time for cleanup purposes
    with open(f"{key_dir}/created_at.txt", "w") as f:
        f.write(datetime.now(timezone.utc).isoformat())

    return jsonify(message=f"KID rotated. New kid: {new_kid}")
