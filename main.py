from src.graph import build_graph
from src.utils import logging_config

import asyncio
from logging import getLogger

logger=getLogger(__name__)

async def main():
    logger.info(msg="Research team warming up.")
    graph=build_graph()
    logger.info(msg="Warmed up successfully. Waiting for user query.")
    # research_topic=input("Enter the research topic: ")
    research_topic="Research on current trends in Agentic AI domain."
    initial_state={
        "query":{
            "query": research_topic
        }
    }
    logger.info(msg="Research starting.")
    updated_state=await graph.ainvoke(initial_state)
    logger.info(msg=f"Received updated state after research.\n{updated_state}")
    logger.info(msg="Research finished.")
    print(f"updated_state\n{updated_state}")

    # status=updated_state["response"]["status"]
    # if status:
    #     content=updated_state["response"]["content"]

    # return {
    #     "status": status, 
    #     "content":content if content else "Please try again."
    #     }


if __name__ == "__main__":
    asyncio.run(main())