"""
Analyzer Agent — Fact-checking and claim verification.

Receives the Researcher's extracted key points and verifies
each claim, marking them as verified, unverified, or disputed.
"""

import json
import uuid
from datetime import datetime, timezone

from langchain_core.messages import SystemMessage, HumanMessage

from src.config import llm
from src.state import GraphState

SYSTEM_PROMPT = """You are the Analyzer Agent in a multi-agent fact-checking and summarization system.

Your job is to:
1. Review each key point/claim extracted by the Researcher Agent
2. Assess whether each claim is accurate based on your knowledge
3. Mark each claim as: "verified", "unverified", or "disputed"
4. Provide a brief justification for each verification decision

Respond ONLY with valid JSON in this exact format:
{
    "verified_claims": [
        {
            "claim": "The original claim text",
            "status": "verified|unverified|disputed",
            "justification": "Why you made this determination",
            "confidence": 0.90
        }
    ],
    "summary": "Overall assessment of claim accuracy",
    "analysis_reasoning": "Your approach to fact-checking these claims",
    "confidence": 0.85
}
"""


def analyzer_node(state: GraphState) -> dict:
    """Fact-check the Researcher's extracted claims."""

    research_output = state.get("research_output", "")
    user_task = state["user_task"]

    # Call LLM
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=(
            f"Here are the key points extracted by the Researcher Agent:\n\n"
            f"{research_output}\n\n"
            f"Original task: {user_task}\n\n"
            f"Please fact-check each claim."
        )),
    ])

    # Parse response
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        result = {
            "verified_claims": [],
            "summary": "Could not parse fact-check results",
            "analysis_reasoning": "Fallback: unable to verify claims",
            "confidence": 0.4,
        }

    confidence = result.get("confidence", 0.75)
    analysis_output = json.dumps(result, indent=2)

    # Count verification statuses
    claims = result.get("verified_claims", [])
    verified_count = sum(1 for c in claims if c.get("status") == "verified")
    unverified_count = sum(1 for c in claims if c.get("status") == "unverified")
    disputed_count = sum(1 for c in claims if c.get("status") == "disputed")

    # Build reasoning log
    task_id = state.get("task_id", str(uuid.uuid4()))
    agent_log = {
        "agent_name": "analyzer",
        "task_id": task_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": {
            "description": "Key points from Researcher for fact-checking",
            "data": research_output,
        },
        "reasoning": {
            "approach": "Reviewed each claim and assessed accuracy based on training knowledge",
            "key_decisions": [
                result.get("analysis_reasoning", "Fact-checked each claim individually"),
                f"Results: {verified_count} verified, {unverified_count} unverified, {disputed_count} disputed",
            ],
        },
        "output": {
            "description": f"Fact-checked {len(claims)} claims: {verified_count} verified, {unverified_count} unverified, {disputed_count} disputed",
            "data": analysis_output,
        },
        "confidence": confidence,
        "metadata": {
            "model": llm.model_name,
        },
    }

    return {
        "analysis_output": analysis_output,
        "agent_logs": [agent_log],
    }
