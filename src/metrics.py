"""
Metrics Collection — Track and compare performance between approaches.

Provides tools for measuring token usage, latency, cost, and output quality
across the baseline (single-agent) and proposed (multi-agent) approaches.
"""

import time
import json
from dataclasses import dataclass, field, asdict
from typing import Optional
from contextlib import contextmanager


# ── Pricing (per 1K tokens, as of 2026) ──────────────────────────

PRICING = {
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
}


@dataclass
class MetricsResult:
    """Stores all performance metrics for a single run."""

    approach: str                         # "baseline" or "proposed"
    task_id: str = ""
    task_text: str = ""

    # Token usage
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    # Timing
    latency_ms: int = 0

    # Cost
    model: str = "gpt-3.5-turbo"
    estimated_cost_usd: float = 0.0

    # Quality (filled in during evaluation)
    output_quality_score: Optional[float] = None     # 1-5 human rating
    explanation_quality_score: Optional[float] = None  # 1-5 human rating
    confidence: float = 0.0

    # Raw data
    summary: str = ""
    explanation: str = ""

    def compute_cost(self) -> float:
        """Calculate estimated API cost based on token usage and model."""
        prices = PRICING.get(self.model, PRICING["gpt-3.5-turbo"])
        input_cost = (self.prompt_tokens / 1000) * prices["input"]
        output_cost = (self.completion_tokens / 1000) * prices["output"]
        self.estimated_cost_usd = round(input_cost + output_cost, 6)
        return self.estimated_cost_usd

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


def metrics_from_baseline(baseline_result: dict) -> MetricsResult:
    """Create a MetricsResult from a baseline run result."""
    token_usage = baseline_result.get("token_usage", {})
    m = MetricsResult(
        approach="baseline",
        task_id=baseline_result.get("task_id", ""),
        task_text=baseline_result.get("user_task", ""),
        prompt_tokens=token_usage.get("prompt_tokens", 0),
        completion_tokens=token_usage.get("completion_tokens", 0),
        total_tokens=token_usage.get("total_tokens", 0),
        latency_ms=baseline_result.get("latency_ms", 0),
        model=baseline_result.get("model", "gpt-3.5-turbo"),
        confidence=baseline_result.get("confidence", 0.0),
        summary=baseline_result.get("summary", ""),
        explanation=baseline_result.get("self_explanation", ""),
    )
    m.compute_cost()
    return m


def metrics_from_proposed(pipeline_result: dict) -> MetricsResult:
    """Create a MetricsResult from a multi-agent pipeline run result."""
    # Aggregate token usage across all agent logs
    total_prompt = 0
    total_completion = 0
    total_latency = 0

    for log in pipeline_result.get("agent_logs", []):
        metadata = log.get("metadata", {})
        # Token data will be populated when running with real API
        total_prompt += metadata.get("prompt_tokens", 0)
        total_completion += metadata.get("completion_tokens", 0)
        total_latency += metadata.get("latency_ms", 0)

    m = MetricsResult(
        approach="proposed",
        task_id=pipeline_result.get("task_id", ""),
        task_text=pipeline_result.get("user_task", ""),
        prompt_tokens=total_prompt,
        completion_tokens=total_completion,
        total_tokens=total_prompt + total_completion,
        latency_ms=total_latency,
        model=pipeline_result.get("model", "gpt-3.5-turbo"),
        confidence=pipeline_result.get("overall_confidence", 0.0),
        summary=pipeline_result.get("final_output", ""),
        explanation=pipeline_result.get("decision_trace", ""),
    )
    m.compute_cost()
    return m


def compare_results(
    baseline_metrics: list[MetricsResult],
    proposed_metrics: list[MetricsResult],
) -> str:
    """Generate a comparison table between baseline and proposed approaches.

    Args:
        baseline_metrics: List of MetricsResult from baseline runs.
        proposed_metrics: List of MetricsResult from proposed runs.

    Returns:
        A formatted string comparison table.
    """
    def _avg(values: list[float]) -> float:
        return round(sum(values) / len(values), 4) if values else 0.0

    b_tokens = [m.total_tokens for m in baseline_metrics]
    p_tokens = [m.total_tokens for m in proposed_metrics]
    b_latency = [m.latency_ms for m in baseline_metrics]
    p_latency = [m.latency_ms for m in proposed_metrics]
    b_cost = [m.estimated_cost_usd for m in baseline_metrics]
    p_cost = [m.estimated_cost_usd for m in proposed_metrics]
    b_conf = [m.confidence for m in baseline_metrics]
    p_conf = [m.confidence for m in proposed_metrics]

    table = f"""
{'='*65}
  BASELINE vs. PROPOSED — Comparison Summary
  ({len(baseline_metrics)} tasks each)
{'='*65}

{'Metric':<25} {'Baseline':>15} {'Proposed':>15}
{'-'*65}
{'Avg Total Tokens':<25} {_avg(b_tokens):>15.0f} {_avg(p_tokens):>15.0f}
{'Avg Latency (ms)':<25} {_avg(b_latency):>15.0f} {_avg(p_latency):>15.0f}
{'Avg Cost (USD)':<25} {f'${_avg(b_cost):.6f}':>15} {f'${_avg(p_cost):.6f}':>15}
{'Avg Confidence':<25} {_avg(b_conf):>15.2%} {_avg(p_conf):>15.2%}
{'Has Explanation':<25} {'Self-reported':>15} {'Decision Trace':>15}
{'='*65}
"""
    return table


def save_results(
    baseline_metrics: list[MetricsResult],
    proposed_metrics: list[MetricsResult],
    output_path: str,
) -> None:
    """Save experiment results to a JSON file."""
    results = {
        "baseline": [m.to_dict() for m in baseline_metrics],
        "proposed": [m.to_dict() for m in proposed_metrics],
    }
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
