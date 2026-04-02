import json
import os
import pytest

from src.schemas.entities import Character, Status, Event, EventScope
from src.engine.api import propose_lore, query_canon

def test_canon_flow(tmp_path, monkeypatch):
    # Mock DATA_DIR to use pytest's tmp_path fixture
    mock_data_dir = str(tmp_path)
    monkeypatch.setenv("DATA_DIR", mock_data_dir)

    # Setup mock character
    char_id = "char_001"
    os.makedirs(os.path.join(mock_data_dir, "characters"), exist_ok=True)
    with open(os.path.join(mock_data_dir, "characters", f"{char_id}.json"), "w") as f:
        char_data = {
            "id": char_id,
            "name": "Dr. Aris",
            "status": "alive"
        }
        json.dump(char_data, f)

    # Test valid proposal
    valid_event = {
        "id": "evt_001",
        "name": "First Contact",
        "timestamp": "Era 1 - Year 5",
        "scope": "global",
        "involved_entities": [char_id],
        "description": "Met the ASI."
    }

    result = propose_lore(valid_event)
    assert result["success"] == True

    # Test Query
    query_result = query_canon(char_id)
    assert len(query_result["related_events"]) == 1
    assert query_result["related_events"][0]["id"] == "evt_001"

    # Setup dead character
    dead_char_id = "char_002"
    with open(os.path.join(mock_data_dir, "characters", f"{dead_char_id}.json"), "w") as f:
        dead_char_data = {
            "id": dead_char_id,
            "name": "Commander Zod",
            "status": "dead"
        }
        json.dump(dead_char_data, f)

    # Test invalid proposal (dead character interacting)
    invalid_event = {
        "id": "evt_002",
        "name": "Second Contact",
        "timestamp": "Era 1 - Year 6",
        "scope": "local",
        "involved_entities": [dead_char_id],
        "description": "Zod strikes back."
    }

    result = propose_lore(invalid_event)
    assert result["success"] == False
    assert "is dead" in result["error"]
