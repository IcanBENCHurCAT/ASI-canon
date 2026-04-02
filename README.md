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

### Entity Schemas
We enforce strict typing using **Pydantic** in Python. Pydantic ensures data correctly adheres to our predefined models before getting saved to the file system.
- **Characters:** Status (alive/dead), location, affiliations, core memories.
- **Events:** Timestamp/Era, scope (global/local), involved entities.
- **Locations:** Current state, governing bodies.

### The Canon Engine
- **QueryCanon:** Allows an agent to fetch context (`src/engine/api.py`). It reads the file system state and returns matched entities.
- **ProposeLore:** Allows an agent to submit a new event. It integrates a **Validation Layer** (`src/engine/validation.py`) to enforce immutable rules, such as preventing a `DEAD` character from participating in a new present-timeline event.

## Future Thoughts
As the lore deepens, doing a basic text query over JSON files may slow down or become less accurate. We plan to integrate `QueryCanon` with a local graph database (e.g., Neo4j) to track complex character networks or a lightweight local vector store (e.g., ChromaDB) for semantic search over historical events.

## Getting Started
1. `pip install -r requirements.txt`
2. Define characters and events as `.json` in the `data/` directories.
3. Use the functions in `src/engine/api.py` to interact with Canon.
