import json
import os
import re
from typing import List, Dict, Any, Optional

from src.schemas.entities import (
    Character,
    Event,
    Location,
    Faction,
    Artifact,
    ENTITY_ID_PATTERN,
)

_ENTITY_ID_RE = re.compile(ENTITY_ID_PATTERN)


def _validate_entity_id(entity_id: str) -> str:
    """Validate that an entity ID contains only safe filename characters."""
    if not isinstance(entity_id, str) or not _ENTITY_ID_RE.fullmatch(entity_id):
        raise ValueError(
            f"Invalid entity ID {entity_id!r}: must match {ENTITY_ID_PATTERN}"
        )
    return entity_id


def _safe_entity_path(subdir: str, entity_id: str) -> str:
    """Resolve and verify an entity JSON path stays inside its data subdirectory."""
    _validate_entity_id(entity_id)
    base_dir = os.path.realpath(os.path.join(get_data_dir(), subdir))
    target = os.path.realpath(os.path.join(base_dir, f"{entity_id}.json"))
    if os.path.commonpath([base_dir, target]) != base_dir:
        raise ValueError(
            f"Entity path escapes base directory for {entity_id!r}"
        )
    return target


# Use a getter for DATA_DIR so changes to os.environ are reflected in subsequent calls
def get_data_dir() -> str:
    return os.environ.get("DATA_DIR", "data")


def load_all_events() -> List[Event]:
    events = []
    events_dir = os.path.join(get_data_dir(), "events")
    if not os.path.exists(events_dir):
        return events

    for filename in os.listdir(events_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(events_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                events.append(Event(**data))
    return events


def load_character(char_id: str) -> Optional[Character]:
    filepath = _safe_entity_path("characters", char_id)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Character(**data)
    return None


def query_canon(entity_id: str) -> Dict[str, Any]:
    """
    Query all events related to a specific entity (Character or Location).
    """
    all_events = load_all_events()
    related_events = [
        event.model_dump() for event in all_events
        if entity_id in event.involved_entities
    ]
    return {
        "entity_id": entity_id,
        "related_events": related_events
    }


def propose_character(character_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Propose a new character to be added to the canon.
    """
    character = Character(**character_data)

    filepath = _safe_entity_path("characters", character.id)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(character.model_dump_json(indent=4))

    return {
        "success": True,
        "character_id": character.id,
        "message": "Character successfully integrated into Canon."
    }

def propose_location(location_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Propose a new location to be added to the canon.
    """
    location = Location(**location_data)

    filepath = _safe_entity_path("locations", location.id)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(location.model_dump_json(indent=4))

    return {
        "success": True,
        "location_id": location.id,
        "message": "Location successfully integrated into Canon."
    }

def propose_faction(faction_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Propose a new faction to be added to the canon.
    """
    faction = Faction(**faction_data)

    filepath = _safe_entity_path("factions", faction.id)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(faction.model_dump_json(indent=4))

    return {
        "success": True,
        "faction_id": faction.id,
        "message": "Faction successfully integrated into Canon."
    }

def propose_artifact(artifact_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Propose a new artifact to be added to the canon.
    """
    artifact = Artifact(**artifact_data)

    filepath = _safe_entity_path("artifacts", artifact.id)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(artifact.model_dump_json(indent=4))

    return {
        "success": True,
        "artifact_id": artifact.id,
        "message": "Artifact successfully integrated into Canon."
    }

def propose_lore(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Propose a new event to be added to the canon.
    Runs validation logic before writing.
    """
    from src.engine.validation import validate_event_proposal

    event = Event(**event_data)

    validation_result = validate_event_proposal(event)
    if not validation_result["is_valid"]:
        return {
            "success": False,
            "error": validation_result["reason"]
        }

    # Write the event to repo if valid
    filepath = _safe_entity_path("events", event.id)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(event.model_dump_json(indent=4))

    return {
        "success": True,
        "event_id": event.id,
        "message": "Lore successfully integrated into Canon."
    }
