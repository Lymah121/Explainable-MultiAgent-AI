"""
Graph State — Shared state schema for the LangGraph workflow.

This TypedDict defines the data passed between all nodes in the graph.
Each agent reads from and writes to this shared state.
"""

from typing import TypedDict, Annotated
import operator


class GraphState(TypedDict):
    """Shared state passed through the LangGraph multi-agent pipeline."""

    # --- Input ---
    user_task: str                          # The original user task

    # --- Orchestrator output ---
    subtasks: list[dict]                    # Decomposed subtasks with assignments

    # --- Agent outputs ---
    research_output: str                    # Researcher's extracted key points
    analysis_output: str                    # Analyzer's fact-check results
    final_output: str                       # Writer's composed summary

    # --- Logging ---
    agent_logs: Annotated[list[dict], operator.add]  # Append-only list of AgentLog dicts

    # --- Explainer output ---
    decision_trace: str                     # Human-readable explanation narrative
    decision_trace_json: dict               # Structured JSON decision trace
    overall_confidence: float               # Aggregated confidence score (0.0–1.0)
