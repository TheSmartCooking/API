import os

from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables from `.env` file
load_dotenv()


class Config:
    MYSQL_HOST = os.getenv("DB_HOST", "localhost")
    MYSQL_USER = os.getenv("DB_USERNAME")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
    MYSQL_DB = os.getenv("DB_NAME")
    MYSQL_CURSORCLASS = "DictCursor"


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
IMAGES_FOLDER = os.path.join(os.getcwd(), "images")

if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per day", "200 per hour", "30 per minute"],
)
