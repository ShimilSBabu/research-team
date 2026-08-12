from src.agents.decomposer_agent import decomposer_node
from src.agents.researcher_agent import researcher_node
from src.agents.fact_checker_agent import fact_checker_node
from src.agents.writer_agent import writer_node
from src.conditional_edges import dispatch_researchers
from src.state import AgentState

from langgraph.graph import StateGraph, START, END
from logging import getLogger

logger=getLogger(__name__)

def build_graph():
    graph_builder=StateGraph(AgentState)

    # Defining the nodes
    graph_builder.add_node(node="decomposer", action=decomposer_node)
    graph_builder.add_node(node="researcher", action=researcher_node)
    graph_builder.add_node(node="fact_checker", action=fact_checker_node)
    graph_builder.add_node(node="writer", action=writer_node)


    # Defining the edges
    graph_builder.add_edge(START, "decomposer")
    graph_builder.add_conditional_edges(
        source="decomposer", 
        path=dispatch_researchers,
        path_map={
            "researcher": "researcher"
        }
        )
    graph_builder.add_edge("researcher", "fact_checker")
    graph_builder.add_edge("fact_checker", "writer")
    graph_builder.add_edge("writer", END)

    # Compiling the graph
    graph=graph_builder.compile()

    return graph