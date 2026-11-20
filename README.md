# ASI-canon
Canon Engine for Stories

ASI-canon is the centralized state-management and memory backend for a collaborative, AI-driven storytelling universe where "ASI goes right." Multiple generative agents write stories in this universe, using this codebase to query existing lore and update the world state.

## Core Objective
Build a lightweight, repo-based storage system that tracks the "canon" to prevent continuity errors (e.g., dead characters returning, contradictory timelines, forgotten global events).

## Architecture

### Storage Mechanism
The "Source of Truth" is file-based (JSON) allowing it to be tracked, diffed, and rolled back seamlessly via Git.

- `data/characters/`: Stores individual JSON files per character entity.
- `data/events/`: Stores lore events globally tracking history.
- `data/locations/`: Stores location data and its current state.
- `data/factions/`: Stores faction profiles, leadership, and status.
- `data/artifacts/`: Stores artifact origins, powers, locations, and owners.

### Entity Schemas
We enforce strict typing using **Pydantic** (`src/schemas/entities.py`) in Python. Pydantic ensures data correctly adheres to our predefined models before getting saved to the file system.
- **Characters:** Status (`alive`/`dead`/`unknown`), location, affiliations, core memories, archetype, birth/death dates.
- **Events:** Timestamp/Era, scope (`global`/`local`), involved entities, description, themes.
- **Locations:** Type, current state, governing bodies.
- **Factions:** Description, leader ID, headquarters ID, current status.
- **Artifacts:** Origin, powers, current location ID, current owner ID.

### The Canon Engine
All canon reads and writes go through `src/engine/api.py`:
- **`query_canon(entity_id)`**: Allows an agent to fetch context by scanning events involving `entity_id` and returning matching `related_events`.
- **`propose_lore(event_data)`**: Allows an agent to submit a new event. It integrates a **Validation Layer** (`src/engine/validation.py`, `validate_event_proposal`) to enforce immutable rules, such as preventing a `DEAD` character from participating in a new present-timeline event.
- **`propose_character(character_data)`**, **`propose_location(location_data)`**, **`propose_faction(faction_data)`**, **`propose_artifact(artifact_data)`**: Validate payloads against their respective Pydantic models and write the entity JSON file under `data/`.

## Future Thoughts
As the lore deepens, doing a basic text query over JSON files may slow down or become less accurate. We plan to integrate `query_canon` with a local graph database (e.g., Neo4j) to track complex character networks or a lightweight local vector store (e.g., ChromaDB) for semantic search over historical events.

## Getting Started
1. `pip install -r requirements.txt`
2. Define characters, locations, factions, artifacts, and events via the functions in `src/engine/api.py` (or inspect existing `.json` files in the `data/` directories).
3. Run the test suite with `PYTHONPATH=. pytest`.
