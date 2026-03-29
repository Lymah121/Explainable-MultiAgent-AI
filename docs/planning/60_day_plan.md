# 60-Day Project Plan

**Project:** Explainable Multi-Agent AI
**Start Date:** February 13, 2026
**End Date:** April 13, 2026
**Course:** COSC 6375 — Graduate Research in Agentic AI and Federated Learning

---

## Overview

| Phase | Weeks | Focus                                    | Rubric Weight             |
| ----- | ----- | ---------------------------------------- | ------------------------- |
| 1     | 1–2  | Foundation: Logging Schema + Base Agents | 30% (Implementation)      |
| 2     | 3–4  | Core: Explainer Agent + Aggregation      | 30% (Implementation)      |
| 3     | 5–6  | Experiment: Baseline vs. Proposed        | 20% (Experimental Design) |
| 4     | 7–8  | Evaluation: Metrics + User Study         | 15% (Outcome Analysis)    |
| 5     | 8–9  | Paper + Presentation                     | 20% (arXiv Report)        |

---

## Week-by-Week Breakdown

### Week 1 (Feb 13–19) — Environment + Logging Schema

- [x] Set up Python environment with LangGraph + OpenAI API
  - Created `venv`, installed all dependencies via `requirements.txt`
  - Created `src/config.py` — loads `.env`, exposes shared `ChatOpenAI` LLM instance
- [x] Define the explanation logging schema (JSON format)
  - `src/schemas/logging_schema.py` — Pydantic models: `AgentLog`, `InputData`, `Reasoning`, `OutputData`, `Metadata`
  - Fixed `datetime.utcnow()` deprecation → `datetime.now(timezone.utc)`
- [x] Create `requirements.txt` and project config
  - `requirements.txt` — `langgraph`, `langchain`, `langchain-openai`, `python-dotenv`, `pydantic`, `pytest`
  - `src/config.py` — validates API key, defaults to `gpt-3.5-turbo` for dev
- [x] Write unit tests for schema validation
  - `tests/test_schema.py` — 18 tests (creation, validation, edge cases) — all passing
  - `tests/test_state.py` — 3 tests (GraphState structure) — all passing
- [x] Document schema in `docs/explainers/logging_schema.md`
  - Already documented (pre-existing)

### Week 2 (Feb 20–26) — Base Agents

- [x] Implement Orchestrator agent (task decomposition)
  - `src/agents/orchestrator.py` — decomposes user task into 3 subtasks (researcher, analyzer, writer)
- [x] Implement Researcher agent (key point extraction)
  - `src/agents/researcher.py` — extracts key points, classifies as fact/opinion/statistic
- [x] Implement Analyzer agent (fact-checking)
  - `src/agents/analyzer.py` — fact-checks claims, marks as verified/unverified/disputed
- [x] Implement Writer agent (summary composition)
  - `src/agents/writer.py` — composes final summary, prioritizes verified claims
- [x] Ensure all agents emit valid reasoning logs
  - Each agent builds a structured `AgentLog` dict with input, reasoning, output, confidence
  - JSON fallback handling if LLM returns malformed response
- [ ] Test agents independently with sample inputs
  - Needs real OpenAI API key in `.env` to run

### Week 3 (Feb 27–Mar 5) — Explainer Agent

- [x] Design the log aggregation pipeline
  - Sequential: all agent logs collected via `operator.add` reducer in `GraphState`
- [x] Implement Explainer agent (collects + synthesizes logs)
  - `src/agents/explainer.py` — formats all logs, calls LLM to synthesize narrative
  - Includes `_compute_average_confidence()` fallback
- [x] Define decision trace output format (narrative + JSON)
  - Outputs: `decision_trace` (narrative string), `decision_trace_json` (structured dict), `overall_confidence` (float)
- [ ] Test Explainer with mock agent logs
  - Needs real OpenAI API key in `.env` to test live
- [x] Document in `docs/explainers/explainer_agent.md`
  - Already documented (pre-existing)

### Week 4 (Mar 6–12) — Full Pipeline Integration

- [x] Wire all agents into LangGraph workflow
  - `src/graph.py` — `StateGraph` with sequential edges: START → orchestrator → researcher → analyzer → writer → explainer → END
  - `src/state.py` — `GraphState(TypedDict)` with `Annotated[list, operator.add]` reducer for `agent_logs`
- [ ] End-to-end test: user task → output + decision trace
  - `src/main.py` — CLI entry point ready (`python -m src.main --task "..."`) — needs API key
