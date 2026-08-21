from src.graph import build_graph
from src.utils import logging_config
from src.utils.config import FASTAPI_HOST, FASTAPI_PORT

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, WebSocketException
import uvicorn
from logging import getLogger
import asyncio

logger=getLogger(__name__)
app=FastAPI()

print("=/"*30)

@app.websocket(path="/research")
async def main(websocket:WebSocket):

    await websocket.accept()

    research_topic=await websocket.receive_text()

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
    researcher_agent_results_list=[]
    async for chunk in graph.astream(input=initial_state, stream_mode="updates"):
        logger.info(msg=f"streaming chunk ({type(chunk)}): {chunk}")
        answer=chunk[list(chunk.keys())[0]]["streaming_display"]
        if list(chunk.keys())[0]=="researcher":
            researcher_agent_results_list.extend(answer)
            combined_researcher_results="\n- ".join(researcher_agent_results_list)
            answer="- "+combined_researcher_results
        if list(chunk.keys())[0]=="fact_checker":
            researcher_agent_results_list=[]
        if answer:
            await websocket.send_json(data={"type": "data", "answer": answer})

    await websocket.send_json(data={"type": "Done"})

    # logger.info(msg=f"Received updated state after research.\n{updated_state}")
    logger.info(msg=f"Received updated state after research.")
    logger.info(msg="Research finished.")

    # status=updated_state["response"]["status"]
    # content=updated_state["response"]["content"]
    # logger.info(f"Final response.\n{content}")
    
    # asyncio.sleep(3)
    # await websocket.close()
    # return {
    #     "status": status, 
    #     "content":content if content else "Please try again."
    #     }


if __name__ == "__main__":
    print("__main__"*30)
    uvicorn.run(
        app="main:app",
        host=FASTAPI_HOST,
        port=FASTAPI_PORT,
        # use_colors=True,
        # reload=True
    )