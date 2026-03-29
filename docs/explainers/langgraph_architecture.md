# LangGraph Architecture

> How the multi-agent workflow is structured using LangGraph.

---

## Why LangGraph

LangGraph (by LangChain) models agent workflows as **directed graphs** where:
- **Nodes** = individual agents or processing steps
- **Edges** = data flow between agents
- **State** = shared context passed through the graph

This maps naturally to our architecture: Orchestrator → Workers → Explainer.

## Graph Structure

```
                    ┌──────────────┐
                    │  START NODE  │
                    │  (User Task) │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ ORCHESTRATOR │
                    │    NODE      │
                    └──┬───┬───┬───┘
                       │   │   │
              ┌────────┘   │   └────────┐
              ▼            ▼            ▼
       ┌────────────┐ ┌──────────┐ ┌─────────┐
       │ RESEARCHER │ │ ANALYZER │ │ WRITER  │
       │    NODE    │ │   NODE   │ │  NODE   │
       └─────┬──────┘ └────┬─────┘ └────┬────┘
             │             │            │
             └─────────────┼────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  EXPLAINER   │
                    │    NODE      │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   END NODE   │
                    │ (Output +    │
                    │  Trace)      │
                    └──────────────┘
```

## State Schema

The shared state object passed through the graph:

```python
from typing import TypedDict, List, Optional

class AgentLog(TypedDict):
    agent_name: str
    task_id: str
    timestamp: str
    input: dict
    reasoning: dict
    output: dict
    confidence: float
    metadata: Optional[dict]

class GraphState(TypedDict):
    user_task: str
    subtasks: List[dict]
    agent_logs: List[AgentLog]
    final_output: str
    decision_trace: str
    overall_confidence: float
```

## Execution Flow

1. **User task** enters the graph
2. **Orchestrator** decomposes it into subtasks, updates state
3. **Worker agents** run (can be parallel or sequential), each appends to `agent_logs`
4. **Explainer** reads all `agent_logs`, generates `decision_trace`
5. **End node** returns `final_output` + `decision_trace` to user

## Open Questions

- [ ] Should worker agents run in parallel or sequentially? (Analyzer needs Researcher output)
- [ ] How to handle conditional edges (e.g., skip Writer if Analyzer flags too many issues)?
- [ ] Should the graph support retry loops for low-confidence outputs?
