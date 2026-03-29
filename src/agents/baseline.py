"""
Baseline Agent — Single-agent approach for comparison.

A single LLM call handles the entire task: summarization, fact-checking,
and self-explanation in one pass. This serves as the baseline for
comparing against the multi-agent + Explainer pipeline.
"""

import json
import uuid
import time
from datetime import datetime, timezone

from langchain_core.messages import SystemMessage, HumanMessage

from src.config import llm

SYSTEM_PROMPT = """You are a helpful AI assistant. You will be given a task that involves summarizing and fact-checking information.

You must:
1. Extract key claims from the provided material
2. Assess the accuracy of each claim (verified, unverified, or disputed)
3. Write a clear, well-structured summary prioritizing verified claims
4. Explain your reasoning process

Respond ONLY with valid JSON in this exact format:
{
    "key_claims": [
        {
            "claim": "A specific claim",
            "status": "verified|unverified|disputed",
            "justification": "Why this determination"
        }
    ],
    "summary": "Your composed summary text",
    "self_explanation": "A description of your reasoning process — what you did, what you prioritized, and why",
    "confidence": 0.90
}
"""


def run_baseline(user_task: str) -> dict:
    """Run the single-agent baseline on a task.

    Args:
        user_task: The task to process.

    Returns:
        A dict with keys: summary, self_explanation, confidence, raw_response,
        token_usage, latency_ms.
    """
    task_id = str(uuid.uuid4())

    start_time = time.time()

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Task: {user_task}"),
    ])

    latency_ms = int((time.time() - start_time) * 1000)

    # Extract token usage from response metadata
    token_usage = {}
    if hasattr(response, "response_metadata"):
        usage = response.response_metadata.get("token_usage", {})
        token_usage = {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }

    # Parse response
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        result = {
            "key_claims": [],
            "summary": response.content,
            "self_explanation": "Could not generate structured explanation",
            "confidence": 0.5,
        }

    return {
        "task_id": task_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_task": user_task,
        "summary": result.get("summary", response.content),
        "self_explanation": result.get("self_explanation", ""),
        "key_claims": result.get("key_claims", []),
        "confidence": result.get("confidence", 0.5),
        "token_usage": token_usage,
        "latency_ms": latency_ms,
        "model": llm.model_name,
        "approach": "baseline_single_agent",
    }
