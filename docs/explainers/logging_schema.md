# Explanation Logging Schema

> How each agent records its reasoning during collaborative tasks.

---

## Purpose

Every agent in the pipeline must output a **structured reasoning log** alongside its actual output. This log is the input to the Explainer Agent, which synthesizes all logs into a human-readable decision trace.

## Schema Definition

```json
{
  "agent_name": "researcher",
  "task_id": "uuid-v4",
  "timestamp": "2026-03-01T14:30:00Z",
  "input": {
    "description": "What the agent received",
    "data": "..."
  },
  "reasoning": {
    "approach": "How the agent decided to tackle the subtask",
    "key_decisions": [
      "Decision 1 and why",
      "Decision 2 and why"
    ]
  },
  "output": {
    "description": "What the agent produced",
    "data": "..."
  },
  "confidence": 0.92,
  "metadata": {
    "tokens_used": 1250,
    "model": "gpt-4",
    "latency_ms": 3200
  }
}
```

## Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_name` | string | ✅ | Identifier for the agent |
| `task_id` | UUID | ✅ | Links all agent logs for the same task |
| `timestamp` | ISO-8601 | ✅ | When the agent completed its work |
| `input` | object | ✅ | What the agent received from the orchestrator |
| `reasoning` | object | ✅ | How and why the agent made its decisions |
| `output` | object | ✅ | What the agent produced |
| `confidence` | float (0–1) | ✅ | Agent's self-assessed confidence in its output |
| `metadata` | object | ❌ | Token usage, model, latency for cost tracking |

## Design Rationale

- **Structured over freeform**: JSON schema ensures the Explainer Agent can reliably parse logs without ambiguity
- **Confidence scores**: Enable the Explainer to flag low-confidence steps and weight the narrative
- **Metadata**: Captures token usage for the cost comparison metric (baseline vs. proposed)
- **Task ID**: Links all agent logs for recombination — critical when running multiple tasks concurrently

## Open Questions

- [ ] Should `reasoning` include chain-of-thought tokens or just a summary?
- [ ] Should confidence be self-assessed by the agent or computed externally?
- [ ] Should we add a `dependencies` field to track which agent's output was used as input?
