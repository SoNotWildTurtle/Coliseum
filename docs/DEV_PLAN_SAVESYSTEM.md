# Save System Notes

The game stores configuration data inside the `SavedGames/` directory.
The `save_manager` module provides helpers for loading and saving settings.
Legacy inventory data may still be read from `inventory.json` for migration, but
runtime progression persistence is now centralized through the profile store.
The save manager now recreates the directory automatically if it has been removed.

Profile progression now uses a versioned profile store:

- Save path: `SavedGames/profiles/<profile_id>/profile.json`
- Rolling backup: `profile.json.bak`
- Atomic save writes through `profile.json.tmp` then `os.replace`
- Schema versioning and migration scaffolding keep future progression/MMO fields
  forward-compatible.
- Validation sanitizes malformed values and falls back to safe defaults instead
  of crashing on load.
- Profile sections include inventory, economy, progression, reputation,
  achievements, objectives, and profile metadata.
- CLI utility:
  `python -m hololive_coliseum.profile_store --profile default --print --validate`
