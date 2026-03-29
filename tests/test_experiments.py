"""
Tests for metrics, benchmark tasks, and user study modules.
"""

import pytest
from src.metrics import MetricsResult, compare_results, metrics_from_baseline
from src.benchmark_tasks import (
    get_all_tasks,
    get_tasks_by_difficulty,
    get_task_by_id,
    BENCHMARK_TASKS,
)
from src.user_study import (
    SurveyResponse,
    analyze_responses,
    generate_survey_template,
    LIKERT_QUESTIONS,
)


# ── Metrics Tests ────────────────────────────────────────────────

class TestMetricsResult:

    def test_creates_with_defaults(self):
        m = MetricsResult(approach="baseline")
        assert m.approach == "baseline"
        assert m.total_tokens == 0
        assert m.estimated_cost_usd == 0.0

    def test_compute_cost_gpt35(self):
        m = MetricsResult(
            approach="baseline",
            prompt_tokens=1000,
            completion_tokens=500,
            model="gpt-3.5-turbo",
        )
        cost = m.compute_cost()
        # 1000/1000 * 0.0005 + 500/1000 * 0.0015 = 0.0005 + 0.00075 = 0.00125
        assert cost == pytest.approx(0.00125, abs=0.0001)

    def test_compute_cost_gpt4(self):
        m = MetricsResult(
            approach="proposed",
            prompt_tokens=2000,
            completion_tokens=1000,
            model="gpt-4",
        )
        cost = m.compute_cost()
        # 2000/1000 * 0.03 + 1000/1000 * 0.06 = 0.06 + 0.06 = 0.12
        assert cost == pytest.approx(0.12, abs=0.001)

    def test_to_dict(self):
        m = MetricsResult(approach="baseline", task_id="test_01")
        d = m.to_dict()
        assert d["approach"] == "baseline"
        assert d["task_id"] == "test_01"

    def test_compare_results(self):
        baseline = [MetricsResult(approach="baseline", total_tokens=100, latency_ms=500, confidence=0.8)]
        proposed = [MetricsResult(approach="proposed", total_tokens=400, latency_ms=2000, confidence=0.9)]
        table = compare_results(baseline, proposed)
        assert "Baseline" in table
        assert "Proposed" in table
        assert "Avg Total Tokens" in table

    def test_metrics_from_baseline(self):
        result = {
            "task_id": "test_01",
            "user_task": "Test task",
            "token_usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
            "latency_ms": 1200,
            "model": "gpt-3.5-turbo",
            "confidence": 0.85,
            "summary": "Test summary",
            "self_explanation": "Test explanation",
        }
        m = metrics_from_baseline(result)
        assert m.approach == "baseline"
        assert m.total_tokens == 150
        assert m.confidence == 0.85


# ── Benchmark Tasks Tests ────────────────────────────────────────

class TestBenchmarkTasks:

    def test_has_12_tasks(self):
        assert len(BENCHMARK_TASKS) == 12

    def test_all_tasks_have_required_fields(self):
        for task in BENCHMARK_TASKS:
            assert "id" in task
            assert "difficulty" in task
            assert "domain" in task
            assert "task" in task
            assert "expected_claims" in task

    def test_difficulty_distribution(self):
        easy = get_tasks_by_difficulty("easy")
        medium = get_tasks_by_difficulty("medium")
        hard = get_tasks_by_difficulty("hard")
        assert len(easy) == 4
        assert len(medium) == 4
        assert len(hard) == 4

    def test_get_task_by_id(self):
        task = get_task_by_id("easy_01")
        assert task is not None
        assert task["difficulty"] == "easy"
        assert "Eiffel Tower" in task["task"]

    def test_get_task_by_id_not_found(self):
        task = get_task_by_id("nonexistent")
        assert task is None

    def test_all_tasks_returns_all(self):
        assert len(get_all_tasks()) == 12

    def test_expected_claims_have_status(self):
        for task in BENCHMARK_TASKS:
            for claim in task["expected_claims"]:
                assert "claim" in claim
                assert "expected_status" in claim
                assert claim["expected_status"] in ("verified", "unverified", "disputed")


# ── User Study Tests ─────────────────────────────────────────────

class TestUserStudy:

    def test_survey_questions_exist(self):
        assert len(LIKERT_QUESTIONS) >= 4

    def test_generate_survey_template(self):
        template = generate_survey_template()
        assert "USER STUDY" in template
        assert "System A" in template.upper() or "SYSTEM A" in template
        assert "System B" in template.upper() or "SYSTEM B" in template

    def test_survey_response_creation(self):
        r = SurveyResponse(
            participant_id="P001",
            task_id="easy_01",
            baseline_comprehensibility=3,
            baseline_accuracy=4,
            baseline_trust=3,
            proposed_comprehensibility=5,
            proposed_accuracy=4,
            proposed_trust=5,
            proposed_explanation_clarity=5,
            preferred_approach="proposed",
        )
        assert r.participant_id == "P001"
        assert r.preferred_approach == "proposed"

    def test_analyze_responses(self):
        responses = [
            SurveyResponse(
                participant_id="P001", task_id="t1",
                baseline_comprehensibility=2, baseline_accuracy=3, baseline_trust=2,
                proposed_comprehensibility=4, proposed_accuracy=4, proposed_trust=5,
                proposed_explanation_clarity=5, preferred_approach="proposed",
            ),
            SurveyResponse(
                participant_id="P002", task_id="t1",
                baseline_comprehensibility=3, baseline_accuracy=3, baseline_trust=3,
                proposed_comprehensibility=5, proposed_accuracy=5, proposed_trust=4,
                proposed_explanation_clarity=4, preferred_approach="proposed",
            ),
        ]
        analysis = analyze_responses(responses)
        assert analysis["num_participants"] == 2
        assert analysis["differences"]["trust_diff"] > 0  # Proposed should be higher
        assert analysis["preference"]["proposed"] == 2

    def test_analyze_empty_responses(self):
        analysis = analyze_responses([])
        assert "error" in analysis
