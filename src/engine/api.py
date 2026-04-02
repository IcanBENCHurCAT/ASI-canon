import json
import os
from typing import List, Dict, Any, Optional

from src.schemas.entities import Character, Event, Location

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
            with open(filepath, "r") as f:
                data = json.load(f)
                events.append(Event(**data))
    return events


def load_character(char_id: str) -> Optional[Character]:
    filepath = os.path.join(get_data_dir(), "characters", f"{char_id}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
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
    events_dir = os.path.join(get_data_dir(), "events")
    os.makedirs(events_dir, exist_ok=True)

    filepath = os.path.join(events_dir, f"{event.id}.json")
    with open(filepath, "w") as f:
        f.write(event.model_dump_json(indent=4))

    return {
        "success": True,
        "event_id": event.id,
        "message": "Lore successfully integrated into Canon."
    }
