"""
Experiment Runner — Run baseline vs. proposed on all benchmark tasks.

Runs both approaches on the full benchmark dataset, collects metrics,
generates comparison tables, and saves all results to JSON.

Usage:
    python -m src.experiment_runner
    python -m src.experiment_runner --difficulty easy
    python -m src.experiment_runner --task-id easy_01
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

from src.benchmark_tasks import get_all_tasks, get_tasks_by_difficulty, get_task_by_id
from src.agents.baseline import run_baseline
from src.graph import app
from src.metrics import (
    MetricsResult,
    metrics_from_baseline,
    metrics_from_proposed,
    compare_results,
    save_results,
)


# Results directory
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")


def run_experiment_baseline(task: dict) -> tuple[dict, MetricsResult]:
    """Run a single benchmark task through the baseline approach."""
    print(f"  [BASELINE] Running task {task['id']}...")
    result = run_baseline(task["task"])
    metrics = metrics_from_baseline(result)
    metrics.task_id = task["id"]
    metrics.task_text = task["task"]
    return result, metrics


def run_experiment_proposed(task: dict) -> tuple[dict, MetricsResult]:
    """Run a single benchmark task through the multi-agent pipeline."""
    import uuid

    print(f"  [PROPOSED] Running task {task['id']}...")
    task_id = str(uuid.uuid4())

    initial_state = {
        "user_task": task["task"],
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

    start_time = time.time()
    result = app.invoke(initial_state)
    total_latency = int((time.time() - start_time) * 1000)

    metrics = metrics_from_proposed(result)
    metrics.task_id = task["id"]
    metrics.task_text = task["task"]
    metrics.latency_ms = total_latency  # Override with wall-clock time
    return result, metrics


def run_full_experiment(tasks: list[dict]) -> dict:
    """Run the full experiment on a list of benchmark tasks.

    Returns:
        Dict with baseline_metrics, proposed_metrics, baseline_results,
        proposed_results, and comparison_table.
    """
    baseline_metrics = []
    proposed_metrics = []
    baseline_results = []
    proposed_results = []

    print(f"\n{'='*60}")
    print(f"  EXPERIMENT: Baseline vs. Proposed")
    print(f"  Tasks: {len(tasks)}")
    print(f"  Started: {datetime.now(timezone.utc).isoformat()}")
    print(f"{'='*60}\n")

    for i, task in enumerate(tasks, 1):
        print(f"\n--- Task {i}/{len(tasks)}: {task['id']} ({task['difficulty']}) ---")

        # Run baseline
        b_result, b_metrics = run_experiment_baseline(task)
        baseline_results.append(b_result)
        baseline_metrics.append(b_metrics)

        # Small delay between API calls
        time.sleep(1)

        # Run proposed
        p_result, p_metrics = run_experiment_proposed(task)
        proposed_results.append(p_result)
        proposed_metrics.append(p_metrics)

        print(f"  Baseline: {b_metrics.total_tokens} tokens, {b_metrics.latency_ms}ms, conf={b_metrics.confidence:.0%}")
        print(f"  Proposed: {p_metrics.total_tokens} tokens, {p_metrics.latency_ms}ms, conf={p_metrics.confidence:.0%}")

        # Small delay between tasks
        time.sleep(1)

    # Generate comparison
    comparison = compare_results(baseline_metrics, proposed_metrics)
    print(comparison)

    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = os.path.join(RESULTS_DIR, f"experiment_{timestamp}.json")
    save_results(baseline_metrics, proposed_metrics, results_path)
    print(f"\nResults saved to: {results_path}")

    return {
        "baseline_metrics": baseline_metrics,
        "proposed_metrics": proposed_metrics,
        "baseline_results": baseline_results,
        "proposed_results": proposed_results,
        "comparison_table": comparison,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run baseline vs. proposed experiments on benchmark tasks"
    )
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        help="Run only tasks of this difficulty",
    )
    parser.add_argument(
        "--task-id",
        type=str,
        help="Run only a specific task by ID (e.g., easy_01)",
    )
    args = parser.parse_args()

    if args.task_id:
        task = get_task_by_id(args.task_id)
        if not task:
            print(f"Task '{args.task_id}' not found.")
            sys.exit(1)
        tasks = [task]
    elif args.difficulty:
        tasks = get_tasks_by_difficulty(args.difficulty)
    else:
        tasks = get_all_tasks()

    if not tasks:
        print("No tasks found matching criteria.")
        sys.exit(1)

    run_full_experiment(tasks)


if __name__ == "__main__":
    main()
