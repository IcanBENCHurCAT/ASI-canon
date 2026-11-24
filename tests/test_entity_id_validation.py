import json
import pytest
from pydantic import ValidationError

from src.schemas.entities import (
    Artifact,
    Character,
    Event,
    Faction,
    Location,
)
from src.engine.api import (
    load_all_events,
    load_character,
    propose_artifact,
    propose_character,
    propose_faction,
    propose_location,
    propose_lore,
)

INVALID_ENTITY_IDS = [
    "",
    "../evil",
    "../../etc/passwd",
    "sub/char_1",
    "sub\\char_1",
    "a b",
    "char.json",
    "..",
]


def _make_payload(model_cls, entity_id: str) -> dict:
    if model_cls is Character:
        return {"id": entity_id, "name": "Test Character"}
    if model_cls is Event:
        return {
            "id": entity_id,
            "name": "Test Event",
            "timestamp": "Era 1 - Year 1",
            "description": "Test description",
        }
    if model_cls is Location:
        return {
            "id": entity_id,
            "name": "Test Location",
            "current_state": "Operational",
        }
    if model_cls is Faction:
        return {
            "id": entity_id,
            "name": "Test Faction",
            "description": "Test faction description",
            "current_status": "Active",
        }
    if model_cls is Artifact:
        return {
            "id": entity_id,
            "name": "Test Artifact",
            "origin": "Architects",
        }
    raise ValueError(f"Unexpected model class: {model_cls}")


MODEL_PROPOSE_PAIRS = [
    (Character, propose_character),
    (Event, propose_lore),
    (Location, propose_location),
    (Faction, propose_faction),
    (Artifact, propose_artifact),
]


@pytest.mark.parametrize("model_cls,_propose_fn", MODEL_PROPOSE_PAIRS)
@pytest.mark.parametrize("bad_id", INVALID_ENTITY_IDS)
def test_schema_rejects_invalid_entity_ids(model_cls, _propose_fn, bad_id):
    """All 5 entity Pydantic models reject empty, whitespace, dot, and traversal IDs."""
    payload = _make_payload(model_cls, bad_id)
    with pytest.raises(ValidationError):
        model_cls(**payload)


@pytest.mark.parametrize("model_cls,propose_fn", MODEL_PROPOSE_PAIRS)
@pytest.mark.parametrize("bad_id", INVALID_ENTITY_IDS)
def test_propose_functions_reject_invalid_entity_ids(
    model_cls, propose_fn, bad_id, tmp_path, monkeypatch
):
    """All propose_* API functions reject invalid entity IDs before touching the filesystem."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    payload = _make_payload(model_cls, bad_id)
    with pytest.raises(ValidationError):
        propose_fn(payload)
    assert list(tmp_path.rglob("*")) == []


@pytest.mark.parametrize("bad_id", INVALID_ENTITY_IDS)
def test_load_character_rejects_invalid_and_traversal_ids(bad_id, tmp_path, monkeypatch):
    """load_character() raises ValueError on invalid IDs and blocks parent directory escapes."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    (tmp_path / "characters").mkdir(parents=True, exist_ok=True)
    # Place a decoy character JSON in parent tmp_path (outside characters/)
    (tmp_path / "decoy.json").write_text(
        json.dumps({"id": "decoy", "name": "Decoy Character", "status": "alive"}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_character(bad_id)
    with pytest.raises(ValueError):
        load_character("../decoy")


def test_load_character_rejects_non_string_id(tmp_path, monkeypatch):
    """load_character() raises ValueError when given a non-string entity ID."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    with pytest.raises(ValueError):
        load_character(None)  # type: ignore[arg-type]


def test_valid_entity_id_characters_accepted(tmp_path, monkeypatch):
    """Alphanumeric, underscore, and hyphen IDs succeed across models and API."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    valid_id = "Char_01-AZ_9"
    res = propose_character({"id": valid_id, "name": "Valid Hero"})
    assert res["success"] is True
    loaded = load_character(valid_id)
    assert loaded is not None
    assert loaded.id == valid_id


def test_unicode_roundtrip_character_and_lore(tmp_path, monkeypatch):
    """UTF-8 file I/O preserves accented Latin, em-dash, CJK, and Cyrillic text."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))

    unicode_name = "Élodie Vance — 希望 / Надежда"
    unicode_memory = "Watched the aurora over Zürich — «начало» (始まり)"
    char_res = propose_character(
        {
            "id": "char_unicode_01",
            "name": unicode_name,
            "status": "alive",
            "core_memories": [unicode_memory],
        }
    )
    assert char_res["success"] is True

    loaded_char = load_character("char_unicode_01")
    assert loaded_char is not None
    assert loaded_char.name == unicode_name
    assert loaded_char.core_memories == [unicode_memory]

    unicode_event_name = "Accord of Genève — 星海条約 / Соглашение"
    unicode_desc = "Treaty signed by Élodie — «мир» across the 星海."
    lore_res = propose_lore(
        {
            "id": "evt_unicode_01",
            "name": unicode_event_name,
            "timestamp": "Era 2 — Year 42",
            "scope": "global",
            "involved_entities": ["char_unicode_01"],
            "description": unicode_desc,
            "themes": ["Согласие", "希望"],
        }
    )
    assert lore_res["success"] is True

    events = load_all_events()
    assert len(events) == 1
    assert events[0].name == unicode_event_name
    assert events[0].description == unicode_desc
    assert events[0].timestamp == "Era 2 — Year 42"
    assert events[0].themes == ["Согласие", "希望"]
