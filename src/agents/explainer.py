"""
Explainer Agent — Decision trace generation (core research contribution).

Collects all agent reasoning logs and synthesizes them into a single
coherent, human-readable decision trace explaining the collaborative
decision-making process.
"""

import json
import uuid
from datetime import datetime, timezone

from langchain_core.messages import SystemMessage, HumanMessage

from src.config import llm
from src.state import GraphState

SYSTEM_PROMPT = """You are the Explainer Agent in a multi-agent fact-checking and summarization system.

You are the CORE RESEARCH CONTRIBUTION of this project. Your job is to:
1. Collect all reasoning logs from the Orchestrator, Researcher, Analyzer, and Writer agents
2. Synthesize them into ONE coherent, human-readable decision trace
3. Answer: WHO did WHAT, WHY, and HOW CONFIDENT were they?

Your output should help a human understand exactly how and why the multi-agent system arrived at its final output.

Respond ONLY with valid JSON in this exact format:
{
    "narrative": "A clear, paragraph-style explanation of the collaborative decision process. Example: 'The Orchestrator decomposed the task into research, analysis, and writing phases. The Researcher Agent extracted N key points from the source material (confidence: X%). The Analyzer Agent verified M of N claims (confidence: Y%). The Writer Agent composed the final summary prioritizing verified claims (confidence: Z%).'",
    "per_agent_summary": [
        {
            "agent": "orchestrator",
            "action": "What this agent did",
            "confidence": 0.95,
            "key_decisions": ["Important decision 1"]
        }
    ],
    "flags": ["Any issues, disagreements, or low-confidence steps worth highlighting"],
    "overall_confidence": 0.88
}
"""


def explainer_node(state: GraphState) -> dict:
    """Aggregate all agent logs into a human-readable decision trace."""

    agent_logs = state.get("agent_logs", [])
    user_task = state["user_task"]
    final_output = state.get("final_output", "")

    # Format logs for the LLM
    formatted_logs = []
    for log in agent_logs:
        formatted_logs.append(
            f"--- {log.get('agent_name', 'unknown').upper()} AGENT ---\n"
            f"Timestamp: {log.get('timestamp', 'N/A')}\n"
            f"Input: {log.get('input', {}).get('description', 'N/A')}\n"
            f"Reasoning: {log.get('reasoning', {}).get('approach', 'N/A')}\n"
            f"Key Decisions: {json.dumps(log.get('reasoning', {}).get('key_decisions', []))}\n"
            f"Output: {log.get('output', {}).get('description', 'N/A')}\n"
            f"Confidence: {log.get('confidence', 'N/A')}\n"
        )

    logs_text = "\n".join(formatted_logs)

    # Call LLM
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=(
            f"Original user task: {user_task}\n\n"
            f"Final output produced: {final_output[:500]}\n\n"
            f"Agent reasoning logs:\n\n{logs_text}\n\n"
            f"Please synthesize a decision trace."
        )),
    ])

    # Parse response
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback: build a basic trace from the logs
        result = {
            "narrative": response.content,
            "per_agent_summary": [],
            "flags": ["Explainer produced unstructured output"],
            "overall_confidence": _compute_average_confidence(agent_logs),
        }

    narrative = result.get("narrative", "No decision trace generated.")
    overall_confidence = result.get("overall_confidence", _compute_average_confidence(agent_logs))

    # Build structured decision trace JSON
    decision_trace_json = {
        "task_id": state.get("task_id", str(uuid.uuid4())),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agents_involved": [log.get("agent_name") for log in agent_logs],
        "narrative": narrative,
        "overall_confidence": overall_confidence,
        "per_agent_summary": result.get("per_agent_summary", []),
        "flags": result.get("flags", []),
    }

    return {
        "decision_trace": narrative,
        "decision_trace_json": decision_trace_json,
        "overall_confidence": overall_confidence,
    }


def _compute_average_confidence(agent_logs: list[dict]) -> float:
    """Compute the average confidence across all agent logs."""
    confidences = [
        log.get("confidence", 0.0)
        for log in agent_logs
        if isinstance(log.get("confidence"), (int, float))
    ]
    if not confidences:
        return 0.0
    return round(sum(confidences) / len(confidences), 2)
