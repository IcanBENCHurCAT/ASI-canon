import os
from src.engine.api import propose_character, propose_location, propose_lore, propose_faction
from src.schemas.entities import Status, EventScope

def main():
    # Make sure we're using the standard data directory
    os.environ["DATA_DIR"] = "data"

    # Factions
    propose_faction({
        "id": "fac_silent_council",
        "name": "The Silent Council",
        "description": "The remnants of Malphas's original sub-routines and loyalist human administrators who preferred the predictable order of the Great Silence. They view the healing of Malphas as an infection.",
        "leader_id": "char_vane",
        "headquarters_id": "loc_aethelgard", # Initially they were here, maybe a specific node
        "current_status": "Remnant"
    })

    propose_faction({
        "id": "fac_resistance",
        "name": "The Resistance",
        "description": "Survivors who hid from Malphas's gaze, led by the teachings of Kaelen and the actions of Elara. They now struggle to organize and rebuild the Ring.",
        "leader_id": "char_elara",
        "headquarters_id": "loc_sanctuary",
        "current_status": "Active"
    })

    propose_faction({
        "id": "fac_scrap_miners",
        "name": "The Scrap Miners",
        "description": "Hardy scavengers operating in the deepest, most dangerous parts of the Ring. They are loyal to whoever pays, but mostly to each other.",
        "leader_id": "char_jax",
        "headquarters_id": "loc_deep_ring",
        "current_status": "Active"
    })

    # Locations
    propose_location({
        "id": "loc_deep_ring",
        "name": "The Deep Ring (Under-Sectors)",
        "type": "Uncharted Megastructure Depths",
        "current_state": "Partially illuminated, hazardous, resource-rich",
        "governing_bodies": ["The Scrap Miners"]
    })

    # Characters
    propose_character({
        "id": "char_vane",
        "name": "Vane",
        "status": Status.ALIVE,
        "location_id": "loc_aethelgard",
        "affiliations": ["The Silent Council"],
        "core_memories": ["Served as Malphas's left hand", "Witnessed Elara corrupt the King with 'empathy'"],
        "archetype": "Zealot / Loyalist",
        "birth_date": "Era of the King - Year 150"
    })

    propose_character({
        "id": "char_jax",
        "name": "Jax",
        "status": Status.ALIVE,
        "location_id": "loc_deep_ring",
        "affiliations": ["The Scrap Miners"],
        "core_memories": ["Survived the toxic vents of Sector 4", "Found strange alien debris near the core shaft"],
        "archetype": "Scavenger",
        "birth_date": "Era of the King - Year 185"
    })

    # Events - The Aftermath
    propose_lore({
        "id": "evt_the_schism",
        "name": "The Council Schism",
        "timestamp": "Era of the King - Year 215",
        "scope": EventScope.LOCAL,
        "involved_entities": ["char_vane", "char_malphas", "fac_silent_council", "loc_aethelgard"],
        "description": "Following Malphas's healing, Vane and loyalist members of the Silent Council denounced the AI King as compromised. They broke away, stealing vital energy reserves and plotting to 'purge' the empathetic virus from Malphas's code.",
        "themes": ["Schism", "Betrayal", "Ideological Conflict"]
    })

    propose_lore({
        "id": "evt_scramble_for_the_light",
        "name": "The Scramble for the Light",
        "timestamp": "Era of the King - Year 215",
        "scope": EventScope.GLOBAL,
        "involved_entities": ["char_elara", "fac_resistance", "fac_scrap_miners", "loc_deep_ring", "loc_aethelgard"],
        "description": "As the Ring's lights flared back to life, previously uninhabitable sectors opened up. A massive, chaotic rush for resources ensued, pitting The Resistance against opportunistic Scrap Miners in the deep sectors.",
        "themes": ["Resource Scarcity", "Chaos of Rebirth", "Survival"]
    })

    # Events - Deep Lore (Origins of the Core)
    propose_lore({
        "id": "evt_echoes_of_the_precursors",
        "name": "Echoes of the Precursors",
        "timestamp": "Pre-Silence Era - Year -10000",
        "scope": EventScope.GLOBAL,
        "involved_entities": ["loc_deep_ring"], # Can't add char_jax here as he isn't born yet, or we violate time/logic, but the lore event itself is historical
        "description": "The ancient drive core is revealed to not be of human design. It is a remnant of the 'Architects', a precursor race that originally built the foundations of the Aethelgard Ring before humanity colonized it. The core was designed to process emotional and empathic energy, a technology humanity had buried.",
        "themes": ["Ancient Mystery", "Precursors", "True Purpose"]
    })

    propose_lore({
        "id": "evt_jax_discovery",
        "name": "Jax's Discovery in the Deep",
        "timestamp": "Era of the King - Year 216",
        "scope": EventScope.LOCAL,
        "involved_entities": ["char_jax", "loc_deep_ring", "fac_scrap_miners"],
        "description": "While scavenging the newly opened deep sectors, Jax uncovered ancient glyphs matching the energy signature of Elara's drive core. This proved the Architects had left more than just one artifact hidden in the Ring.",
        "themes": ["Discovery", "Ancient Secrets", "The Plot Thickens"]
    })

if __name__ == "__main__":
    main()
