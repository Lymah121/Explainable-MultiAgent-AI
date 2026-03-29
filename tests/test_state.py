"""
Unit tests for the GraphState schema.
"""

from src.state import GraphState


class TestGraphState:
    """Tests for GraphState initialization and structure."""

    def test_creates_with_all_fields(self):
        state: GraphState = {
            "user_task": "Summarize this article",
            "subtasks": [],
            "research_output": "",
            "analysis_output": "",
            "final_output": "",
            "agent_logs": [],
            "decision_trace": "",
            "decision_trace_json": {},
            "overall_confidence": 0.0,
        }
        assert state["user_task"] == "Summarize this article"
        assert state["agent_logs"] == []
        assert state["overall_confidence"] == 0.0

    def test_agent_logs_is_list(self):
        state: GraphState = {
            "user_task": "Test",
            "subtasks": [],
            "research_output": "",
            "analysis_output": "",
            "final_output": "",
            "agent_logs": [{"agent_name": "test", "confidence": 0.9}],
            "decision_trace": "",
            "decision_trace_json": {},
            "overall_confidence": 0.0,
        }
        assert len(state["agent_logs"]) == 1
        assert state["agent_logs"][0]["agent_name"] == "test"

    def test_subtasks_is_list_of_dicts(self):
        subtasks = [
            {"agent": "researcher", "instruction": "Extract key points"},
            {"agent": "analyzer", "instruction": "Fact-check claims"},
        ]
        state: GraphState = {
            "user_task": "Test",
            "subtasks": subtasks,
            "research_output": "",
            "analysis_output": "",
            "final_output": "",
            "agent_logs": [],
            "decision_trace": "",
            "decision_trace_json": {},
            "overall_confidence": 0.0,
        }
        assert len(state["subtasks"]) == 2
        assert state["subtasks"][0]["agent"] == "researcher"
