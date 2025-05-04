import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOGS_DIRECTORY = "logs"


def setup_logging():
    # Create a logger
    logger = logging.getLogger("Smart_Cooking-API")
    logger.setLevel(logging.DEBUG)

    # Create a file handler that rotates logs daily
    current_time = datetime.datetime.now().strftime("%Y-%m-%d")

    # Create a directory for logs if it doesn't exist
    if not os.path.exists(LOGS_DIRECTORY):
        os.makedirs(LOGS_DIRECTORY)
    log_filename = f"{LOGS_DIRECTORY}/{current_time}.log"

    # Set up timed rotating file handler
    file_handler = TimedRotatingFileHandler(
        log_filename,
        when="midnight",  # Rotate logs every midnight
        interval=1,  # Every 1 day
        backupCount=90,  # Keep the last 90 days of logs
    )
    file_handler.setLevel(logging.DEBUG)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logging setup complete.")

    return logger
