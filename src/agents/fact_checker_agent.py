from src.model import call_llm
from src.state import AgentState, FactCheckerState
from src.prompt_factory.prompt_manager import get_prompt

from langchain_core.messages import SystemMessage, HumanMessage
from logging import getLogger

logger=getLogger(__name__)

async def fact_checker_node(state:AgentState):
    logger.info(msg="Initializing Fact checker node.")
    user_query=state.query.query
    fact_checker_system_prompt=get_prompt(module_type="agent", module_name="Fact Checker ")
    fact_checker_system_prompt=fact_checker_system_prompt["content"].format(query=user_query)
    logger.info(msg="Setting up the fact checker.")
    research_results_list=[]
    for research_result in state.researcher.research_results:
        research_results_list.append(research_result["task"])
        research_results_list.append(research_result["websearch_result"])
    combined_research_results=("-"*50+"\n").join(research_results_list)
    logger.info(msg="Collected research results.")
    messages=[
        SystemMessage(content=fact_checker_system_prompt),
        HumanMessage(content=combined_research_results)
    ]
    logger.info(msg="Fact checking.")
    response=await call_llm(messages=messages, structured_output=FactCheckerState, llm_purpose="Fact Checker Agent", temperature=0.0)
    fact_check_report=response["content"]
    if response["status"]:
        logger.info(msg=f"Fact check successful. Fact Check Report\n{fact_check_report}")
        return {"fact_checker":fact_check_report}
    else:
        logger.critical(msg=f"Fact check unsuccessful. Fact Check Report\n{fact_check_report}")
        return {
            "fact_checker":{
                "fact_check_log": {
                    "single_line_log":fact_check_report
                }
            }
        }