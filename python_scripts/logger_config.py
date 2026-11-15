import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging():
    # Create a 'logs' folder if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if setup is called twice
    if logger.handlers:
        return

    # Define how the log messages will look
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # 1. Terminal Handler (prints to screen)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)  # Screen only shows INFO and above
    console.setFormatter(formatter)

    # 2. Rotating File Handler (saves to file)
    # Max size 1MB, keeps 3 backups, saves DEBUG and above
    file_handler = RotatingFileHandler(
        log_dir / "etl_pipeline.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(console)
    logger.addHandler(file_handler)
