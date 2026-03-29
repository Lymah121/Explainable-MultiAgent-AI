# Agent Specifications

> Input/output contracts and responsibilities for each agent.

---

## Orchestrator Agent

| Property | Value |
|----------|-------|
| **Input** | Raw user task (string) |
| **Output** | List of subtasks with agent assignments |
| **Responsibility** | Decompose the user's task and assign subtasks to worker agents |
| **Logs** | Task breakdown, assignment reasoning |

---

## Researcher Agent

| Property | Value |
|----------|-------|
| **Input** | Source material (article, text) from orchestrator |
| **Output** | List of extracted key points |
| **Responsibility** | Read and extract the most important information from the input |
| **Logs** | What was extracted, why these points were chosen, confidence |

---

## Analyzer Agent

| Property | Value |
|----------|-------|
| **Input** | Key points from Researcher |
| **Output** | Verification results for each claim (verified / unverified / disputed) |
| **Responsibility** | Fact-check and validate the claims extracted by the Researcher |
| **Logs** | Which claims checked, sources used, verification status, confidence |

---

## Writer Agent

| Property | Value |
|----------|-------|
| **Input** | Verified key points from Analyzer |
| **Output** | Final composed summary |
| **Responsibility** | Write a coherent, well-structured output prioritizing verified claims |
| **Logs** | Writing decisions, what was included/excluded, confidence |

---

## Explainer Agent

| Property | Value |
|----------|-------|
| **Input** | All reasoning logs from Orchestrator + Worker agents |
| **Output** | Decision trace (narrative text + structured JSON) |
| **Responsibility** | Aggregate reasoning into a coherent explanation of the collaborative decision |
| **Logs** | N/A (the Explainer's output IS the explanation) |
