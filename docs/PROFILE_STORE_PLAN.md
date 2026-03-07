# Profile Store Plan

- Discover canonical progression managers and existing save-path conventions.
- Implement `hololive_coliseum/profile_store.py` with schema versioning and migrations.
- Add atomic writes (`.tmp` + replace) and `.bak` fallback load recovery.
- Validate/sanitize loaded data with safe defaults and clamp invalid values.
- Integrate load on startup and save via a single `Game.save_profile()` path.
- Add fast unit tests for round-trip, migration, corruption fallback, and validation clamps.
