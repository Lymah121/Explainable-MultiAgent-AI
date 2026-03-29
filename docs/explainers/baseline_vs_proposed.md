# Baseline vs. Proposed Comparison

> Experimental design for comparing single-agent and multi-agent approaches.

---

## Purpose

The rubric requires a clear **"Baseline vs. Proposed"** comparison. This document defines both approaches and how they'll be evaluated.

## Baseline: Single-Agent

A single LLM prompt handles the entire task:
- Input: same user task (e.g., "Summarize and fact-check this article")
- Process: one GPT-4 call with a comprehensive prompt
- Output: final result only (no decision trace)
- Explanation: none, or self-generated ("Here's why I did this")

## Proposed: Multi-Agent + Explainer

The full pipeline as designed:
- Orchestrator decomposes the task
- Researcher, Analyzer, Writer each handle subtasks with logged reasoning
- Explainer aggregates logs into a decision trace
- Output: final result + human-readable decision trace

## Comparison Metrics

| Metric | How Measured | Baseline | Proposed |
|--------|-------------|----------|----------|
| **Output Quality** | Human evaluation (1–5 scale) or F1 on fact-checking | ✓ | ✓ |
| **Token Usage** | Total tokens consumed (input + output) | ✓ | ✓ |
| **Latency** | End-to-end time in seconds | ✓ | ✓ |
| **Cost** | API cost in USD | ✓ | ✓ |
| **Explanation Quality** | User study (comprehensibility, accuracy) | N/A | ✓ |
| **User Trust** | Likert scale survey (1–5) | ✓ (no explanation) | ✓ (with explanation) |

## Hypothesis

The multi-agent system with the Explainer Agent will:
1. Produce **higher quality** outputs due to task decomposition and specialization
2. Use **more tokens** but provide proportional value through explainability
3. Significantly **increase user trust** when decision traces are provided

## Open Questions

- [ ] How many benchmark tasks to run? (Minimum 10 suggested)
- [ ] What domain for benchmark tasks? (Research articles, news, claims?)
- [ ] Should the single-agent baseline also get a "explain your reasoning" prompt for fairness?
