# Evaluation Methodology

> How we measure success: metrics, user study design, and statistical analysis.

---

## Automated Metrics

| Metric | Description | How Collected |
|--------|-------------|---------------|
| **Output Quality** | Accuracy of fact-checking, completeness of summary | Human evaluation (1–5 scale) or F1-score on labeled claims |
| **Token Usage** | Total input + output tokens per approach | OpenAI API usage logs |
| **Latency** | End-to-end wall-clock time | Python `time` module |
| **Cost** | USD cost per task | Calculated from token usage × price per token |

## User Study Design

### Participants
- Target: 10–15 participants
- Background: mix of technical and non-technical users

### Protocol
1. Present participants with task outputs from **both** approaches (randomized order)
2. For the multi-agent approach, show the decision trace alongside the output
3. Ask participants to rate on a **5-point Likert scale**:
   - **Comprehensibility**: "I understand how this output was produced"
   - **Accuracy**: "I believe this output is accurate"
   - **Trust**: "I trust this output"
   - **Preference**: "I prefer this output over the other"

### Statistical Analysis
- Paired t-test or Wilcoxon signed-rank test (for non-normal distributions)
- Significance threshold: p < 0.05
- Report effect sizes (Cohen's d)

## Benchmark Tasks

- [ ] Define 10–15 tasks (e.g., fact-check a news article, summarize a research paper)
- [ ] Ensure tasks have verifiable ground truth where possible
- [ ] Balance difficulty across easy, medium, and hard tasks

## Expected Deliverables

1. Comparison table: baseline vs. proposed on all automated metrics
2. Bar charts: user trust and comprehensibility scores
3. Statistical significance results
4. Qualitative feedback summary from participants
