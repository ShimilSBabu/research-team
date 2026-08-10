from src.agents.decomposer_agent import decomposer_node
from src.state import AgentState
from src.prompt_factory.prompt_manager import get_prompt
from src.utils import logging_config

from logging import getLogger
from langgraph.graph import StateGraph

logger=getLogger(__name__)
logger.info("trial logging..")

def main():
    print("Hello from research-team!")
    # state=StateGraph(AgentState)
    user_query={
            "query":"Research on current trends in Agentic AI domain."
        }
    state=AgentState(query=user_query)
    # print(f"state\n{state}")

    response=decomposer_node(state=state)
    print(f"response ({type(response["content"])}): {response["content"]}")


if __name__ == "__main__":
    main()
