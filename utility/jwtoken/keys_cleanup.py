"""
To run this script ensure you're in the root directory of the project.
Run the script with: `python3 -m utility.jwtoken.keys_cleanup`
"""

from datetime import datetime, timedelta, timezone

from config.jwtoken import CREATED_AT_FILE, KEYS_DIR
from jwtoken.tokens import JWT_REFRESH_TOKEN_EXPIRY
from utility.jwtoken.common import get_active_kid

EXPIRY_DAYS = JWT_REFRESH_TOKEN_EXPIRY.days + 1


def cleanup_old_keys():
    current_time = datetime.now(timezone.utc)
    active_kid = get_active_kid()

    for kid_dir in KEYS_DIR.iterdir():
        if not kid_dir.is_dir():
            continue
        if kid_dir.name == active_kid:
            continue  # Don't delete active key
        created_at_file = kid_dir / CREATED_AT_FILE
        if not created_at_file.exists():
            continue  # Skip keys without metadata

        with open(created_at_file, "r") as f:
            created_at = datetime.fromisoformat(f.read().strip())

        if (current_time - created_at) > timedelta(days=EXPIRY_DAYS):
            print(f"Deleting expired key: {kid_dir.name}")
            for item in kid_dir.iterdir():
                item.unlink()
            kid_dir.rmdir()


if __name__ == "__main__":
    cleanup_old_keys()
