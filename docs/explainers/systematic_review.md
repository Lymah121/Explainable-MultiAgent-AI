# Systematic Review & Project Notes: Explainable Multi-Agent AI

## 1. Project Evaluation: "Explainable Multi-Agent AI"
**Grade: A- (Strong Conceptual Foundation)**
*   **Architecture:** The Supervisor/Hierarchical model (Orchestrator → Workers → Explainer Agent) is technically sound and aligns with modern "Agentic AI" definitions.
*   **Gap:** Need for quantified metrics regarding "Trust" and "Human-Readability."
*   **Recommendation:** Implement **Contrastive Explanations** (answering "Why A instead of B") to satisfy human cognitive biases identified in literature.

---

## 2. Grading of Initial Reference Papers

| Paper | Focus | Project Relevance | Grade |
| :--- | :--- | :--- | :--- |
| Sapkota et al. (2026) | Taxonomy | High (Definitions) | 10/10 |
| Abou Ali et al. (2025) | Architecture | High (Neural Lineage) | 10/10 |
| Anjomshoae et al. (2019) | XAI Mechanics | High (Explanation Phases) | 9/10 |
| Bandi et al. (2025) | Frameworks | High (Metrics/Case Studies) | 9/10 |
| Acharya et al. (2025) | Foundational | Medium (General Survey) | 8/10 |
| Hughes et al. (2025) | Societal | Medium (Trust/Legal) | 8/10 |
| Kostopoulos et al. (2025) | Domain | Low (Education Focus) | 7/10 |
| Dorri et al. (2018) | Classical MAS | Low (Pre-LLM context) | 6/10 |

---

## 3. Systematic Review of "Better" Targeted Papers

This section reviews the state-of-the-art literature specifically for implementing reasoning traces and multi-agent coordination.

### A. Wang et al. (2024) - "A Survey on LLM-based Autonomous Agents"
*   **Contribution:** Defines the "brain" architecture of agents.
*   **Key Concept:** Categorizes **Planning** (Chain-of-Thought, Tree-of-Thought) and **Memory** (Short-term/Long-term) mechanisms.
*   **Application:** Use this to define the internal data structures for your "Researcher" and "Analyst" agents.

### B. Yao et al. (2023) - "ReAct: Synergizing Reasoning and Acting in Language Models"
*   **Contribution:** The industry standard for reasoning traces.
*   **Key Concept:** The **Thought-Action-Observation** loop.
*   **Application:** This is the specific format your agents should use to "record their own steps" as outlined in your first objective.

### C. Heuillet et al. (2021) - "Explainable Multi-Agent Systems: A Survey"
*   **Contribution:** Bridges the gap between XAI and MAS.
*   **Key Concept:** **Collective Explainability.** How a group of agents justifies a singular global outcome.
*   **Application:** Foundational for your "Explainer Agent" whose job is to aggregate individual logs into a cohesive story.

### D. Du et al. (2024) - "Improving Factuality through Multiagent Debate"
*   **Contribution:** Logic for reconciling agent contradictions.
*   **Key Concept:** **Multiagent Debate.**
*   **Application:** Provides the "reconciliation" algorithm for your Explainer Agent when different workers (e.g., Researcher vs. Analyst) disagree.

### E. Hoffman et al. (2023) - "Metrics for Explainable AI"
*   **Contribution:** Psychological validation of XAI.
*   **Key Concept:** **Mental Model Alignment.**
*   **Application:** Provides the testing methodology for your third objective: "Check if these actually help people to trust AI."

---

## 4. Implementation Roadmap
1.  **Trace Generation:** Implement the **ReAct** loop (Yao et al., 2023) for all worker agents.
2.  **Aggregation Logic:** Use **Collective Explainability** principles (Heuillet et al., 2021) to design the Explainer Agent's synthesis function.
3.  **Conflict Resolution:** Apply the **Multiagent Debate** framework (Du et al., 2024) if worker agents provide conflicting reasoning.
4.  **Trust Validation:** Run **Mental Model Alignment** tests (Hoffman et al., 2023) with human participants to grade the "Readability."
