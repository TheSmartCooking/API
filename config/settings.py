import os
from datetime import timedelta

from dotenv import load_dotenv

# Load environment variables from `.env` file
load_dotenv()


# Pagination configuration
DEFAULT_PAGE_SIZE = 10


class Config:
    # Database configuration
    MYSQL_HOST = os.getenv("DB_HOST", "host.docker.internal")
    MYSQL_USER = os.getenv("DB_USERNAME", "root")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "myrootpassword")
    MYSQL_DB = os.getenv("DB_NAME", "smartcooking")
    MYSQL_CURSORCLASS = "DictCursor"

    # JWT configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRY = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRY = timedelta(days=30)

    # Image upload folder
    IMAGES_FOLDER = os.path.join(os.getcwd(), "pictures")
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1 MB


if not os.path.exists(Config.IMAGES_FOLDER):
    os.makedirs(Config.IMAGES_FOLDER)
