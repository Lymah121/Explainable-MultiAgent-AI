"""
Researcher Agent — Key point and claim extraction.

Reads the source material (provided in the user task) and extracts
the most important information, claims, and key points.
"""

import json
import uuid
from datetime import datetime, timezone

from langchain_core.messages import SystemMessage, HumanMessage

from src.config import llm
from src.state import GraphState

SYSTEM_PROMPT = """You are the Researcher Agent in a multi-agent fact-checking and summarization system.

Your job is to:
1. Carefully read the provided source material
2. Extract the key points, claims, and important facts
3. Identify which claims are verifiable vs. opinions

Respond ONLY with valid JSON in this exact format:
{
    "key_points": [
        {
            "point": "A specific claim or key point",
            "type": "fact|opinion|statistic",
            "verifiable": true
        }
    ],
    "summary_of_source": "Brief description of what the source material covers",
    "extraction_reasoning": "Why you chose these particular points",
    "confidence": 0.90
}
"""


def researcher_node(state: GraphState) -> dict:
    """Extract key points and claims from the user's source material."""

    user_task = state["user_task"]
    subtasks = state.get("subtasks", [])

    # Find the researcher's specific instruction from orchestrator
    researcher_instruction = user_task
    for subtask in subtasks:
        if subtask.get("agent") == "researcher":
            researcher_instruction = subtask.get("instruction", user_task)
            break

    # Call LLM
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Source material to analyze:\n\n{researcher_instruction}\n\nOriginal task: {user_task}"),
    ])

    # Parse response
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        result = {
            "key_points": [{"point": user_task, "type": "fact", "verifiable": True}],
            "summary_of_source": "Could not parse source material properly",
            "extraction_reasoning": "Fallback: treated entire input as a single claim",
            "confidence": 0.5,
        }

    confidence = result.get("confidence", 0.8)
    research_output = json.dumps(result, indent=2)

    # Build reasoning log
    task_id = state.get("task_id", str(uuid.uuid4()))
    agent_log = {
        "agent_name": "researcher",
        "task_id": task_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": {
            "description": "Source material for key point extraction",
            "data": researcher_instruction,
        },
        "reasoning": {
            "approach": "Read the source material and extracted key claims, facts, and opinions",
            "key_decisions": [
                result.get("extraction_reasoning", "Extracted main points from the text"),
                f"Identified {len(result.get('key_points', []))} key points",
            ],
        },
        "output": {
            "description": f"Extracted {len(result.get('key_points', []))} key points from source material",
            "data": research_output,
        },
        "confidence": confidence,
        "metadata": {
            "model": llm.model_name,
        },
    }

    return {
        "research_output": research_output,
        "agent_logs": [agent_log],
    }
