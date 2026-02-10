# Explainable Multi-Agent AI

> **Generating Human-Readable Decision Traces in Collaborative Agent Systems**

A research project exploring how to make multi-agent AI systems transparent by generating clear, human-readable explanations of collaborative decisions.

---

## 🎯 Problem

When multiple AI agents collaborate on a task, understanding **why** a particular decision was made becomes challenging. The reasoning is distributed across agents with no single point of accountability. This project addresses the **explainability gap** in multi-agent AI systems.

## 💡 Solution

We propose an **Explanation Aggregation Framework** where:
1. Each agent logs its reasoning as it works
2. A dedicated **Explainer Agent** collects all logs
3. The Explainer synthesizes them into one **human-readable decision trace**

## 🏗 Architecture

```
User Task → Orchestrator → [Researcher | Analyzer | Writer] → Explainer Agent → Output + Explanation
```

| Component | Role |
|-----------|------|
| **Orchestrator** | Splits the task and assigns to worker agents |
| **Researcher Agent** | Extracts key information from input |
| **Analyzer Agent** | Fact-checks and validates claims |
| **Writer Agent** | Composes the final output |
| **Explainer Agent** | Aggregates all agent logs into a decision trace |

## 📁 Project Structure

```
Agentic AI/
├── README.md                          # This file
├── .gitignore
├── Explainable_MultiAgent_Project/
│   ├── project_proposal.md            # Detailed proposal with objectives and citations
│   └── Agentic AI.pdf                 # Submitted project proposal
└── Reference_paper/                   # Reference papers (gitignored)
    ├── *.pdf                          # Original PDFs
    └── *.txt                          # Extracted text for analysis
```

## 🔬 Research Question

> Can we generate coherent, human-readable explanations for decisions made by collaborating AI agents, and do such explanations improve user trust compared to unexplained multi-agent outputs?

## 📋 Objectives

- Design a structured logging format for each agent's reasoning
- Build a 3-agent prototype with explanation tracking
- Develop an Explainer Agent that aggregates reasoning into clear summaries
- Evaluate explanation quality through a user study

## 📚 Key References

1. Miller, T. (2019). "Explanation in artificial intelligence: Insights from the social sciences." *Artificial Intelligence*
2. Das, S. K., et al. (2021). "Explainable Multi-Agent Systems: A Survey"
3. Anjomshoae, S., et al. (2019). "Explainable Agents and Robots: A Survey of Strategies and Human-Agent Interaction"
4. Chan, A., et al. (2023). "Governance of Agentic AI Systems"
5. Bandi, A., et al. (2025). "The Rise of Agentic AI: A Review of Definitions, Frameworks, Architectures, Applications, Evaluation Metrics, and Challenges"

## ⚙️ Tech Stack

- **Language:** Python
- **LLM API:** OpenAI / Gemini
- **Framework:** LangChain or CrewAI (TBD)

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

This project is part of a Master's research thesis.

---

**Author:** [Lymah121](https://github.com/Lymah121)
