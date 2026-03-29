# Project Proposal

---

## Title

**Explainable Multi-Agent AI: Generating Human-Readable Decision Traces in Collaborative Agent Systems**

---

## Objectives / Goals

1. **Design an Explanation Logging Schema** — Define a structured format for each agent to record its reasoning (input received, decision made, confidence level, and justification) during collaborative tasks.

2. **Build a Multi-Agent System with Explanation Tracking** — Implement a working prototype with 3 specialized LLM-based agents (e.g., Researcher, Analyzer, Writer) that log their individual contributions as they collaborate on a task.

3. **Develop an Explainer Agent** — Create a dedicated agent that collects the reasoning logs from all participating agents and synthesizes them into a single, coherent, human-readable explanation of the final decision.

4. **Evaluate Explanation Quality** — Conduct a user study to assess whether the generated explanations are understandable, accurate, and whether they improve user trust in multi-agent outputs compared to unexplained outputs.

5. **Compare Single-Agent vs Multi-Agent Explainability** — Benchmark explanation clarity and user comprehension between a single-agent approach (one agent explains itself) and the multi-agent aggregated explanation approach.

---

## Expected Outcomes

1. **Explanation Aggregation Framework** — A reusable, lightweight framework that can be plugged into any multi-agent LLM system to generate decision traces, including reasoning logs per agent and an aggregated explanation pipeline.

2. **Working Prototype** — A functional 3-agent system demonstrating collaborative task completion with full explanation tracking, built using Python and an LLM API (e.g., OpenAI or Gemini).

3. **Explanation Quality Metrics** — A set of measurable criteria for evaluating multi-agent explanations, including comprehensibility, accuracy of attribution, and user trust scores.

4. **User Study Results** — Empirical evidence showing how aggregated multi-agent explanations impact user trust and understanding, with statistical analysis comparing explained vs unexplained outputs.

5. **Design Guidelines** — Practical recommendations for making multi-agent AI systems more transparent and auditable, applicable to domains like healthcare, education, and enterprise automation.

---

## Design Workflow

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
│         Logs: task breakdown + assignments            │
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
│               EXPLAINER AGENT                        │
│                                                      │
│  Collects all agent logs and generates:              │
│                                                      │
│  "The Researcher Agent extracted 5 key points        │
│   from the article (confidence: 92%). The Analyzer   │
│   Agent verified 4 of 5 claims against external      │
│   sources (1 claim could not be verified). The       │
│   Writer Agent composed the summary, prioritizing    │
│   the 4 verified claims. Final confidence: 88%."     │
│                                                      │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                  USER RECEIVES                       │
│                                                      │
│  1. Final Output (the summary)                       │
│  2. Decision Trace (who did what and why)            │
│  3. Confidence Score (overall reliability)            │
└─────────────────────────────────────────────────────┘
```

---

## 5 Most Aligned Citations

1. **Sapkota, R., Roumeliotis, K.I., & Karkee, M. (2026).** "AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications and Challenges." *Information Fusion, 126*, 103599.
   — Identifies **explainability deficits** as a key challenge in Agentic AI and calls for "explainability pipelines that integrate across agents (e.g., timeline visualizations or dialogue replays)" to ensure safety in multi-agent systems.

2. **Abou Ali, M., Dornaika, F., & Charafeddine, J. (2025).** "Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions." *Artificial Intelligence Review, 59*(11).
   — Emphasizes that agents must operate "in a manner that is **transparent and auditable** where required" and highlights the governance divide where neural systems lack the explainability of symbolic systems.

3. **OpenAI (2023).** "Practices for Governing Agentic AI Systems."
   — Defines **"Legibility of Agent Activity"** as a core governance practice, arguing that revealing an agent's reasoning to the user "enables them to spot errors, allows for subsequent debugging, and instills trust when deserved."

4. **Baron, S. (2025).** "Trust, Explainability and AI." *Philosophy & Technology, 38*(1).
   — Establishes the theoretical link between **explainability and user trust** in AI systems, providing the conceptual foundation for measuring how explanations affect human confidence in agent decisions.

5. **Papagni, G., de Pagter, J., Zafari, S., Filzmoser, M., & Koeszegi, S.T. (2023).** "Artificial Agents' Explainability to Support Trust: Considerations on Timing and Context." *AI & Society, 38*(2), 947–960.
   — Investigates **when and how** AI agent explanations should be presented to maximize trust, directly informing our design of the Explainer Agent's output format and timing.

---
