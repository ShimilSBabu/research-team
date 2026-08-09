from utils.config import (
    LOG_FOLDER, LOG_PROJECT_FILTER, LOG_PROJECT_NAME, LOG_TIMING, LOG_INTERVAL, LOG_BACKUP_COUNT,
    LOG_CONSOLE_HANDLER, LOG_FILE_HANDLER, LOG_ROOT_LOGGER, LOG_FILE_NAME, LOG_FORMAT
)

import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from rich.logging import RichHandler

LOG_LEVEL_DICT={
    "DEBUG":logging.DEBUG,
    "INFO":logging.INFO,
    "WARNING":logging.WARNING,
    "ERROR":logging.ERROR,
    "CRITICAL":logging.CRITICAL,
}
log_dir = Path(LOG_FOLDER)
log_dir.mkdir(exist_ok=True)

class ProjectFilter(logging.Filter):
    def filter(self, record):
        return record.name.startswith(LOG_PROJECT_NAME)
    

formatter = logging.Formatter(LOG_FORMAT)

console_handler = RichHandler(
    rich_tracebacks=True,
    show_path=False,
)
console_handler.setLevel(LOG_LEVEL_DICT[LOG_CONSOLE_HANDLER])
if LOG_PROJECT_FILTER:
    console_handler.addFilter(ProjectFilter())
# console_handler.setFormatter(formatter)

file_handler = TimedRotatingFileHandler(
    LOG_FILE_NAME,
    when=LOG_TIMING,
    interval=LOG_INTERVAL,
    backupCount=LOG_BACKUP_COUNT
)
file_handler.setLevel(LOG_LEVEL_DICT[LOG_FILE_HANDLER])
file_handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL_DICT[LOG_ROOT_LOGGER])

root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)