import os
from dotenv import load_dotenv

load_dotenv()

# Logging Config
LOG_FOLDER=os.getenv("LOG_FOLDER", "logs")
LOG_FILE_NAME=os.getenv("LOG_FILE_NAME", "logs/streamlit.log")
LOG_FORMAT=os.getenv("LOG_FORMAT", "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s")
LOG_PROJECT_FILTER=os.getenv("LOG_PROJECT_FILTER", True)
LOG_PROJECT_NAME=os.getenv("LOG_PROJECT_NAME", "frontend") # Change to project name if necessary
LOG_TIMING=os.getenv("LOG_TIMING", "midnight")
LOG_INTERVAL=os.getenv("LOG_INTERVAL", 1)
LOG_BACKUP_COUNT=os.getenv("LOG_BACKUP_COUNT", 30)
LOG_CONSOLE_HANDLER=os.getenv("LOG_CONSOLE_HANDLER", "DEBUG")
LOG_FILE_HANDLER=os.getenv("LOG_FILE_HANDLER", "INFO")
LOG_ROOT_LOGGER=os.getenv("LOG_ROOT_LOGGER", "DEBUG")

# Streamlit
BACKEND_ENDPOINT=os.getenv("BACKEND_ENDPOINT", "http://127.0.0.1:8000/")

# Personal
SENDER_EMAIL_ID=os.getenv("SENDER_EMAIL_ID", "")
RECEIVER_EMAIL_ID=os.getenv("RECEIVER_EMAIL_ID", "")
GMAIL_CREDENTIALS_PATH=os.getenv("GMAIL_CREDENTIALS_PATH", os.path.join("frontend", "credentials.json"))
GMAIL_TOKEN_PATH=os.getenv("GMAIL_TOKEN_PATH", os.path.join("frontend", "token.json"))