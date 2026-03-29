"""
Orchestrator Agent — Task decomposition and subtask assignment.

Receives the user's task and breaks it down into subtasks
assigned to the Researcher, Analyzer, and Writer agents.
"""

import json
import uuid
from datetime import datetime, timezone

from langchain_core.messages import SystemMessage, HumanMessage

from src.config import llm
from src.state import GraphState

SYSTEM_PROMPT = """You are the Orchestrator Agent in a multi-agent fact-checking and summarization system.

Your job is to:
1. Analyze the user's task
2. Decompose it into exactly 3 subtasks for:
   - **Researcher**: Extract key points and claims from the source material
   - **Analyzer**: Fact-check and verify the extracted claims
   - **Writer**: Compose a final summary based on verified claims

Respond ONLY with valid JSON in this exact format:
{
    "task_breakdown": "Your reasoning for how you decomposed the task",
    "subtasks": [
        {
            "agent": "researcher",
            "instruction": "Specific instruction for the Researcher agent",
            "priority": "high"
        },
        {
            "agent": "analyzer",
            "instruction": "Specific instruction for the Analyzer agent",
            "priority": "high"
        },
        {
            "agent": "writer",
            "instruction": "Specific instruction for the Writer agent",
            "priority": "medium"
        }
    ],
    "confidence": 0.95
}
"""


def orchestrator_node(state: GraphState) -> dict:
    """Decompose user task into subtasks and assign to worker agents."""

    user_task = state["user_task"]

    # Call LLM
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Task: {user_task}"),
    ])

    # Parse response
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback: create default subtasks if LLM doesn't return valid JSON
        result = {
            "task_breakdown": "Default decomposition applied",
            "subtasks": [
                {"agent": "researcher", "instruction": f"Extract key points from: {user_task}", "priority": "high"},
                {"agent": "analyzer", "instruction": "Fact-check all extracted claims", "priority": "high"},
                {"agent": "writer", "instruction": "Write a summary of verified claims", "priority": "medium"},
            ],
            "confidence": 0.7,
        }

    confidence = result.get("confidence", 0.85)

    # Build the reasoning log
    task_id = state.get("task_id", str(uuid.uuid4()))
    agent_log = {
        "agent_name": "orchestrator",
        "task_id": task_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": {
            "description": "Raw user task",
            "data": user_task,
        },
        "reasoning": {
            "approach": "Decomposed the task into 3 subtasks: research, analysis, and writing",
            "key_decisions": [
                result.get("task_breakdown", "Decomposed into research → analysis → writing pipeline"),
            ],
        },
        "output": {
            "description": "Subtask assignments for worker agents",
            "data": json.dumps(result.get("subtasks", [])),
        },
        "confidence": confidence,
        "metadata": {
            "model": llm.model_name,
        },
    }

    return {
        "subtasks": result.get("subtasks", []),
        "agent_logs": [agent_log],
    }
