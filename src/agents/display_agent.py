from src.state import AgentState

from logging import getLogger

logger=getLogger(__name__)
async def display_node(state:AgentState):
    logger.info(msg="Initializing the display node.")
    research_report=state.writer.draft_research_report
    logger.info(msg="Collected the final research report.")
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