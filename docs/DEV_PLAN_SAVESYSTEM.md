# Save System Notes

The game stores configuration data inside the `SavedGames/` directory.
The `save_manager` module provides helpers for loading and saving settings.
Future updates will add player progress and unlocks. Inventory contents are now
saved to `inventory.json` so items persist between sessions.
The save manager now recreates the directory automatically if it has been removed.

Profile progression now uses a versioned profile store:

- Save path: `SavedGames/profiles/<profile_id>/profile.json`
- Rolling backup: `profile.json.bak`
- Atomic save writes through `profile.json.tmp` then `os.replace`
- Profile sections include inventory, economy, progression, reputation,
  achievements, objectives, and profile metadata.
- CLI utility:
  `python -m hololive_coliseum.profile_store --profile default --print --validate`
