import json
import os
import pytest

from src.schemas.entities import Artifact
from src.engine.api import propose_artifact

def test_artifact_insertion(tmp_path, monkeypatch):
    mock_data_dir = str(tmp_path)
    monkeypatch.setenv("DATA_DIR", mock_data_dir)

    artifact_data = {
        "id": "art_001",
        "name": "Drive Core Fragment",
        "origin": "Architects",
        "powers": ["Healing", "Energy Manipulation"],
        "current_location_id": "loc_deep_ring",
        "current_owner_id": "char_jax"
    }

    result = propose_artifact(artifact_data)
    assert result["success"] == True
    assert result["artifact_id"] == "art_001"

    assert os.path.exists(os.path.join(mock_data_dir, "artifacts", "art_001.json"))
    with open(os.path.join(mock_data_dir, "artifacts", "art_001.json"), "r") as f:
        data = json.load(f)
        assert data["name"] == "Drive Core Fragment"
        assert data["origin"] == "Architects"
        assert data["powers"] == ["Healing", "Energy Manipulation"]
        assert data["current_location_id"] == "loc_deep_ring"
        assert data["current_owner_id"] == "char_jax"
