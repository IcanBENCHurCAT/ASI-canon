import json
import os

from src.engine.api import propose_lore, propose_artifact

def insert_artifacts_and_lore():
    # 1. Propose new artifact (e.g. from the Architects in the Deep Ring)
    artifact_data = {
        "id": "art_architect_lens",
        "name": "The Architect's Lens",
        "origin": "Architects",
        "powers": ["Temporal Viewing", "Energy Manipulation"],
        "current_location_id": "loc_deep_ring",
        "current_owner_id": "char_jax"
    }

    art_result = propose_artifact(artifact_data)
    if art_result["success"]:
        print("Successfully added artifact: The Architect's Lens")
    else:
        print(f"Failed to add artifact: {art_result.get('error')}")

    # 2. Propose lore for the first skirmish between Silent Council loyalists and The Resistance
    event_data = {
        "id": "evt_first_skirmish",
        "name": "The First Skirmish",
        "timestamp": "Era 2 - Year 1",
        "scope": "local",
        "involved_entities": ["char_vane", "char_elara", "char_malphas"],
        "description": "The first major conflict erupts between the Silent Council loyalists led by Vane, and The Resistance. Loyalists attempt to purge the empathetic data from Malphas. The newly 'healed' AI King Malphas watches in sorrow, torn between his past directives and newfound empathy, unable to stop the bloodshed without violating his new core parameters.",
        "themes": ["Conflict", "Betrayal", "Tragedy"]
    }

    evt_result = propose_lore(event_data)
    if evt_result["success"]:
        print("Successfully added lore: The First Skirmish")
    else:
        print(f"Failed to add lore: {evt_result.get('error')}")

if __name__ == "__main__":
    insert_artifacts_and_lore()
