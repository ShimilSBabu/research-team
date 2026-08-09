from src.prompt_factory.prompt_manager import get_prompt
from src.state import AgentState
from src.model import get_llm_responce

def decomposer_node(state:AgentState):
    user_query=state.query.query
    decomposer_system_prompt=get_prompt(module_type="agent", module_name="decomposer")
    decomposer_system_prompt=decomposer_system_prompt["content"].format(query=user_query)
       
    print(f"decomposer_system_prompt\n{decomposer_system_prompt}")