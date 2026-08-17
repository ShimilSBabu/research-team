from src.prompt_factory.prompt_manager import get_prompt
from src.state import AgentState, DecomposerState
from src.model import call_llm

from time import perf_counter
from langchain_core.messages import SystemMessage, HumanMessage
from logging import getLogger
logger=getLogger()

async def decomposer_node(state:AgentState):
    logger.info(msg="Initiating decomposer node.")
    start_time=perf_counter()
    user_query=state.query.query
    decomposer_system_prompt=get_prompt(module_type="agent", module_name="decomposer")
    decomposer_system_prompt=decomposer_system_prompt["content"].format(query=user_query)
    messages=[
        SystemMessage(content=decomposer_system_prompt),
        HumanMessage(content=user_query)
    ]
    logger.info(msg="Decomposing the task.")
    decomposed_task_list=await call_llm(messages=messages, temperature=0.1, llm_purpose="Decomposer Agent",
                      structured_output=DecomposerState)
    logger.info(msg=f"Decomposed task list generated.\n{decomposed_task_list["content"]}")
    latency = perf_counter() - start_time
    logger.info(msg=f"Decomposed Task List. Latency: {latency:.6f} seconds\n{decomposed_task_list}")

    return {
        "decomposer": decomposed_task_list["content"]
        }