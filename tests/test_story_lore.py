import json
import os
import pytest

from src.schemas.entities import Character, Status, Event, EventScope, Location
from src.engine.api import propose_character, propose_location, propose_lore, query_canon

def test_character_insertion(tmp_path, monkeypatch):
    mock_data_dir = str(tmp_path)
    monkeypatch.setenv("DATA_DIR", mock_data_dir)

    char_data = {
        "id": "char_hero",
        "name": "Aris",
        "status": "alive",
        "archetype": "Reluctant Hero",
        "birth_date": "Year 0"
    }

    result = propose_character(char_data)
    assert result["success"] == True
    assert result["character_id"] == "char_hero"

    assert os.path.exists(os.path.join(mock_data_dir, "characters", "char_hero.json"))
    with open(os.path.join(mock_data_dir, "characters", "char_hero.json"), "r") as f:
        data = json.load(f)
        assert data["name"] == "Aris"
        assert data["archetype"] == "Reluctant Hero"
        assert data["birth_date"] == "Year 0"
        assert data["death_date"] == None

def test_location_insertion(tmp_path, monkeypatch):
    mock_data_dir = str(tmp_path)
    monkeypatch.setenv("DATA_DIR", mock_data_dir)

    loc_data = {
        "id": "loc_base",
        "name": "Alpha Base",
        "type": "Space Station",
        "current_state": "Operational"
    }

    result = propose_location(loc_data)
    assert result["success"] == True
    assert result["location_id"] == "loc_base"

    assert os.path.exists(os.path.join(mock_data_dir, "locations", "loc_base.json"))
    with open(os.path.join(mock_data_dir, "locations", "loc_base.json"), "r") as f:
        data = json.load(f)
        assert data["name"] == "Alpha Base"
        assert data["type"] == "Space Station"

def test_event_creation_valid(tmp_path, monkeypatch):
    mock_data_dir = str(tmp_path)
    monkeypatch.setenv("DATA_DIR", mock_data_dir)

    # First add a character and location
    propose_character({"id": "char_1", "name": "Bob", "status": "alive"})
    propose_location({"id": "loc_1", "name": "Earth", "current_state": "Mostly harmless"})

    evt_data = {
        "id": "evt_1",
        "name": "Arrival",
        "timestamp": "Year 0",
        "scope": "global",
        "involved_entities": ["char_1", "loc_1"],
        "description": "Bob arrives.",
        "themes": ["New Beginnings"]
    }

    result = propose_lore(evt_data)
    assert result["success"] == True

    query_res = query_canon("char_1")
    assert len(query_res["related_events"]) == 1
    assert query_res["related_events"][0]["themes"] == ["New Beginnings"]

def test_event_creation_invalid_dead_character(tmp_path, monkeypatch):
    mock_data_dir = str(tmp_path)
    monkeypatch.setenv("DATA_DIR", mock_data_dir)

    propose_character({"id": "char_dead", "name": "Alice", "status": "dead"})

    evt_data = {
        "id": "evt_invalid",
        "name": "Zombie Attack",
        "timestamp": "Year 1",
        "scope": "local",
        "involved_entities": ["char_dead"],
        "description": "Alice returns.",
        "themes": ["Horror"]
    }

    result = propose_lore(evt_data)
    assert result["success"] == False
    assert "dead" in result["error"].lower()
