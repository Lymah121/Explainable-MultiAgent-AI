# 📂 Project Index

> Quick reference for what each folder contains and where to find things.  
> *This file is for personal reference — not part of the public repo.*

---

## Root

| File | Purpose |
|------|---------|
| `README.md` | Public-facing project overview, architecture, roadmap |
| `.gitignore` | Git exclusion rules (references, deliverables, LaTeX, env) |

---

## `docs/` — All Project Documentation

Everything you write *about* the project lives here.

| Subfolder | What's Inside | When to Use |
|-----------|---------------|-------------|
| `archive/` | `proposal.md` — original markdown proposal | Reference only, don't edit |
| `planning/` | `60_day_plan.md` — week-by-week timeline | Check off tasks weekly, adjust dates as needed |
| `explainers/` | Conceptual deep-dives on how things work | Read before building each component |
| `implementation/` | Technical specs, setup, evaluation | Reference during coding and experiments |
| `tutorials/` | `resources.md` — curated videos, courses, docs | **Start here** — follow the suggested learning path |

### `docs/explainers/` — Read These First

| File | Covers |
|------|--------|
| `systematic_review.md` | Literature review, paper gradings, 5 targeted papers (ReAct, Multiagent Debate, etc.) |
| `logging_schema.md` | The JSON schema agents use to log reasoning |
| `explainer_agent.md` | How the Explainer Agent aggregates logs into decision traces |
| `langgraph_architecture.md` | Graph structure, state schema, execution flow |
| `baseline_vs_proposed.md` | Single-agent vs. multi-agent experimental design |

### `docs/implementation/` — Reference During Build

| File | Covers |
|------|--------|
| `setup_guide.md` | Python environment, API keys, running the project |
| `agent_specifications.md` | I/O contracts for all 5 agents |
| `evaluation_methodology.md` | Metrics, user study protocol, statistical analysis |

---

## `deliverables/` — Final Outputs *(gitignored)*

What you submit for grading.

| Subfolder | What Goes Here |
|-----------|----------------|
| `paper/` | IEEE Access LaTeX paper (template already here) |
| `presentations/` | Final presentation slides, posters |

---

## `references/` — Research Papers *(gitignored)*

Source material you're reading and citing.

| Subfolder | What's Inside |
|-----------|---------------|
| `pdfs/` | 11 original PDF papers |
| `extracted_text/` | 11 text extractions (named to match source papers) |

---

## Rubric Quick Reference

| Category | Weight | Where It Lives |
|----------|--------|----------------|
| Literature Review (15%) | `references/`, `docs/explainers/systematic_review.md` |
| Implementation (30%) | `src/` *(coming soon)* |
| Experimental Design (20%) | `docs/explainers/baseline_vs_proposed.md` |
| Outcome Analysis (15%) | `docs/implementation/evaluation_methodology.md` |
| arXiv Report (20%) | `deliverables/paper/` |
