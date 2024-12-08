import os
from datetime import timedelta

from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables from `.env` file
load_dotenv()


class Config:
    # Database configuration
    MYSQL_HOST = os.getenv("DB_HOST", "host.docker.internal")
    MYSQL_USER = os.getenv("DB_USERNAME", "root")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "myrootpassword")
    MYSQL_DB = os.getenv("DB_NAME", "smartcooking")
    MYSQL_CURSORCLASS = "DictCursor"

    # Pagination configuration
    DEFAULT_PAGE = 1
    DEFAULT_PAGE_SIZE = 10

    # JWT configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRY = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRY = timedelta(days=30)

    # Image upload folder
    IMAGES_FOLDER = os.path.join(os.getcwd(), "images")
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1 MB


if not os.path.exists(Config.IMAGES_FOLDER):
    os.makedirs(Config.IMAGES_FOLDER)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per day", "200 per hour", "30 per minute", "3 per second"],
)
