# Mid-Term Presentation: Talking Points

Use these talking points alongside the HTML slides. Just read or loosely follow these notes for each slide to sound confident and prepared.

---

### Slide 1: Title Slide (Explainable Multi-Agent AI)
**What to say:**
"Hi everyone, my name is Lymah and today I’m presenting my mid-term progress for my graduate research project: Explainable Multi-Agent AI. The goal of my project is to generate human-readable decision traces in collaborative agent systems so we can actually understand how AI reaches a decision."

---

### Slide 2: The Problem (The Explainability Gap)
**What to say:**
"Let’s start with the problem. When you use a single AI, like ChatGPT, you can just ask it to explain itself. But the future of AI is *multi-agent* systems—specialized AI agents working together. 
The problem is that in these systems, reasoning is distributed. There’s no single point of accountability, making it very hard to know *who did what and why*. In high-stakes fields like healthcare or finance, you can’t deploy an AI system if you can’t explain its decisions."

---

### Slide 3: Project Objectives
**What to say:**
"To address this gap, I set out with five main objectives for this research: First, design a strict logging schema to capture AI reasoning at every step. Second, build a collaborative multi-agent system that utilizes this schema. Third, develop a novel 'Explainer' agent to aggregate these logs. Fourth, evaluate the quality of these explanations through a user study. And fifth, benchmark this multi-agent trace against a traditional single-agent baseline to see if it actually improves user trust."

---

### Slide 4: The Solution (Explanation Aggregation)
**What to say:**
"My solution is an explanation aggregation framework built with LangGraph. I built a pipeline of 5 specialized agents. 
The Orchestrator delegates tasks, the Researcher pulls facts, the Analyzer fact-checks them, and the Writer drafts a final summary based *only* on the verified claims. 
But my core research contribution is the 5th agent: **The Explainer**. It doesn't do the task itself; instead, it watches the other 4 agents and synthesizes all their decision logs into one human-readable trace."

---

### Slide 4: System Architecture
**What to say:**
"Here is the architecture. It's a sequential graph. The really important part here is that *every* agent is forced by a strict Pydantic database schema to output an `AgentLog`. That log guarantees I capture their inputs, reasoning, outputs, and confidence scores live as they work."

---

### Slide 5: Current State
**What to say:**
"So, where am I at for the mid-term? I have successfully completed Phase 1 and hit my Working Prototype milestone. 
I have fully built the shared state management, all 5 of the agents are written in Python, the pipeline is fully connected, and the strict logging schemas are working perfectly."

---

### Slide 6: Rigorous Engineering & Testing
**What to say:**
"Because this is a research project, reproducibility is critical. I took a heavily test-driven approach. Before I even ran a single live OpenAI API call and spent credits, I wrote a massive test suite. 
Right now, I have 39 automated unit tests and 100% of them are passing with zero warnings. I’ve also built-in graceful failure handling so if an LLM hallucinates bad JSON format, my pipeline won't crash."

---

### Slide 7: Experiment Infrastructure (Ahead of Schedule)
**What to say:**
"I am actually ahead of schedule on my 60-day plan. I've already built the entire experiment infrastructure for the second half of the semester. 
I've programmed the single-agent baseline for comparison, I built an automated metrics engine to track token costs and latency, and I’ve already curated my benchmark dataset of 12 fact-checking tasks across different difficulties."

---

### Slide 8: Next Steps (2nd Half)
**What to say:**
"With the code infrastructure 100% complete, the second half of the semester is purely data collection and analysis. 
My next steps are to plug in my API key and run the full pipeline on my dataset. 
Then, I'll take those outputs and run a user study with 10 to 15 participants to definitively measure if my Explainer Agent actually increases *human trust and comprehensibility* compared to a basic AI output."

---

### Slide 9: Q&A
**What to say:**
"And that will culminate in my final IEEE-formatted paper. Thank you all for listening. Does anyone have any questions regarding my architecture or the baseline vs. proposed experiment structure?"
