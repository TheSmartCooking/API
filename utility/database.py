from contextlib import contextmanager

from config.database import get_db_connection

__all__ = ["database_cursor", "extract_error_message"]


@contextmanager
def database_cursor():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        yield cursor
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()


def extract_error_message(message):
    """Extracts a user-friendly error message from a database error message."""
    try:
        cleaner_message = message.split(", ")[1].strip("()'")
        return cleaner_message if "SQL" not in cleaner_message else "Database error"
    except IndexError:
        return "An unknown error occurred"
