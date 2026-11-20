import json
from pathlib import Path
import pytest

from src.schemas.entities import (
    Artifact,
    Character,
    Event,
    EventScope,
    Faction,
    Location,
    Status,
)
from src.engine.api import (
    load_all_events,
    load_character,
    propose_character,
    propose_location,
    query_canon,
)
from src.engine.validation import validate_event_proposal


REPO_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

SCHEMA_DIRS = [
    ("characters", Character),
    ("events", Event),
    ("locations", Location),
    ("factions", Faction),
    ("artifacts", Artifact),
]


@pytest.mark.parametrize("subdir,schema_cls", SCHEMA_DIRS)
def test_committed_data_parses_into_schemas(subdir, schema_cls):
    """Verify every committed JSON file under data/ parses into its Pydantic schema."""
    target_dir = REPO_DATA_DIR / subdir
    json_files = sorted(target_dir.glob("*.json"))
    assert json_files, f"Expected at least one JSON file in {target_dir}"

    for json_path in json_files:
        with json_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
        entity = schema_cls(**payload)
        assert entity.id == json_path.stem


def test_committed_events_pass_validation(monkeypatch):
    """Verify all committed events pass validate_event_proposal against committed characters."""
    monkeypatch.setenv("DATA_DIR", str(REPO_DATA_DIR))
    events = load_all_events()
    assert len(events) > 0

    for event in events:
        result = validate_event_proposal(event)
        assert result["is_valid"] is True, f"{event.id} failed validation: {result}"


def test_load_all_events_missing_dir_returns_empty(tmp_path, monkeypatch):
    """load_all_events() returns [] when the events directory does not exist."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    assert load_all_events() == []


def test_load_all_events_skips_non_json_files(tmp_path, monkeypatch):
    """load_all_events() loads .json files and ignores non-.json files in events/."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    events_dir = tmp_path / "events"
    events_dir.mkdir(parents=True, exist_ok=True)

    (events_dir / "README.txt").write_text("not an event", encoding="utf-8")
    (events_dir / "notes.md").write_text("# notes", encoding="utf-8")
    event_payload = {
        "id": "evt_json_only",
        "name": "Valid JSON Event",
        "timestamp": "Era 1 - Year 1",
        "scope": "local",
        "involved_entities": [],
        "description": "Only json files should be loaded.",
    }
    (events_dir / "evt_json_only.json").write_text(
        json.dumps(event_payload), encoding="utf-8"
    )

    events = load_all_events()
    assert len(events) == 1
    assert events[0].id == "evt_json_only"


def test_load_character_nonexistent_returns_none(tmp_path, monkeypatch):
    """load_character() returns None when no character JSON matches the ID."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    assert load_character("char_does_not_exist") is None


def test_query_canon_no_matching_events_returns_empty(tmp_path, monkeypatch):
    """query_canon() returns empty related_events when no events involve entity_id."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    events_dir = tmp_path / "events"
    events_dir.mkdir(parents=True, exist_ok=True)
    (events_dir / "evt_other.json").write_text(
        json.dumps(
            {
                "id": "evt_other",
                "name": "Unrelated Event",
                "timestamp": "Era 1 - Year 2",
                "scope": "local",
                "involved_entities": ["char_someone_else"],
                "description": "Nothing to see here.",
            }
        ),
        encoding="utf-8",
    )

    result = query_canon("char_missing")
    assert result == {"entity_id": "char_missing", "related_events": []}


def test_validate_event_proposal_status_unknown_accepted(tmp_path, monkeypatch):
    """validate_event_proposal() accepts characters with Status.UNKNOWN."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    propose_character(
        {"id": "char_mystery", "name": "The Wanderer", "status": Status.UNKNOWN.value}
    )

    event = Event(
        id="evt_unknown_char",
        name="Shadow Sighting",
        timestamp="Era 2 - Year 1",
        scope=EventScope.LOCAL,
        involved_entities=["char_mystery"],
        description="The Wanderer appears briefly.",
    )
    result = validate_event_proposal(event)
    assert result["is_valid"] is True


def test_validate_event_proposal_unknown_entity_ids_accepted(tmp_path, monkeypatch):
    """validate_event_proposal() accepts non-existent IDs and non-character entity IDs."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    propose_location(
        {"id": "loc_outpost", "name": "Outer Outpost", "current_state": "Intact"}
    )

    event = Event(
        id="evt_non_char_entities",
        name="Signal Detected",
        timestamp="Era 2 - Year 2",
        scope=EventScope.LOCAL,
        involved_entities=["loc_outpost", "fac_untracked", "char_nonexistent"],
        description="Signal detected at Outer Outpost.",
    )
    result = validate_event_proposal(event)
    assert result["is_valid"] is True


def test_validate_event_proposal_multi_entity_dead_vs_alive_unknown(
    tmp_path, monkeypatch
):
    """Multi-entity events fail if any involved character is DEAD, and pass for alive/unknown."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    propose_character({"id": "char_alive", "name": "Vera", "status": Status.ALIVE.value})
    propose_character(
        {"id": "char_unknown", "name": "Cipher", "status": Status.UNKNOWN.value}
    )
    propose_character({"id": "char_dead", "name": "Kaelen", "status": Status.DEAD.value})
    propose_location(
        {"id": "loc_hub", "name": "Central Hub", "current_state": "Operational"}
    )

    accepted_event = Event(
        id="evt_multi_valid",
        name="Council Briefing",
        timestamp="Era 3 - Year 1",
        scope=EventScope.GLOBAL,
        involved_entities=["loc_hub", "char_alive", "char_unknown", "fac_unlisted"],
        description="Living and unknown-status characters meet at the hub.",
    )
    accepted_result = validate_event_proposal(accepted_event)
    assert accepted_result["is_valid"] is True

    rejected_event = Event(
        id="evt_multi_invalid",
        name="Impossible Reunion",
        timestamp="Era 3 - Year 2",
        scope=EventScope.LOCAL,
        involved_entities=["loc_hub", "char_alive", "char_unknown", "char_dead"],
        description="Includes a deceased character alongside valid ones.",
    )
    rejected_result = validate_event_proposal(rejected_event)
    assert rejected_result["is_valid"] is False
    assert "Kaelen" in rejected_result["reason"]
    assert "char_dead" in rejected_result["reason"]
