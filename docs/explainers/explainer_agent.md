# The Explainer Agent

> How the Explainer Agent aggregates reasoning logs into a human-readable decision trace.

---

## Role

The Explainer Agent is the **core research contribution** of this project. It is a dedicated agent that:
1. Collects all reasoning logs from the worker agents (Researcher, Analyzer, Writer)
2. Synthesizes them into a **single coherent narrative** explaining the collaborative decision
3. Outputs both a human-readable text explanation and structured data

## How It Works

```
Agent Logs (JSON) → Explainer Agent → Decision Trace (narrative + data)
```

### Input
An array of reasoning logs from all agents that participated in the task, linked by `task_id`.

### Processing
1. **Order** logs chronologically by timestamp
2. **Extract** key decisions, confidence scores, and reasoning from each agent
3. **Identify** points of agreement, disagreement, or uncertainty across agents
4. **Synthesize** into a narrative that answers: *who did what, why, and how confident were they?*

### Output

**Narrative (human-readable):**
> "The Researcher Agent extracted 5 key points from the article (confidence: 92%). The Analyzer Agent verified 4 of 5 claims against external sources (1 claim could not be verified, confidence: 78%). The Writer Agent composed the summary, prioritizing the 4 verified claims. Final confidence: 88%."

**Structured (JSON):**
```json
{
  "task_id": "uuid",
  "agents_involved": ["researcher", "analyzer", "writer"],
  "narrative": "...",
  "overall_confidence": 0.88,
  "per_agent_summary": [
    { "agent": "researcher", "action": "...", "confidence": 0.92 },
    { "agent": "analyzer", "action": "...", "confidence": 0.78 },
    { "agent": "writer", "action": "...", "confidence": 0.95 }
  ],
  "flags": ["1 claim could not be verified"]
}
```

## Design Decisions

- [ ] Should the Explainer use the same LLM (GPT-4) or a smaller model?
- [ ] Should it produce explanations in real-time (streaming) or post-hoc?
- [ ] How should disagreements between agents be surfaced in the narrative?
