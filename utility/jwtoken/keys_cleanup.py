"""
To run this script ensure you're in the root directory of the project.
Run the script with: `python3 -m utility.jwt_keys_cleanup`
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

from jwtoken.tokens import JWT_REFRESH_TOKEN_EXPIRY
from utility.jwtoken.common import get_active_kid

KEYS_DIR = Path("keys")
EXPIRY_DAYS = JWT_REFRESH_TOKEN_EXPIRY.days + 1


def cleanup_old_keys():
    now = datetime.now(timezone.utc)
    active_kid = get_active_kid()

    for kid_dir in KEYS_DIR.iterdir():
        if not kid_dir.is_dir():
            continue
        if kid_dir.name == active_kid:
            continue  # Don't delete active key
        created_at_file = kid_dir / "created_at.txt"
        if not created_at_file.exists():
            continue  # Skip keys without metadata

        with open(created_at_file, "r") as f:
            created_at = datetime.fromisoformat(f.read().strip())

        if (now - created_at) > timedelta(days=EXPIRY_DAYS):
            print(f"Deleting expired key: {kid_dir.name}")
            for item in kid_dir.iterdir():
                item.unlink()
            kid_dir.rmdir()


if __name__ == "__main__":
    cleanup_old_keys()
