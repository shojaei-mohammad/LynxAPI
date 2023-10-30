import logging
from pathlib import Path

# get the current dir and go up two level
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR_PATH = BASE_DIR / "logs"
# Create the logs directory if it doesn't exist
LOG_DIR_PATH.mkdir(parents=True, exist_ok=True)


def configure_logger() -> logging.Logger:
    """
    Configures and returns a logger instance for the project.

    Parameters:
    - log_file (str): Path to the file where logs will be saved. Default is "project_log.log".

    Returns:
    - logging.Logger: Configured logger instance for the project.
    """
    # Set up logging to file
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        handlers=[
            logging.FileHandler(LOG_DIR_PATH / "project.log"),
            logging.StreamHandler(),  # This will allow logging to console as well
        ],
    )

    return logging.getLogger(__name__)
