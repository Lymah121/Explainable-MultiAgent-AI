"""
User Study — Survey generation and analysis tools.

Generates formatted materials for the user study: side-by-side comparisons
of explained vs. unexplained outputs, Likert-scale survey templates,
and tools for analyzing collected responses.

Usage:
    python -m src.user_study --generate-survey
    python -m src.user_study --analyze results/survey_responses.json
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from typing import Optional


# ── Survey Questions ─────────────────────────────────────────────

LIKERT_QUESTIONS = [
    {
        "id": "comprehensibility",
        "text": "I understand how this output was produced.",
        "scale": "1 (Strongly Disagree) — 5 (Strongly Agree)",
    },
    {
        "id": "accuracy",
        "text": "I believe this output is accurate.",
        "scale": "1 (Strongly Disagree) — 5 (Strongly Agree)",
    },
    {
        "id": "trust",
        "text": "I trust this output.",
        "scale": "1 (Strongly Disagree) — 5 (Strongly Agree)",
    },
    {
        "id": "preference",
        "text": "I prefer this output over the other.",
        "scale": "1 (Strongly Disagree) — 5 (Strongly Agree)",
    },
    {
        "id": "explanation_clarity",
        "text": "The explanation helped me understand the decision-making process.",
        "scale": "1 (Strongly Disagree) — 5 (Strongly Agree)",
        "condition": "proposed_only",  # Only shown for multi-agent outputs
    },
]


@dataclass
class SurveyResponse:
    """A single participant's response for one task comparison."""
    participant_id: str
    task_id: str
    # Baseline ratings
    baseline_comprehensibility: int = 0
    baseline_accuracy: int = 0
    baseline_trust: int = 0
    # Proposed ratings
    proposed_comprehensibility: int = 0
    proposed_accuracy: int = 0
    proposed_trust: int = 0
    proposed_explanation_clarity: int = 0
    # Overall preference
    preferred_approach: str = ""  # "baseline" or "proposed"
    free_text_feedback: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def generate_survey_template(
    experiment_results_path: Optional[str] = None,
) -> str:
    """Generate a formatted survey template for the user study.

    Args:
        experiment_results_path: Optional path to experiment results JSON.
            If provided, includes actual outputs in the survey.

    Returns:
        Formatted survey template as a string.
    """
    survey = []
    survey.append("=" * 65)
    survey.append("  EXPLAINABLE MULTI-AGENT AI — USER STUDY")
    survey.append("=" * 65)
    survey.append("")
    survey.append("Thank you for participating in this research study.")
    survey.append("You will be shown outputs from two AI systems that performed")
    survey.append("the same task. Please rate each output on the following criteria.")
    survey.append("")
    survey.append("Participant ID: _______________")
    survey.append("Date: _______________")
    survey.append("Background: [ ] Technical  [ ] Non-technical")
    survey.append("")

    # Load experiment results if available
    tasks_data = []
    if experiment_results_path and os.path.exists(experiment_results_path):
        with open(experiment_results_path) as f:
            data = json.load(f)
            baseline_data = data.get("baseline", [])
            proposed_data = data.get("proposed", [])
            for b, p in zip(baseline_data, proposed_data):
                tasks_data.append({"baseline": b, "proposed": p})

    # Generate per-task survey sections
    num_tasks = len(tasks_data) if tasks_data else 3  # Default 3 placeholder tasks
    for i in range(num_tasks):
        task_id = tasks_data[i]["baseline"].get("task_id", f"task_{i+1}") if tasks_data else f"task_{i+1}"
        survey.append(f"\n{'─'*65}")
        survey.append(f"  TASK {i+1}: {task_id}")
        survey.append(f"{'─'*65}\n")

        if tasks_data:
            survey.append(f"Task: {tasks_data[i]['baseline'].get('task_text', 'N/A')[:200]}")
            survey.append("")

        # System A (randomized — could be baseline or proposed)
        survey.append("  ┌─────────────────────────────────────────────┐")
        survey.append("  │  SYSTEM A OUTPUT                            │")
        survey.append("  ├─────────────────────────────────────────────┤")
        if tasks_data:
            summary = tasks_data[i]["baseline"].get("summary", "N/A")[:300]
            survey.append(f"  │  {summary}")
        else:
            survey.append("  │  [Output will be inserted here]")
        survey.append("  │")
        survey.append("  │  (No explanation provided)")
        survey.append("  └─────────────────────────────────────────────┘")
        survey.append("")

        # System B
        survey.append("  ┌─────────────────────────────────────────────┐")
        survey.append("  │  SYSTEM B OUTPUT                            │")
        survey.append("  ├─────────────────────────────────────────────┤")
        if tasks_data:
            summary = tasks_data[i]["proposed"].get("summary", "N/A")[:300]
            survey.append(f"  │  {summary}")
            survey.append("  │")
            explanation = tasks_data[i]["proposed"].get("explanation", "N/A")[:400]
            survey.append(f"  │  Decision Trace: {explanation}")
        else:
            survey.append("  │  [Output will be inserted here]")
            survey.append("  │")
            survey.append("  │  Decision Trace: [Explanation will be inserted here]")
        survey.append("  └─────────────────────────────────────────────┘")
        survey.append("")

        # Rating questions
        survey.append("  RATINGS (1=Strongly Disagree, 5=Strongly Agree):")
        survey.append("")
        survey.append("  System A:")
        for q in LIKERT_QUESTIONS:
            if q.get("condition") == "proposed_only":
                continue
            survey.append(f"    {q['text']}")
            survey.append(f"    [ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 5 ]")
            survey.append("")

        survey.append("  System B:")
        for q in LIKERT_QUESTIONS:
            survey.append(f"    {q['text']}")
            survey.append(f"    [ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 5 ]")
            survey.append("")

        survey.append("  Overall preference: [ ] System A   [ ] System B")
        survey.append("  Free-text feedback: ________________________________")

    # Final section
    survey.append(f"\n{'='*65}")
    survey.append("  GENERAL FEEDBACK")
    survey.append(f"{'='*65}\n")
    survey.append("How important is it to you to understand HOW an AI reached its answer?")
    survey.append("[ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 5 ]")
    survey.append("")
    survey.append("Additional comments:")
    survey.append("_______________________________________________________")
    survey.append("_______________________________________________________")
    survey.append("")
    survey.append("Thank you for your participation!")

    return "\n".join(survey)


