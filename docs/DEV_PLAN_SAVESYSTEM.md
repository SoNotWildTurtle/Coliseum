# Save System Notes

The game stores configuration data inside the `SavedGames/` directory.
The `save_manager` module provides helpers for loading and saving settings.
Future updates will add player progress and unlocks. Inventory contents are now
saved to `inventory.json` so items persist between sessions.
The save manager now recreates the directory automatically if it has been removed.
