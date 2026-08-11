from src.utils.config import TRAVILY_API_KEY
import os
from tavily import AsyncTavilyClient
from logging import getLogger

from dotenv import load_dotenv
load_dotenv()

logger = getLogger(__name__)
client = AsyncTavilyClient(api_key=TRAVILY_API_KEY)

async def run(query:str="", max_results=5):
    logger.debug(f"Invoking tavily for query: {query}.")
    results=error=""
    try:
        results = await client.search(
            query=query,
            max_results=max_results
        )
    except Exception as error:
        logger.exception("Web search tool error.")

    logger.debug(f"Tavily responded;\n{results}")
    return {
            "status":True if results else False,
            "content":results if results else None,
            "error":error if results else None,
            "metadata":{"query": query, "max_results":max_results}
        }
