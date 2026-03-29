"""
LangGraph Pipeline — Multi-agent workflow graph.

Wires all agents into a sequential LangGraph workflow:
START → Orchestrator → Researcher → Analyzer → Writer → Explainer → END
"""

from langgraph.graph import StateGraph, START, END

from src.state import GraphState
from src.agents import (
    orchestrator_node,
    researcher_node,
    analyzer_node,
    writer_node,
    explainer_node,
)


def build_graph() -> StateGraph:
    """Build and compile the multi-agent LangGraph workflow."""

    graph = StateGraph(GraphState)

    # Add agent nodes
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("analyzer", analyzer_node)
    graph.add_node("writer", writer_node)
    graph.add_node("explainer", explainer_node)

    # Wire sequential edges (data dependencies require this order)
    graph.add_edge(START, "orchestrator")
    graph.add_edge("orchestrator", "researcher")
    graph.add_edge("researcher", "analyzer")
    graph.add_edge("analyzer", "writer")
    graph.add_edge("writer", "explainer")
    graph.add_edge("explainer", END)

    return graph.compile()


# Pre-compiled graph for import
app = build_graph()
