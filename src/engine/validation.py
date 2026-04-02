from typing import Dict, Any

from src.schemas.entities import Event, Status
from src.engine.api import load_character


def validate_event_proposal(event: Event) -> Dict[str, Any]:
    """
    Validates a proposed event against current canon rules.
    """

    # 1. Status conflicts: Check if any involved character is DEAD.
    # Immutable Rule: Interacting with a deceased entity is invalid unless specified as a flashback (not implemented here).
    for entity_id in event.involved_entities:
        # Assuming ID formats tell us if it's a character or we just try loading them.
        # Here we just try loading it as a character to see if they exist.
        character = load_character(entity_id)
        if character and character.status == Status.DEAD:
            return {
                "is_valid": False,
                "reason": f"Immutable Rule Violation: Character {character.name} ({character.id}) is dead and cannot participate in new present events."
            }

    # 2. Temporal Paradoxes / Missing Prerequisites
    # (To be fully implemented with a Graph DB/Vector store)
    # E.g., check if the event timestamp is sequentially valid for involved entities.

    return {
        "is_valid": True,
        "reason": "Passed validation."
    }
