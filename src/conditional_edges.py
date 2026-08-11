from src.state import AgentState

from langgraph.types import Send
from logging import getLogger
logger=getLogger(__name__)

def dispatch_researchers(state:AgentState):
    logger.info(msg="Preparing researchers")
    user_query=state.query.query
    logger.debug(msg=f"Fetched user query.\n{user_query}")
    sub_topics_list=state.decomposer.tasks
    logger.debug(msg=f"Collected sub-topics list.\n{sub_topics_list}")
    research_topics_list=[{"research_topic": user_query, "research_sub_topic": sub_topic} for sub_topic in sub_topics_list]
    logger.debug(msg=f"Created research topics.\n{research_topics_list}")
    task_list = [Send(node="researcher", arg=research_topic_element) for research_topic_element in research_topics_list]
    logger.info(msg=f"Dispatching {len(task_list)} researchers.")
    return task_list