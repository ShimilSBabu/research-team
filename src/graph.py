from src.agents.decomposer_agent import decomposer_node
from src.agents.researcher_agent import researcher_node
from src.agents.fact_checker_agent import fact_checker_node
from src.agents.writer_agent import writer_node
from src.agents.critic_agent import critic_node
from src.agents.display_agent import display_node
from src.conditional_edges import dispatch_researchers, critic_decision
from src.state import AgentState

from time import perf_counter
from langgraph.graph import StateGraph, START, END
from logging import getLogger

logger=getLogger(__name__)

def build_graph():
    logger.info(msg="Building the graph.")
    start_time=perf_counter()
    graph_builder=StateGraph(AgentState)

    # Defining the nodes
    logger.info(msg="Adding the nodes.")
    graph_builder.add_node(node="decomposer", action=decomposer_node)
    graph_builder.add_node(node="researcher", action=researcher_node)
    graph_builder.add_node(node="fact_checker", action=fact_checker_node)
    graph_builder.add_node(node="writer", action=writer_node)
    graph_builder.add_node(node="critic", action=critic_node)
    graph_builder.add_node(node="display", action=display_node)


    # Defining the edges
    logger.info(msg="Creating the connections.")
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
    graph_builder.add_edge("writer", "critic")
    graph_builder.add_conditional_edges(
        source="critic",
        path=critic_decision,
        path_map={
            "rewrite":"writer",
            "proceed":"display"
        }
    )
    graph_builder.add_edge("display", END)

    # Compiling the graph
    logger.info(msg="Compiling the graph.")
    graph=graph_builder.compile()
    latency = perf_counter() - start_time
    logger.info(msg=f"Graph built successfully. Latency: {latency:.6f} seconds.")
    return graph