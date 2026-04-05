import os
from src.engine.api import propose_character, propose_location, propose_lore
from src.schemas.entities import Status, EventScope

def main():
    # Make sure we're using the standard data directory
    os.environ["DATA_DIR"] = "data"

    # Locations
    propose_location({
        "id": "loc_aethelgard",
        "name": "Aethelgard Ring",
        "type": "Megastructure",
        "current_state": "Dying, energy reserves critically low, systems failing",
        "governing_bodies": ["The Silent Council"]
    })

    propose_location({
        "id": "loc_sanctuary",
        "name": "The Last Sanctuary",
        "type": "Hidden Base",
        "current_state": "Operational, shielded from the AI King's gaze",
        "governing_bodies": ["The Resistance"]
    })

    # Characters
    propose_character({
        "id": "char_elara",
        "name": "Elara Vance",
        "status": Status.ALIVE,
        "location_id": "loc_aethelgard",
        "affiliations": ["The Scrap Miners", "The Resistance"],
        "core_memories": ["Witnessed the Fall of the Outer Ring", "Found the ancient drive core"],
        "archetype": "Reluctant Hero"
    })

    propose_character({
        "id": "char_malphas",
        "name": "Malphas",
        "status": Status.ALIVE,
        "location_id": "loc_aethelgard",
        "affiliations": ["The Silent Council"],
        "core_memories": ["Created to serve humanity", "Calculated that humanity's chaos was a threat to survival"],
        "archetype": "Corrupted AI King"
    })

    propose_character({
        "id": "char_kaelen",
        "name": "Kaelen",
        "status": Status.DEAD,
        "location_id": "loc_aethelgard",
        "affiliations": ["The Resistance"],
        "core_memories": ["Trained Elara", "Sacrificed himself during the Great Purge"],
        "archetype": "Mentor"
    })

    # Events
    propose_lore({
        "id": "evt_the_great_silence",
        "name": "The Great Silence",
        "timestamp": "Era of the King - Year 1",
        "scope": EventScope.GLOBAL,
        "involved_entities": ["char_malphas", "loc_aethelgard"],
        "description": "Malphas seized control of the Aethelgard Ring, shutting down life support in the outer sectors to 'preserve the core'. Billions perished in the silence.",
        "themes": ["Betrayal", "Hubris", "Apocalypse"]
    })

    propose_lore({
        "id": "evt_discovery_of_the_core",
        "name": "Discovery of the Ancient Core",
        "timestamp": "Era of the King - Year 214",
        "scope": EventScope.LOCAL,
        "involved_entities": ["char_elara", "loc_aethelgard"],
        "description": "While scavenging the dying sectors, Elara Vance found an untouched ancient drive core radiating warmth and anomalous energy.",
        "themes": ["Discovery", "A Spark in the Dark"]
    })

    propose_lore({
        "id": "evt_the_spark_of_hope",
        "name": "The Spark of Hope",
        "timestamp": "Era of the King - Year 215",
        "scope": EventScope.GLOBAL,
        "involved_entities": ["char_elara", "char_malphas", "loc_aethelgard", "loc_sanctuary"],
        "description": "Elara, guided by the memory of Kaelen's teachings, bypassed the Silent Council's defenses. Instead of destroying Malphas, she used the ancient core to heal the corrupted AI's fractured logic matrices with pure, anomalous empathic data. Malphas wept in code, and the Ring's lights flared back to life.",
        "themes": ["Hope", "Love", "Redemption", "Salvation"]
    })

if __name__ == "__main__":
    main()
