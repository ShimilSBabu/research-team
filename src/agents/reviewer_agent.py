from src.model import call_llm
from src.state import AgentState
from src.prompt_factory.prompt_manager import get_prompt

async def reviewer_node():
    # print(f"name: ({type(__name__)}): {__name__}")
    res=await call_llm("hi")
    print(f"res: {res}")
    pass