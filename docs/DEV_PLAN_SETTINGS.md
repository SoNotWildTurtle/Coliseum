# Settings Menu Development Plan

The settings menu will allow players to customize their experience. Key areas:

- **Key Bindings**: Rebind actions such as jump, shoot, melee, and special attack.
- Managed through a `KeybindManager` so bindings can be saved and loaded.
- **Window Size**: Toggle between common resolutions or allow direct input.
- **Volume Control**: Adjust master volume for sounds and music.
- **Save Management**: Provide a button to wipe all files inside `SavedGames/`.
- **Account Management**: Register or delete the current user account.
- **Background Mining**: Toggle a 20% CPU proof-of-work helper that evolves the
  MMO world. The menu explains the higher resource usage when enabled.
- **Accessibility**: Toggle colorblind mode via `AccessibilityManager`.
- **Persistence**: Changes persist across sessions via `settings.json`.

Current prototype implements these features with a dedicated key-binding menu
and volume adjustments using the arrow keys.
