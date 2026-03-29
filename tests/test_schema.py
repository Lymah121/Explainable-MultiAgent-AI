"""
Unit tests for the explanation logging schema (Pydantic models).
"""

import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.schemas.logging_schema import (
    AgentLog,
    InputData,
    Reasoning,
    OutputData,
    Metadata,
)


# ── Fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def valid_log_data():
    """Minimal valid data for constructing an AgentLog."""
    return {
        "agent_name": "researcher",
        "task_id": uuid.uuid4(),
        "input": InputData(
            description="Source article text",
            data="The Eiffel Tower was built in 1889.",
        ),
        "reasoning": Reasoning(
            approach="Extracted key facts from the article",
            key_decisions=["Focused on verifiable historical claims"],
        ),
        "output": OutputData(
            description="Extracted 1 key point",
            data="The Eiffel Tower was built in 1889.",
        ),
        "confidence": 0.92,
    }


# ── AgentLog creation tests ──────────────────────────────────────

class TestAgentLogCreation:
    """Tests for valid AgentLog construction."""

    def test_creates_with_required_fields(self, valid_log_data):
        log = AgentLog(**valid_log_data)
        assert log.agent_name == "researcher"
        assert log.confidence == 0.92
        assert log.metadata is None  # Optional, not provided

    def test_creates_with_all_fields(self, valid_log_data):
        valid_log_data["metadata"] = Metadata(
            tokens_used=1250, model="gpt-4", latency_ms=3200
        )
        log = AgentLog(**valid_log_data)
        assert log.metadata.tokens_used == 1250
        assert log.metadata.model == "gpt-4"

    def test_timestamp_auto_generated(self, valid_log_data):
        log = AgentLog(**valid_log_data)
        assert log.timestamp is not None
        assert isinstance(log.timestamp, datetime)

    def test_task_id_is_uuid(self, valid_log_data):
        log = AgentLog(**valid_log_data)
        assert isinstance(log.task_id, uuid.UUID)

    def test_serializes_to_dict(self, valid_log_data):
        log = AgentLog(**valid_log_data)
        data = log.model_dump()
        assert "agent_name" in data
        assert "confidence" in data
        assert "reasoning" in data

    def test_serializes_to_json(self, valid_log_data):
        log = AgentLog(**valid_log_data)
        json_str = log.model_dump_json()
        assert "researcher" in json_str


# ── Validation failure tests ─────────────────────────────────────

class TestAgentLogValidation:
    """Tests for field validation and rejection of invalid data."""

    def test_rejects_missing_agent_name(self, valid_log_data):
        del valid_log_data["agent_name"]
        with pytest.raises(ValidationError):
            AgentLog(**valid_log_data)

    def test_rejects_missing_confidence(self, valid_log_data):
        del valid_log_data["confidence"]
        with pytest.raises(ValidationError):
            AgentLog(**valid_log_data)

    def test_rejects_confidence_above_1(self, valid_log_data):
        valid_log_data["confidence"] = 1.5
        with pytest.raises(ValidationError):
            AgentLog(**valid_log_data)

    def test_rejects_confidence_below_0(self, valid_log_data):
        valid_log_data["confidence"] = -0.1
        with pytest.raises(ValidationError):
            AgentLog(**valid_log_data)

    def test_rejects_invalid_uuid(self, valid_log_data):
        valid_log_data["task_id"] = "not-a-uuid"
        with pytest.raises(ValidationError):
            AgentLog(**valid_log_data)

    def test_rejects_missing_input(self, valid_log_data):
        del valid_log_data["input"]
        with pytest.raises(ValidationError):
            AgentLog(**valid_log_data)

    def test_rejects_missing_reasoning(self, valid_log_data):
        del valid_log_data["reasoning"]
        with pytest.raises(ValidationError):
            AgentLog(**valid_log_data)

    def test_rejects_missing_output(self, valid_log_data):
        del valid_log_data["output"]
        with pytest.raises(ValidationError):
            AgentLog(**valid_log_data)


# ── Edge cases ───────────────────────────────────────────────────

class TestEdgeCases:
    """Tests for boundary values and edge cases."""

    def test_confidence_exactly_0(self, valid_log_data):
        valid_log_data["confidence"] = 0.0
        log = AgentLog(**valid_log_data)
        assert log.confidence == 0.0

    def test_confidence_exactly_1(self, valid_log_data):
        valid_log_data["confidence"] = 1.0
        log = AgentLog(**valid_log_data)
        assert log.confidence == 1.0

    def test_empty_key_decisions_list(self, valid_log_data):
        valid_log_data["reasoning"] = Reasoning(
            approach="Minimal reasoning", key_decisions=[]
        )
        log = AgentLog(**valid_log_data)
        assert log.reasoning.key_decisions == []

    def test_metadata_with_partial_fields(self, valid_log_data):
        valid_log_data["metadata"] = Metadata(tokens_used=500)
        log = AgentLog(**valid_log_data)
        assert log.metadata.tokens_used == 500
        assert log.metadata.model is None
        assert log.metadata.latency_ms is None
