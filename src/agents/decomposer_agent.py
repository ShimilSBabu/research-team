from src.prompt_factory.prompt_manager import get_prompt
from src.state import AgentState, DecomposerState
from src.model import call_llm
from langchain_core.messages import SystemMessage, HumanMessage

def decomposer_node(state:AgentState):
    user_query=state.query.query
    decomposer_system_prompt=get_prompt(module_type="agent", module_name="decomposer")
    decomposer_system_prompt=decomposer_system_prompt["content"].format(query=user_query)
       
    # print(f"decomposer_system_prompt\n{decomposer_system_prompt}")
    messages=[
        SystemMessage(content=decomposer_system_prompt),
        HumanMessage(content=user_query)
    ]
    response=call_llm(messages=messages, temperature=0.1, llm_purpose="Decomposer Agent",
                      structured_output=DecomposerState)
    print(f"response: {response}")