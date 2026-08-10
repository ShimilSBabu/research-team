from src.prompt_factory.prompt_manager import get_prompt
from src.utils import logging_config
from logging import getLogger

logger=getLogger(__name__)
logger.info("trial logging..")

def main():
    print("Hello from research-team!")
    prompt=get_prompt()
    print(f"prompt: {prompt}")


if __name__ == "__main__":
    main()
