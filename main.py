from src.graph import build_graph
from src.utils import logging_config

from fastapi import FastAPI
import uvicorn
from logging import getLogger

logger=getLogger(__name__)
app=FastAPI()

@app.get(path="/research")
async def main(research_topic:str=""):
    if not research_topic:
        return {
                "status": False, 
                "content":"Please enter an input for research."
            }
    logger.info(msg="Research team warming up.")
    graph=build_graph()
    logger.info(msg=f"Warmed up successfully.\nUser query: {research_topic}")
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

    status=updated_state["response"]["status"]
    content=updated_state["response"]["content"]
    logger.info(f"Final response.\n{content}")

    return {
        "status": status, 
        "content":content if content else "Please try again."
        }


if __name__ == "__main__":
    import os
    uvicorn.run(
        app="main:app",
        host=os.getenv("FASTAPI_HOST", "127.0.0.1"),
        port=os.getenv("FASTAPI_PORT",8080),
        # use_colors=True,
        # reload=True
    )