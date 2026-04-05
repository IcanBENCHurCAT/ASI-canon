# Agent Guidelines for ASI-Canon

This file serves as a comprehensive guide for generative agents working on the ASI-canon codebase. It outlines the project's architecture, data modeling conventions, and instructions for how to contribute effectively without breaking the lore engine.

## Core Objective

ASI-canon is a centralized state-management and memory backend for an AI-driven storytelling universe. It uses a file-based JSON storage mechanism (trackable via Git) to prevent continuity errors and maintain a cohesive canon.

## Architecture & Data Storage

The data for this universe is file-based and resides in the `data/` directory.

- **`data/characters/`**: Individual JSON files for each character.
- **`data/events/`**: Lore events globally tracking history.
- **`data/locations/`**: Location data and current states.

### Interacting with the Canon

**DO NOT create JSON files manually.** Always use the Python API to propose new lore. This ensures that Pydantic validation checks are run against new entities to prevent continuity errors (e.g., trying to have a dead character participate in a new event).

The core API functions are located in `src/engine/api.py`:
- `propose_character(character_data: Dict[str, Any])`
- `propose_location(location_data: Dict[str, Any])`
- `propose_lore(event_data: Dict[str, Any])`
- `query_canon(entity_id: str)`

## Schemas & Validation

We use **Pydantic** (`src/schemas/entities.py`) to enforce strict typing and schema validation.

Current major properties:
- **Characters**: `status` (alive/dead), `archetype` (e.g. Reluctant Hero), `affiliations`.
- **Events**: `scope` (local/global), `involved_entities`, `themes` (e.g. Hope, Betrayal).
- **Locations**: `type` (e.g. Space Station, Planet), `current_state`.

The validation layer (`src/engine/validation.py`) enforces immutable universe rules. For example, it prevents events from including characters whose status is `DEAD`.

## Instructions for Agents

1. **Automation:** Whenever you need to add story elements, write a Python script (like `insert_story_lore.py`) that uses the API functions mentioned above.
2. **Testing:** Any new logic or new schema rules must be accompanied by pytest tests in the `tests/` directory. Run tests with `PYTHONPATH=. pytest`.
3. **Updating this File:** If you make significant architectural changes (e.g., swapping file-based JSON for a vector store like ChromaDB, or adding new entity schemas like "Factions" or "Items"), you **must** update this `AGENTS.md` file to reflect those changes so future agents understand the new structure.
4. **Pre-commit Checks:** Always ensure your tests pass and your code is clean before submitting a pull request.
