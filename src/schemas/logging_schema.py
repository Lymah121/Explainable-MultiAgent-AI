"""
Explanation Logging Schema — Pydantic Models

Structured format for each agent to record its reasoning during
collaborative tasks. These logs are the input to the Explainer Agent.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, confloat


class InputData(BaseModel):
    """What the agent received from the orchestrator."""
    description: str = Field(..., description="Human-readable description of the input")
    data: str = Field(..., description="The actual input content")


class Reasoning(BaseModel):
    """How and why the agent made its decisions."""
    approach: str = Field(..., description="How the agent decided to tackle the subtask")
    key_decisions: list[str] = Field(
        default_factory=list,
        description="List of decisions the agent made and why"
    )


class OutputData(BaseModel):
    """What the agent produced."""
    description: str = Field(..., description="Human-readable description of the output")
    data: str = Field(..., description="The actual output content")


class Metadata(BaseModel):
    """Optional metadata for cost and performance tracking."""
    tokens_used: Optional[int] = Field(None, description="Total tokens consumed")
    model: Optional[str] = Field(None, description="LLM model used (e.g. gpt-4)")
    latency_ms: Optional[int] = Field(None, description="Processing time in milliseconds")


class AgentLog(BaseModel):
    """
    Complete reasoning log emitted by each agent.

    Every agent in the pipeline must produce one of these alongside
    its actual output. The Explainer Agent collects all AgentLogs
    for a given task_id and synthesizes them into a decision trace.
    """
    agent_name: str = Field(..., description="Identifier for the agent (e.g. 'researcher')")
    task_id: UUID = Field(..., description="Links all agent logs for the same task")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the agent completed its work (ISO-8601)"
    )
    input: InputData = Field(..., description="What the agent received")
    reasoning: Reasoning = Field(..., description="How the agent made its decisions")
    output: OutputData = Field(..., description="What the agent produced")
    confidence: confloat(ge=0.0, le=1.0) = Field(
        ..., description="Agent's self-assessed confidence (0.0 to 1.0)"
    )
    metadata: Optional[Metadata] = Field(
        None, description="Token usage, model, latency for cost tracking"
    )
