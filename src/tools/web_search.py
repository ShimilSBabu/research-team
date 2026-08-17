from src.utils.config import TRAVILY_API_KEY

import os
from time import perf_counter
from tavily import AsyncTavilyClient
from logging import getLogger

from dotenv import load_dotenv
load_dotenv()

logger = getLogger(__name__)
client = AsyncTavilyClient(api_key=TRAVILY_API_KEY)

async def run(query:str="", max_results=5):
    logger.debug(f"Invoking tavily for query: {query}.")
    start_time=perf_counter()
    results=error=""
    try:
        results = await client.search(
            query=query,
            max_results=max_results
        )
    except Exception as error:
        latency = perf_counter() - start_time
        logger.exception("Web search tool error. Latency: {latency:.6f} seconds.")

    latency = perf_counter() - start_time
    logger.debug(f"Tavily responded. Latency: {latency:.6f} seconds.\n{results}")
    return {
            "status":True if results else False,
            "content":results if results else None,
            "error":error if results else None,
            "metadata":{"query": query, "max_results":max_results}
        }
