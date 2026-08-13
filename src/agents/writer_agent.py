from src.model import call_llm
from src.state import AgentState, WriterState
from src.prompt_factory.prompt_manager import get_prompt

import json
from langchain_core.messages import SystemMessage, HumanMessage
from logging import getLogger

logger=getLogger(__name__)

async def writer_node(state:AgentState):
    logger.info(msg="Initializing writer node.")
    research_topic=state.query.query
    logger.info(msg="Collecting the research report.")
    research_results_list=[]
    for research_result in state.researcher.research_results:
        research_results_list.append(research_result["task"])
        research_results_list.append(research_result["websearch_result"])
    research_report=("-"*50+"\n").join(research_results_list)
    logger.info(msg="Collecting the fact check report.")
    fact_check_report=json.dumps(state.fact_checker.model_dump()["fact_check_results"])
    logger.info(msg="Checking for critic feedback.")
    critic_feedback=state.critic.critic_report.critic_feedback
    logger.info("Setting up the writer.")
    writer_system_prompt=get_prompt(module_type="agent", module_name="writer")
    writer_system_prompt=writer_system_prompt["content"].format(research_topic=research_topic, research_report=research_report, fact_check_report=fact_check_report, critic_feedback=critic_feedback)
    messages=[
        SystemMessage(content=writer_system_prompt),
        HumanMessage(content="Prepare a professional research report.")
    ]
    logger.info(msg="Writing the draft report.")
    draft_report=await call_llm(messages=messages, structured_output=WriterState, temperature=0.5, llm_purpose="Writer Agent")
    logger.info(msg=f"Draft report generated.\n{draft_report["content"]}")

    return {
        "writer": draft_report["content"]
    }