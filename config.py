from dotenv import load_dotenv
import os

# Load environment variables from `.env` file
load_dotenv()

class Config:
    MYSQL_HOST = os.getenv('DB_HOST', 'localhost')
    MYSQL_USER = os.getenv('DB_USERNAME')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD')
    MYSQL_DB = os.getenv('DB_NAME')
    MYSQL_CURSORCLASS = 'DictCursor'