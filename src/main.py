"""
Main Entry Point — Run the Explainable Multi-Agent AI pipeline.

Usage:
    python -m src.main --task "Summarize and fact-check this article: ..."
    python -m src.main   (interactive mode — prompts for task input)
"""

import argparse
import json
import uuid
import sys

from src.graph import app


def run_pipeline(user_task: str) -> dict:
    """Run the full multi-agent pipeline on a user task.

    Args:
        user_task: The task to process (e.g. a statement to fact-check and summarize).

    Returns:
        The final GraphState with all outputs and the decision trace.
    """
    task_id = str(uuid.uuid4())

    initial_state = {
        "user_task": user_task,
        "task_id": task_id,
        "subtasks": [],
        "research_output": "",
        "analysis_output": "",
        "final_output": "",
        "agent_logs": [],
        "decision_trace": "",
        "decision_trace_json": {},
        "overall_confidence": 0.0,
    }

    print(f"\n{'='*60}")
    print(f"  EXPLAINABLE MULTI-AGENT AI PIPELINE")
    print(f"{'='*60}")
    print(f"Task ID: {task_id}")
    print(f"Task: {user_task}")
    print(f"{'='*60}\n")

    # Stream events so user sees progress
    print("▶ Running Orchestrator...")
    print("▶ Running Researcher...")
    print("▶ Running Analyzer...")
    print("▶ Running Writer...")
    print("▶ Running Explainer...")
    print()

    # Run the full graph
    result = app.invoke(initial_state)

    # Display results
    _print_results(result)

    return result


def _print_results(result: dict) -> None:
    """Pretty-print the pipeline results."""

    print(f"\n{'='*60}")
    print("  FINAL OUTPUT")
    print(f"{'='*60}\n")
    print(result.get("final_output", "No output generated."))

    print(f"\n{'='*60}")
    print("  DECISION TRACE (Human-Readable)")
    print(f"{'='*60}\n")
    print(result.get("decision_trace", "No decision trace generated."))

    print(f"\n{'='*60}")
    print("  CONFIDENCE SCORE")
    print(f"{'='*60}\n")
    confidence = result.get("overall_confidence", 0.0)
    print(f"Overall Confidence: {confidence:.0%}")

    print(f"\n{'='*60}")
    print("  AGENT LOGS SUMMARY")
    print(f"{'='*60}\n")
    for log in result.get("agent_logs", []):
        agent = log.get("agent_name", "unknown")
        conf = log.get("confidence", 0.0)
        output_desc = log.get("output", {}).get("description", "N/A")
        print(f"  [{agent.upper():>12}]  confidence={conf:.0%}  |  {output_desc}")

    # Optionally dump full JSON trace
    trace_json = result.get("decision_trace_json", {})
    if trace_json:
        print(f"\n{'='*60}")
        print("  STRUCTURED DECISION TRACE (JSON)")
        print(f"{'='*60}\n")
        print(json.dumps(trace_json, indent=2))

    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Run the Explainable Multi-Agent AI pipeline"
    )
    parser.add_argument(
        "--task",
        type=str,
        help="The task to process (e.g. a statement to fact-check and summarize)",
    )
    args = parser.parse_args()

    if args.task:
        user_task = args.task
    else:
        # Interactive mode
        print("\n🤖 Explainable Multi-Agent AI")
        print("Enter a task to fact-check and summarize.\n")
        user_task = input("Your task: ").strip()
        if not user_task:
            print("No task provided. Exiting.")
            sys.exit(1)

    run_pipeline(user_task)


if __name__ == "__main__":
    main()
