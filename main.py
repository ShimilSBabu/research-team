from src.agents.decomposer_agent import decomposer_node
from src.state import AgentState

from logging import getLogger
from langgraph.graph import StateGraph

logger=getLogger(__name__)

def main():
    print("Hello from research-team!")
    # state=StateGraph(AgentState)
    user_query={
            "query":"Research on current trends in Agentic AI domain."
        }
    state=AgentState(query=user_query)
    print(f"state\n{state}")

    decomposer_node(state=state)
    # print(f"prompt: {prompt}")


if __name__ == "__main__":
    main()
