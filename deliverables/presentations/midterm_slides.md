---
marp: true
theme: default
paginate: true
header: "Explainable Multi-Agent AI"
footer: "COSC 6375 Mid-Term Evaluation"
---

# Explainable Multi-Agent AI
## Generating Human-Readable Decision Traces in Collaborative Agent Systems

**Student:** Lymah121
**Course:** COSC 6375 — Graduate Research in Agentic AI and Federated Learning
**Phase:** Mid-Term Evaluation (Week 4/9)

---

## 🎯 The Problem: The Explainability Gap

- **Single AI Agents:** Easy to prompt for an explanation.
- **Multi-Agent Systems:** Reasoning is **distributed** across specialized agents.
- **The Result:** No single point of accountability. It's difficult to understand *who did what* and *why*.
- **Why it matters:** In high-stakes domains (healthcare, finance), users cannot trust AI outputs without seeing the decision-making process.

---

## 📋 Project Objectives

1. **Design an Explanation Logging Schema:** Structured format to record input, reasoning, output, and confidence.
2. **Build a Multi-Agent System:** Specialized LLM-based agents that log their reasoning.
3. **Develop an Explainer Agent:** Aggregates reasoning logs into a coherent decision trace.
4. **Evaluate Explanation Quality:** Conduct a user study measuring comprehensibility, accuracy, and trust.
5. **Benchmark Approaches:** Compare explanation clarity between single-agent and multi-agent aggregated approaches.

---

## 💡 The Solution: Explanation Aggregation

A LangGraph-based framework with 5 specialized agents:

1. **Orchestrator:** Breaks tasks into subtasks.
2. **Researcher:** Extracts key facts from sources.
3. **Analyzer:** Fact-checks and verifies claims.
4. **Writer:** Composes the final output prioritizing verified claims.
5. **Explainer (Core Contribution):** Synthesizes logs from all agents into a human-readable decision trace.

---

## 🏗 System Architecture

![Architecture](https://via.placeholder.com/800x400?text=Orchestrator+->+Researcher+->+Analyzer+->+Writer+->+Explainer)

*Each agent must output a strict JSON `AgentLog` (Input, Reasoning, Output, Confidence).*

---

## 🚀 Mid-Term Progress: Current State

**Milestone Reached:** Working Prototype Code Infrastructure (Weeks 1-4 Complete)

✅ **Environment & Config:** `src/config.py`, OpenAI integration.
✅ **Shared State Management:** `src/state.py` (LangGraph `TypedDict` with reducer).
✅ **All 5 Agents Built:** Modular Python implementations in `src/agents/`.
✅ **LangGraph Pipeline Wired:** Sequential flow established in `src/graph.py`.
✅ **Strict Logging Schema:** Pydantic models enforcing explainability.

---

## 🧪 Rigorous Engineering & Testing

I took a heavily test-driven approach to ensure research reproducibility before running live API calls.

- **Unit Tests:** 39 tests written across validation, schemas, and state tracking.
- **Current Status:** **39 / 39 Tests Passing** (0 warnings).
- **Graceful Failures:** Implemented JSON parse fallbacks for all LLM calls.

---

## 📊 Experiment Infrastructure (Weeks 5-6 Built Early)

I am ahead of schedule and have already built the experiment pipeline:

1. **Baseline Agent:** Single-prompt agent built for comparison.
2. **Metrics Engine:** Built `src/metrics.py` to track token cost, latency, and confidence automatically.
3. **Benchmark Dataset:** 12 curated fact-checking tasks (easy/medium/hard) developed in `src/benchmark_tasks.py`.
4. **Experiment Runner:** CLI tool ready to run Baseline vs. Proposed.

---

## 📝 Next Steps (Second Half of Semester)

Now that the core infrastructure is 100% built, the focus shifts to data collection:

1. **API Integration:** Plug in live API keys and run the full pipeline.
2. **Run the Benchmark:** Execute the baseline vs. proposed systems across the 12 tasks to gather performance metrics (cost, latency, quality).
3. **User Study (Weeks 7-8):** Present explained vs. unexplained outputs to 10-15 participants to measure **trust and comprehensibility**.
4. **Final Paper:** Compile findings into the IEEE Access formatted paper.

---

# Thank You!
## Questions?

*Focus: Can we generate coherent explanations for multi-agent systems, and does it improve user trust?*
