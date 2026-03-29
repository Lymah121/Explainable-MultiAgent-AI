# Explainable Multi-Agent AI

> **Generating Human-Readable Decision Traces in Collaborative Agent Systems**

A Master's research project (COSC 6375) exploring how to make multi-agent AI systems transparent by generating clear, human-readable explanations of collaborative decisions.

---

## 🎯 Problem

When multiple AI agents collaborate on a task, understanding **why** a particular decision was made becomes challenging. The reasoning is distributed across agents with no single point of accountability. This project addresses the **explainability gap** in multi-agent AI systems.

## 💡 Solution

We propose an **Explanation Aggregation Framework** where:
1. Each agent logs its reasoning using a structured schema (input, output, confidence, justification)
2. A dedicated **Explainer Agent** collects all reasoning logs
3. The Explainer synthesizes them into one **human-readable decision trace**

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────┐
│                    USER SUBMITS TASK                 │
│              "Summarize and fact-check               │
│               this research article"                 │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                 ORCHESTRATOR AGENT                   │
│         Decomposes task into subtasks                │
│         Assigns to specialized agents                │
│         Logs: task breakdown + assignments           │
└──────┬──────────────┬──────────────┬────────────────┘
       │              │              │
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ RESEARCHER  │ │  ANALYZER   │ │   WRITER    │
│   AGENT     │ │   AGENT     │ │   AGENT     │
│             │ │             │ │             │
│ Reads the   │ │ Fact-checks │ │ Writes the  │
│ article and │ │ key claims  │ │ final       │
│ extracts    │ │ against     │ │ summary     │
│ key points  │ │ sources     │ │             │
│             │ │             │ │             │
│ Logs:       │ │ Logs:       │ │ Logs:       │
│ • Input     │ │ • Input     │ │ • Input     │
│ • Reasoning │ │ • Reasoning │ │ • Reasoning │
│ • Output    │ │ • Output    │ │ • Output    │
│ • Confidence│ │ • Confidence│ │ • Confidence│
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │              │              │
       └──────────────┼──────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│               EXPLAINER AGENT                       │
│                                                     │
│  Collects all agent logs and generates:             │
│                                                     │
│  "The Researcher Agent extracted 5 key points       │
│   from the article (confidence: 92%). The Analyzer  │
│   Agent verified 4 of 5 claims against external     │
│   sources (1 claim could not be verified). The      │
│   Writer Agent composed the summary, prioritizing   │
│   the 4 verified claims. Final confidence: 88%."   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                  USER RECEIVES                      │
│                                                     │
│  1. Final Output (the summary)                      │
│  2. Decision Trace (who did what and why)           │
│  3. Confidence Score (overall reliability)          │
└─────────────────────────────────────────────────────┘
```

| Component | Role |
|-----------|------|
| **Orchestrator** | Splits the task and assigns to worker agents |
| **Researcher Agent** | Extracts key information from input |
| **Analyzer Agent** | Fact-checks and validates claims |
| **Writer Agent** | Composes the final output |
| **Explainer Agent** | Aggregates all agent logs into a decision trace |

## 🔬 Research Question

> Can we generate coherent, human-readable explanations for decisions made by collaborating AI agents, and do such explanations improve user trust compared to unexplained multi-agent outputs?

## 📋 Objectives

1. **Design an Explanation Logging Schema** — Structured format for each agent to record input, reasoning, output, and confidence
2. **Build a Multi-Agent System with Explanation Tracking** — 3 specialized LLM-based agents that log their reasoning as they collaborate
3. **Develop an Explainer Agent** — Aggregates reasoning logs into a single coherent decision trace
4. **Evaluate Explanation Quality** — User study measuring comprehensibility, accuracy, and trust
5. **Compare Single-Agent vs Multi-Agent Explainability** — Benchmark explanation clarity between a single-agent approach and the multi-agent aggregated approach

## 🗺 Roadmap

- [ ] **Phase 1: Foundation** — Logging schema + base agents (Orchestrator, Researcher, Analyzer, Writer)
- [ ] **Phase 2: Core Contribution** — Explainer Agent + aggregation pipeline
- [ ] **Phase 3: Experimental Design** — Baseline (single-agent) vs. Proposed (multi-agent + explainer)
- [ ] **Phase 4: Evaluation** — Metrics (Accuracy, F1, Token Usage) + user study
- [ ] **Phase 5: Deliverables** — IEEE Access paper + final presentation

## 📁 Project Structure

```
Agentic AI/
├── README.md
├── .gitignore
├── docs/
│   ├── archive/
│   │   └── proposal.md               # Original proposal (markdown)
│   ├── proposal.pdf                   # Submitted project proposal
│   ├── rubrics_and_guidelines.pdf     # Grading rubrics
│   ├── planning/
│   │   └── 60_day_plan.md             # Week-by-week project timeline
│   ├── explainers/                    # Conceptual deep-dives
│   │   ├── systematic_review.md       # Literature review + paper gradings
│   │   ├── logging_schema.md          # How agents log reasoning
│   │   ├── explainer_agent.md         # How the Explainer works
│   │   ├── langgraph_architecture.md  # LangGraph workflow design
│   │   └── baseline_vs_proposed.md    # Experimental comparison design
│   ├── implementation/                # Technical build docs
│   │   ├── setup_guide.md             # Environment + API setup
│   │   ├── agent_specifications.md    # I/O contracts per agent
│   │   └── evaluation_methodology.md  # Metrics + user study protocol
│   └── tutorials/
│       └── resources.md               # Curated learning resources + suggested path
├── deliverables/                      # Final outputs (gitignored)
│   ├── paper/                         # IEEE Access LaTeX paper
│   └── presentations/                 # Slide decks and posters
└── references/                        # Research papers (gitignored)
    ├── pdfs/                          # Original PDF papers (11)
    └── extracted_text/                # Text extractions (11)
```

## ⚙️ Tech Stack

| Tool | Choice |
|------|--------|
| **Language** | Python 3.10+ |
| **Agentic Framework** | LangGraph |
| **LLM API** | OpenAI (GPT-4) |
| **Reporting** | LaTeX (IEEE Access template) |

## 📚 Key References

1. **Sapkota, R., Roumeliotis, K.I., & Karkee, M. (2026).** "AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications and Challenges." *Information Fusion, 126*, 103599.
2. **Abou Ali, M., Dornaika, F., & Charafeddine, J. (2025).** "Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions." *Artificial Intelligence Review, 59*(11).
3. **OpenAI (2023).** "Practices for Governing Agentic AI Systems."
4. **Baron, S. (2025).** "Trust, Explainability and AI." *Philosophy & Technology, 38*(1).
5. **Papagni, G., et al. (2023).** "Artificial Agents' Explainability to Support Trust: Considerations on Timing and Context." *AI & Society, 38*(2), 947–960.

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/Lymah121/Explainable-MultiAgent-AI.git
cd Explainable-MultiAgent-AI

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (coming soon)
pip install -r requirements.txt
```

## 📄 License

This project is part of a Master's research thesis (COSC 6375 — Spring '26).

---

**Author:** [Lymah121](https://github.com/Lymah121)
