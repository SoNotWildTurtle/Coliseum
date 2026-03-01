# Project State Analysis

- Generated (UTC): `2026-02-11T19:04:32+00:00`
- Python modules (`hololive_coliseum`): 218
- Test modules (`tests/test_*.py`): 136
- Auto-dev modules: 48
- Module docstring ratio: 100.0%

## Largest Core Modules

- `hololive_coliseum/game.py`: 7107 lines
- `hololive_coliseum/auto_dev_pipeline.py`: 3025 lines
- `hololive_coliseum/game_mmo_ui.py`: 2340 lines
- `hololive_coliseum/player.py`: 2138 lines
- `hololive_coliseum/menus.py`: 2099 lines
- `hololive_coliseum/auto_dev_intelligence_manager.py`: 2081 lines
- `hololive_coliseum/game_mmo_logic.py`: 1789 lines
- `hololive_coliseum/network.py`: 1095 lines
- `hololive_coliseum/world_generation_manager.py`: 848 lines
- `hololive_coliseum/auto_dev_codebase_analyzer.py`: 845 lines

## Largest Test Modules

- `tests/test_game.py`: 914 lines
- `tests/test_player.py`: 809 lines
- `tests/test_arena_fun_balancing.py`: 572 lines
- `tests/test_auto_dev_pipeline.py`: 520 lines
- `tests/test_network.py`: 486 lines
- `tests/test_world_generation_manager.py`: 450 lines
- `tests/test_mmo_logic_mixin.py`: 343 lines
- `tests/test_auto_dev_intelligence_manager.py`: 341 lines
- `tests/test_blockchain.py`: 258 lines
- `tests/test_hazards.py`: 252 lines

## Directory Footprint

- `hololive_coliseum`: 441 files, 4.90 MB
- `tests`: 400 files, 3.80 MB
- `docs`: 11 files, 0.46 MB
- `tools`: 12 files, 0.09 MB
- `Images`: 148 files, 0.28 MB
- `asset_pack`: 2 files, 0.00 MB
- `sounds`: 1 files, 0.00 MB
- `SavedGames`: 251 files, 29.04 MB

## Runtime Save Snapshot

- JSON save files: 9
- SQLite-related files: 1
- Iteration snapshots (`.gguf`): 239
- SavedGames total size: 29.04 MB

## Pygame Test Audit

- Tests referencing pygame: 40
- Tests missing importorskip: 0

## TODO Snapshot

- TODOs in modules/tests: 0

## README Alignment Notes

- The roster is seeded from `docs/DEV_PLAN_CHARACTERS.md`, but the selection
  list is backfilled from `CHARACTER_CLASSES` up to 20 entries, so the final
  roster is not strictly sourced from the plan file when that list is short.

## Key Observations

- Test-file to module ratio is 0.62; coverage breadth is strong.
- Largest implementation hotspots: hololive_coliseum/game.py,
  hololive_coliseum/auto_dev_pipeline.py, hololive_coliseum/game_mmo_ui.py.
- SavedGames contains many iteration snapshots; archive old `.gguf` files.