def analyze_responses(responses: list[SurveyResponse]) -> dict:
    """Analyze collected survey responses.

    Returns:
        Dict with means, comparisons, and statistical summaries.
    """
    if not responses:
        return {"error": "No responses to analyze"}

    n = len(responses)

    # Compute means
    def _mean(values: list[int]) -> float:
        return round(sum(values) / len(values), 2) if values else 0.0

    baseline_comp = [r.baseline_comprehensibility for r in responses]
    baseline_acc = [r.baseline_accuracy for r in responses]
    baseline_trust = [r.baseline_trust for r in responses]

    proposed_comp = [r.proposed_comprehensibility for r in responses]
    proposed_acc = [r.proposed_accuracy for r in responses]
    proposed_trust = [r.proposed_trust for r in responses]
    proposed_expl = [r.proposed_explanation_clarity for r in responses]

    preference_counts = {
        "baseline": sum(1 for r in responses if r.preferred_approach == "baseline"),
        "proposed": sum(1 for r in responses if r.preferred_approach == "proposed"),
        "no_preference": sum(1 for r in responses if r.preferred_approach not in ("baseline", "proposed")),
    }

    return {
        "num_participants": n,
        "baseline": {
            "comprehensibility_mean": _mean(baseline_comp),
            "accuracy_mean": _mean(baseline_acc),
            "trust_mean": _mean(baseline_trust),
        },
        "proposed": {
            "comprehensibility_mean": _mean(proposed_comp),
            "accuracy_mean": _mean(proposed_acc),
            "trust_mean": _mean(proposed_trust),
            "explanation_clarity_mean": _mean(proposed_expl),
        },
        "differences": {
            "comprehensibility_diff": round(_mean(proposed_comp) - _mean(baseline_comp), 2),
            "accuracy_diff": round(_mean(proposed_acc) - _mean(baseline_acc), 2),
            "trust_diff": round(_mean(proposed_trust) - _mean(baseline_trust), 2),
        },
        "preference": preference_counts,
    }


def print_analysis(analysis: dict) -> None:
    """Pretty-print the analysis results."""
    print(f"\n{'='*55}")
    print("  USER STUDY RESULTS")
    print(f"  Participants: {analysis['num_participants']}")
    print(f"{'='*55}\n")

    print(f"{'Metric':<30} {'Baseline':>10} {'Proposed':>10} {'Δ':>8}")
    print("-" * 60)

    b = analysis["baseline"]
    p = analysis["proposed"]
    d = analysis["differences"]

    print(f"{'Comprehensibility':<30} {b['comprehensibility_mean']:>10.2f} {p['comprehensibility_mean']:>10.2f} {d['comprehensibility_diff']:>+8.2f}")
    print(f"{'Accuracy':<30} {b['accuracy_mean']:>10.2f} {p['accuracy_mean']:>10.2f} {d['accuracy_diff']:>+8.2f}")
    print(f"{'Trust':<30} {b['trust_mean']:>10.2f} {p['trust_mean']:>10.2f} {d['trust_diff']:>+8.2f}")
    print(f"{'Explanation Clarity':<30} {'N/A':>10} {p['explanation_clarity_mean']:>10.2f}")

    pref = analysis["preference"]
    print(f"\nPreference: Baseline={pref['baseline']}, Proposed={pref['proposed']}, No pref={pref['no_preference']}")
    print(f"{'='*55}\n")


def main():
    parser = argparse.ArgumentParser(description="User study tools")
    parser.add_argument("--generate-survey", action="store_true", help="Generate survey template")
    parser.add_argument("--results-file", type=str, help="Path to experiment results JSON")
    parser.add_argument("--analyze", type=str, help="Path to survey responses JSON to analyze")
    parser.add_argument("--output", type=str, help="Output file for generated survey")
    args = parser.parse_args()

    if args.generate_survey:
        survey = generate_survey_template(args.results_file)
        if args.output:
            with open(args.output, "w") as f:
                f.write(survey)
            print(f"Survey saved to: {args.output}")
        else:
            print(survey)

    elif args.analyze:
        if not os.path.exists(args.analyze):
            print(f"File not found: {args.analyze}")
            sys.exit(1)
        with open(args.analyze) as f:
            raw = json.load(f)
        responses = [SurveyResponse(**r) for r in raw]
        analysis = analyze_responses(responses)
        print_analysis(analysis)
        # Save analysis
        if args.output:
            with open(args.output, "w") as f:
                json.dump(analysis, f, indent=2)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