- [x] Handle edge cases (agent failures, low confidence, conflicts)
  - Every agent has JSON parse fallback with degraded but functional output
  - Default confidence scores when parsing fails
- [x] Document architecture in `docs/explainers/langgraph_architecture.md`
  - Already documented (pre-existing)
- [ ] **Milestone: Working prototype demo** — code complete, needs API key for live demo

### Week 5 (Mar 13–19) — Baseline Implementation

- [x] Implement single-agent baseline (one prompt, same task)
  - `src/agents/baseline.py` — single LLM call for summarization + fact-checking + self-explanation
  - Captures token usage and latency for metrics comparison
- [x] Set up metrics collection (accuracy, token usage, latency)
  - `src/metrics.py` — `MetricsResult` dataclass, API cost estimation, comparison tables, JSON export
  - Includes pricing for gpt-3.5-turbo, gpt-4, gpt-4-turbo, gpt-4o, gpt-4o-mini
- [ ] Run both approaches on 10+ sample tasks
  - `src/experiment_runner.py` ready — needs API key to run: `python -m src.experiment_runner`
- [x] Document in `docs/explainers/baseline_vs_proposed.md`
  - Already documented (pre-existing)

### Week 6 (Mar 20–26) — Experimental Runs

- [x] Define benchmark dataset (curated articles/claims for fact-checking)
  - `src/benchmark_tasks.py` — 12 tasks across 3 difficulty levels (easy/medium/hard), 4 domains
  - Each task has expected verification statuses for evaluation against ground truth
  - 18 tests validating dataset structure — all passing
- [ ] Run full experiment: baseline vs. proposed on all benchmark tasks
  - `src/experiment_runner.py` ready — `python -m src.experiment_runner` (needs API key)
  - Supports `--difficulty easy` and `--task-id easy_01` filtering
- [x] Collect metrics: output quality, token cost, latency
  - Automated via `src/metrics.py` — `compare_results()` generates comparison tables
- [x] Log all results for analysis
  - Auto-saves to `results/experiment_YYYYMMDD_HHMMSS.json`
  - `results/` added to `.gitignore`
- [x] Document methodology in `docs/implementation/evaluation_methodology.md`
  - Already documented (pre-existing)

### Week 7 (Mar 27–Apr 2) — User Study + Analysis

- [x] Design user study survey (comprehensibility, trust, accuracy)
  - `src/user_study.py` — 5 Likert-scale questions, `SurveyResponse` dataclass
  - Generate templates: `python -m src.user_study --generate-survey`
  - Can incorporate real experiment results: `--results-file results/experiment_*.json`
- [ ] Recruit participants (minimum 10–15)
- [ ] Run user study: present explained vs. unexplained outputs
- [x] Collect and analyze responses
  - `analyze_responses()` computes means, differences, and preference counts
  - `python -m src.user_study --analyze results/survey_responses.json`
- [ ] Statistical analysis (t-tests or Wilcoxon for significance)

### Week 8 (Apr 3–9) — Paper Writing

- [ ] Write paper sections: Abstract, Introduction, Related Work
- [ ] Write Methodology, Results, Discussion
- [ ] Create figures: architecture diagram, metrics charts, user study results
- [ ] Compile and review LaTeX paper

### Week 9 (Apr 10–13) — Final Polish

- [ ] Finalize paper, proofread, check citations (10+ required)
- [ ] Prepare final presentation slides
- [ ] Clean up GitHub repo (documentation, code comments)
- [ ] **Final submission**

---

## Key Milestones

| Date   | Milestone                               |
| ------ | --------------------------------------- |
| Feb 19 | Logging schema finalized                |
| Feb 26 | All 4 base agents working               |
| Mar 5  | Explainer agent working                 |
| Mar 12 | **Full pipeline demo** ⭐         |
| Mar 19 | Baseline implemented + first comparison |
| Mar 26 | All experimental runs complete          |
| Apr 2  | User study complete                     |
| Apr 9  | Paper draft complete                    |
| Apr 13 | **Final submission** 🎯           |

---

## Risk Mitigation

| Risk                        | Mitigation                                              |
| --------------------------- | ------------------------------------------------------- |
| OpenAI API costs escalate   | Set token budget limits, use GPT-3.5 for testing        |
| User study recruitment slow | Start recruiting in Week 5, use online survey tools     |
| LangGraph complexity        | Build incrementally, test each node before wiring       |
| Scope creep                 | Stick to 3 agents + 1 explainer, no additional features |
