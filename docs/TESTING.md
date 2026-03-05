# Testing Guide

This repository favors small, fast unit tests with optional Pygame coverage.
Use these steps to keep local runs consistent and reviews easy.

## Quick start

```
pytest -q
```

## Pygame and headless runs

- Pygame tests call `pytest.importorskip("pygame")` to skip cleanly.
- Headless CI or terminal runs should set `SDL_VIDEODRIVER=dummy`.
- If you are on Windows, PowerShell supports `setx` or `$env:SDL_VIDEODRIVER`.

## Targeted test runs

Run only a subset while iterating:

```
pytest -q tests/test_game.py
pytest -q tests/test_level_manager.py
pytest -q tests/test_hud_manager.py
```

## Gameplay smoke checks

These are manual checks when changing menus or gameplay UX:

- Start the game and visit main menu, settings, character select, and map select.
- Enter a story chapter and ensure hazards/platforms spawn correctly.
- Use the MMO hub to confirm overlays render and map layers toggle.

## UI smoke runner

Run the headless UI smoke runner for deterministic menu/HUD/MMO checks:

```
python -m hololive_coliseum.tools.ui_smoke_runner --res 1280x720 --font-scale 1.0 --mode menu --frames 30
```

Stress config (useful for overflow/collision checks with UI debug logging):

```
python -m hololive_coliseum.tools.ui_smoke_runner --res 1024x576 --font-scale 1.25 --mode all --frames 60 --ui-debug
```

## MMO hub checklist

Use this when touching MMO hub logic, flow, or UI:

- Enter the MMO hub and confirm the regions list renders without errors.
- Change sort modes and biome filter; confirm ordering changes.
- Open Help and Tour overlays; confirm text renders and navigation works.
- Use Waypoint set/clear actions; confirm log messages appear.
- Create a trade route and dispatch an operation; confirm status appears in lists.
- Assign a patrol to a region; confirm the patrol entry shows the assignment.
- Post and cancel a market order; confirm expiration/cancel status appears.
- Let MMO time advance; confirm contracts/operations tick down and complete.

## Docs and analysis regeneration

When features change, refresh the analysis and graph outputs:

```
python tools/generate_codebase_analysis.py
python tools/generate_codebase_graphs.py
python tools/analyze_project_state.py
```

For a visible autoplay demo run:

```
python tools/run_autoplay_demo.py --mode flow
python tools/run_autoplay_demo.py --mode agent
python tools/run_autoplay_demo.py --mode flow --mmo
python tools/run_autoplay_demo.py --mode agent --full
```
