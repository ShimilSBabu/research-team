from src.state import AgentState

from time import perf_counter
from logging import getLogger

logger=getLogger(__name__)

async def display_node(state:AgentState):
    logger.info(msg="Initializing the display node.")
    start_time=perf_counter()
    research_report=state.writer.draft_research_report
    latency = perf_counter() - start_time
    logger.info(msg=f"Collected the final research report.  Latency: {latency:.6f} seconds.\n{research_report}")
    if research_report:
        logger.info(msg="Research success.")
        return {
            "response":{
                "status":True,
                "content":research_report,
                }
        }
    logger.info(msg="Research failed.")
    return {
            "response":{
                "status":False
                }
        }