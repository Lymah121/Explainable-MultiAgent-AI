"""
Writer Agent — Final summary composition.

Receives verified claims from the Analyzer and composes a coherent,
well-structured summary prioritizing verified information.
"""

import json
import uuid
from datetime import datetime, timezone

from langchain_core.messages import SystemMessage, HumanMessage

from src.config import llm
from src.state import GraphState

SYSTEM_PROMPT = """You are the Writer Agent in a multi-agent fact-checking and summarization system.

Your job is to:
1. Review the verified claims from the Analyzer Agent
2. Compose a clear, well-structured summary
3. Prioritize verified claims; flag any unverified or disputed claims
4. Write in a professional, accessible tone

Respond ONLY with valid JSON in this exact format:
{
    "summary": "Your composed summary text here. This should be a coherent paragraph or short set of paragraphs.",
    "writing_decisions": [
        "Decision 1: why you structured the summary this way",
        "Decision 2: what you included or excluded and why"
    ],
    "claims_included": 3,
    "claims_excluded": 1,
    "exclusion_reasons": ["Reason for excluding each claim"],
    "confidence": 0.90
}
"""


def writer_node(state: GraphState) -> dict:
    """Compose a final summary from verified claims."""

    analysis_output = state.get("analysis_output", "")
    research_output = state.get("research_output", "")
    user_task = state["user_task"]

    # Call LLM
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=(
            f"Original task: {user_task}\n\n"
            f"Researcher's key points:\n{research_output}\n\n"
            f"Analyzer's fact-check results:\n{analysis_output}\n\n"
            f"Please compose the final summary."
        )),
    ])

    # Parse response
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        # If JSON parsing fails, use the raw response as the summary
        result = {
            "summary": response.content,
            "writing_decisions": ["Used raw LLM output as fallback"],
            "claims_included": 0,
            "claims_excluded": 0,
            "exclusion_reasons": [],
            "confidence": 0.6,
        }

    confidence = result.get("confidence", 0.85)
    final_summary = result.get("summary", response.content)

    # Build reasoning log
    task_id = state.get("task_id", str(uuid.uuid4()))
    agent_log = {
        "agent_name": "writer",
        "task_id": task_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": {
            "description": "Verified claims from Analyzer for summary composition",
            "data": analysis_output[:500],  # Truncate for log readability
        },
        "reasoning": {
            "approach": "Composed a summary prioritizing verified claims, flagging unverified ones",
            "key_decisions": result.get("writing_decisions", ["Wrote summary from verified claims"]),
        },
        "output": {
            "description": f"Final summary ({result.get('claims_included', '?')} claims included, {result.get('claims_excluded', '?')} excluded)",
            "data": final_summary,
        },
        "confidence": confidence,
        "metadata": {
            "model": llm.model_name,
        },
    }

    return {
        "final_output": final_summary,
        "agent_logs": [agent_log],
    }
