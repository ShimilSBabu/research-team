import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Environment Constants
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
TRAVILY_API_KEY = os.getenv("TRAVILY_API_KEY", "")

# Logging Constants
LOG_FOLDER="logs"
LOG_FILE_NAME="logs/app.log"
LOG_FORMAT="%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s"
LOG_PROJECT_FILTER=True
LOG_PROJECT_NAME="src" # Change to project name if necessary
LOG_TIMING="midnight"
LOG_INTERVAL=1
LOG_BACKUP_COUNT=30
LOG_CONSOLE_HANDLER="DEBUG"
LOG_FILE_HANDLER="INFO"
LOG_ROOT_LOGGER="DEBUG"
