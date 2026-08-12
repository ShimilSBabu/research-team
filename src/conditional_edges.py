from src.state import AgentState
# from 
from langgraph.types import Send
from logging import getLogger
logger=getLogger(__name__)

def dispatch_researchers(state:AgentState):
    logger.info(msg="Preparing researchers")
    user_query=state.query.query
    logger.debug(msg=f"Fetched user query.\n{user_query}")
    sub_topics_list=state.decomposer.tasks
    logger.debug(msg=f"Collected sub-topics list.\n{sub_topics_list}")
    research_topics_list=[{"research_topic": user_query, "research_sub_topic": sub_topic, "researcher_id":str(index)} for index, sub_topic in enumerate(sub_topics_list)]
    logger.debug(msg=f"Created research topics.\n{research_topics_list}")
    task_list = [Send(node="researcher", arg=research_topic_element) for research_topic_element in research_topics_list]
    logger.info(msg=f"Dispatching {len(task_list)} researchers.")
    return task_list


def critic_decision(state:AgentState):
    logger.info(msg="Critic deciding.")
    critic_score=state.critic.critic_report.critic_score
    logger.info(msg="Considering critic score.")
    if critic_score < 0.5:
        if state.critic.critic_iteration_count >= state.critic.critic_max_iteration:
            logger.info(msg=f"Low citic score: {critic_score}/1.00. Proceeding forward as critic reached maximum iteration limit.")
            return "proceed"
        logger.info(msg=f"Low citic score: {critic_score}/1.00. Rewriting.")
        return "rewrite"
    logger.info(msg=f"Good critic score: {critic_score}/1.00. Proceeding to final review.")
    return "proceed"