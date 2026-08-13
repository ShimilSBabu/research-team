from src.model import call_llm
from src.state import AgentState, CriticReport
from src.prompt_factory.prompt_manager import get_prompt

from langchain_core.messages import SystemMessage, HumanMessage
from logging import getLogger

logger= getLogger(__name__)

async def critic_node(state:AgentState):
    logger.info(msg="Initiating critic node.")
    critic_iteration_count=state.critic.critic_iteration_count
    critic_iteration_limit=state.critic.critic_max_iteration
    logger.info(msg=f"Critic iteration count: {critic_iteration_count}/{critic_iteration_limit}")
    research_topic=state.query.query
    draft_report=state.writer.draft_research_report
    critic_system_prompt=get_prompt(module_type="agent", module_name="critic")
    logger.info(msg="Collected necessary info.")
    critic_system_prompt=critic_system_prompt["content"].format(research_topic=research_topic)
    messages=[
        SystemMessage(content=critic_system_prompt),
        HumanMessage(content=draft_report)
    ]
    logger.info(msg="Generating critic report.")
    critic_response=await call_llm(messages=messages, structured_output=CriticReport, llm_purpose="Critic")
    logger.info(msg=f"Critic report generated.\n{critic_response["content"]}")
    return {
        "critic":{
            "critic_report": {
                "critic_feedback":critic_response["content"].critic_feedback,
                "critic_score":critic_response["content"].critic_score
            },
            "critic_iteration_count": critic_iteration_count+1
        },
    }