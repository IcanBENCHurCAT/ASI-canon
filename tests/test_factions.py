import json
import os
import pytest

from src.schemas.entities import Faction
from src.engine.api import propose_faction

def test_faction_insertion(tmp_path, monkeypatch):
    mock_data_dir = str(tmp_path)
    monkeypatch.setenv("DATA_DIR", mock_data_dir)

    faction_data = {
        "id": "fac_rebels",
        "name": "The Rebels",
        "description": "Freedom fighters of the new era.",
        "leader_id": "char_hero",
        "headquarters_id": "loc_base",
        "current_status": "Active"
    }

    result = propose_faction(faction_data)
    assert result["success"] == True
    assert result["faction_id"] == "fac_rebels"

    assert os.path.exists(os.path.join(mock_data_dir, "factions", "fac_rebels.json"))
    with open(os.path.join(mock_data_dir, "factions", "fac_rebels.json"), "r") as f:
        data = json.load(f)
        assert data["name"] == "The Rebels"
        assert data["description"] == "Freedom fighters of the new era."
        assert data["leader_id"] == "char_hero"
        assert data["headquarters_id"] == "loc_base"
        assert data["current_status"] == "Active"
