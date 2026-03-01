# Codebase Analysis

Manual notes can live outside the auto-generated section below.

<!-- AUTO-GENERATED:codebase-analysis:start -->
## How to Regenerate

```bash
python tools/generate_codebase_analysis.py
python tools/generate_codebase_graphs.py
```

## Entry Points

- `main.py` -> `hololive_coliseum.game.main()`
- `python -m hololive_coliseum` -> `hololive_coliseum.game.main()`

## High-Level Pipelines

### Game Runtime Loop

- `Game.__init__` configures managers, loads settings, and builds menus.
- `LevelManager.setup_level` instantiates player/enemies and map objects.
- `Game.run` handles menu state, input, AI, collisions, HUD, saves.

### Asset Pipeline

- `placeholder_sprites.ensure_placeholder_sprites` writes missing PNGs.
- `game._load` loads images or falls back to an in-memory icon surface.

### Save/Load Pipeline

- `save_manager.load_settings/load_inventory` read JSON from `SavedGames`.
- `save_manager.save_settings/save_inventory` persist state on exit.
- `wipe_saves` removes files under `SavedGames`.

### Auto-Dev Pipeline

- `auto_dev_*` managers feed `AutoDevPipeline` and HUD summaries.
- `WorldGenerationManager.generate_region_from_seed` composes MMO metadata.

### Networking and State Sync

- `network.NetworkManager` handles sockets and relay state.
- `node_registry` and `state_sync` store shared state snapshots.

## Module Inventory

### `hololive_coliseum\__init__.py`

- docstring: Hololive Coliseum game package.
- imports:
  - .accessibility_manager
  - .accounts
  - .achievement_manager
  - .ad_manager
  - .ai_manager
  - .ai_moderation_manager
  - .ally_manager
  - .animation_manager
  - .api_manager
  - .appearance_manager
  - .arena_ai_player
  - .arena_manager
  - .auth_manager
  - .auto_balancer
  - .auto_dev_boss_manager
  - .auto_dev_creation_manager
  - .auto_dev_design_manager
  - .auto_dev_evolution_manager
  - .auto_dev_feedback_manager
  - .auto_dev_focus_manager
  - .auto_dev_guidance_manager
  - .auto_dev_innovation_manager
  - .auto_dev_intelligence_manager
  - .auto_dev_mob_ai_manager
  - .auto_dev_modernization_manager
  - .auto_dev_monster_manager
  - .auto_dev_network_manager
  - .auto_dev_optimization_manager
  - .auto_dev_projection_manager
  - .auto_dev_quest_manager
  - .auto_dev_research_manager
  - .auto_dev_roadmap_manager
  - .auto_dev_scenario_manager
  - .auto_dev_self_evolution_manager
  - .auto_dev_spawn_manager
  - .auto_dev_synthesis_manager
  - .auto_dev_systems_manager
  - .auto_dev_tuning_manager
  - .auto_skill_manager
  - .ban_manager
  - .billing_manager
  - .blockchain
  - .bot_manager
  - .buff_manager
  - .camera_manager
  - .chat_manager
  - .cheat_detection_manager
  - .class_generator
  - .class_manager
  - .cluster_manager
  - .combat_manager
  - .companion_manager
  - .crafting_manager
  - .crafting_station
  - .currency_manager
  - .daily_task_manager
  - .damage_manager
  - .damage_number
  - .data_protection_manager
  - .device_manager
  - .distributed_state_manager
  - .dungeon_manager
  - .dynamic_content_manager
  - .economy_manager
  - .effect_manager
  - .emote_manager
  - .environment_manager
  - .equipment_manager
  - .event_manager
  - .event_modifier_manager
  - .experience_manager
  - .friend_manager
  - .game
  - .game_state_manager
  - .gathering_manager
  - .geo_manager
  - .goal_analysis_manager
  - .gravity_zone
  - .guild_manager
  - .hazard_manager
  - .hazards
  - .healing_zone
  - .health_manager
  - .holographic_compression
  - .housing_manager
  - .hud_manager
  - .input_manager
  - .instance_manager
  - .interaction_generator
  - .interaction_manager
  - .inventory_manager
  - .item_manager
  - .iteration_manager
  - .keybind_manager
  - .level_manager
  - .leveling_manager
  - .load_balancer_manager
  - .localization_manager
  - .logging_manager
  - .loot_manager
  - .mail_manager
  - .mana_manager
  - .map_manager
  - .matchmaking_manager
  - .melee_attack
  - .menu_manager
  - .migration_manager
  - .minigame_manager
  - .mining_manager
  - .mmo_builder
  - .mount_manager
  - .name_manager
  - .network
  - .node_manager
  - .node_registry
  - .notification_manager
  - .npc_manager
  - .objective_manager
  - .onboarding_manager
  - .party_manager
  - .patch_manager
  - .pet_manager
  - .platform
  - .player
  - .powerup
  - .profession_manager
  - .projectile
  - .quest_manager
  - .raid_manager
  - .recursive_generator
  - .replay_manager
  - .reputation_manager
  - .resource_manager
  - .save_manager
  - .score_manager
  - .screenshot_manager
  - .script_manager
  - .season_manager
  - .session_manager
  - .shared_state_manager
  - .skill_generator
  - .skill_manager
  - .sound_manager
  - .spawn_manager
  - .stamina_manager
  - .state_sync
  - .state_verification_manager
  - .stats_manager
  - .status_effects
  - .story_maps
  - .subclass_generator
  - .support_manager
  - .sync_manager
  - .team_manager
  - .telemetry_manager
  - .threat_manager
  - .title_manager
  - .tournament_manager
  - .trade_manager
  - .trade_skill_crafting_manager
  - .trade_skill_generator
  - .transmission_manager
  - .tutorial_manager
  - .ui_manager
  - .voice_chat_manager
  - .voting_manager
  - .war_manager
  - .weather_forecast_manager
  - .weekly_manager
  - .world_generation_manager
  - .world_player_manager
  - .world_region_manager
  - .world_seed_manager
- globals:
  - __all__
- classes:
  - (none)
- functions:
  - (none)

### `hololive_coliseum\__main__.py`

- docstring: Package entry point for `python -m hololive_coliseum`.
- imports:
  - .game
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - (none)

### `hololive_coliseum\accessibility_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - AccessibilityManager (bases: (none))
    doc: Store toggles for accessibility features.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - toggle(self, name) -> None
- functions:
  - (none)

### `hololive_coliseum\accounts.py`

- docstring: User account registry storing public keys and access levels.
- imports:
  - __future__
  - cryptography.hazmat.primitives
  - cryptography.hazmat.primitives.asymmetric
  - json
  - os
  - typing
- globals:
  - ACCOUNTS_FILE
  - KEY_FILE_FMT
  - SAVE_DIR
  - _DEFAULT_MANAGER
- classes:
  - AccountsManager (bases: (none))
    doc: Manage user accounts stored in ``accounts.json``.
    class_vars:
      - (none)
    methods:
      - __init__(self, path) -> None
      - load(self) -> Dict[str, Dict[str, str]]
      - save(self, data) -> None
      - register(self, user_id, level, public_key_pem) -> None
      - delete(self, user_id) -> None
      - get(self, user_id) -> Dict[str, str] | None
      - renew_key(self, user_id) -> bytes
- functions:
  - _load_json(path, default) -> Any
  - _save_json(path, data) -> None
  - load_accounts() -> Dict[str, Dict[str, str]]
  - save_accounts(data) -> None
  - register_account(user_id, level, public_key_pem) -> None
  - delete_account(user_id) -> None
  - get_account(user_id) -> Dict[str, str] | None
  - renew_key(user_id) -> bytes
  - load_private_key(user_id) -> bytes | None

### `hololive_coliseum\achievement_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - AchievementManager (bases: (none))
    doc: Record unlocked achievements.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - unlock(self, name) -> None
      - is_unlocked(self, name) -> bool
      - to_dict(self) -> dict
      - load_from_dict(self, data) -> None
- functions:
  - (none)

### `hololive_coliseum\ad_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - AdManager (bases: (none))
    doc: Manage in-game advertisements and promotions.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_ad(self, text) -> None
      - current_ads(self) -> list[str]
- functions:
  - (none)

### `hololive_coliseum\ai_autoplayer.py`

- docstring: Adaptive autoplay agent that steers the local player during runs.
- imports:
  - __future__
  - dataclasses
  - pygame
  - random
  - typing
- globals:
  - (none)
- classes:
  - AutoPlayerTuning (bases: (none))
    doc: Tune aggression and reactions for the autoplay agent.
    class_vars:
      - aggression
      - caution
      - desired_range
      - dodge_bias
      - melee_range
      - shoot_range
      - special_chance
      - strafe_chance
    methods:
      - from_dict(cls, data) -> 'AutoPlayerTuning'
      - to_dict(self) -> dict[str, float | int]
      - clamp(self) -> None
  - KeyState (bases: (none))
    doc: Lightweight key state wrapper for simulated input.
    class_vars:
      - (none)
    methods:
      - __init__(self, pressed) -> None
      - __getitem__(self, key) -> bool
  - _AutoTarget (bases: (none))
    doc: Tiny target wrapper for exploration goals.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, name) -> None
  - AutoPlayer (bases: (none))
    doc: Generate basic input decisions for the local player.
    class_vars:
      - (none)
    methods:
      - __init__(self, game, tuning) -> None
      - inputs(self, now) -> tuple[KeyState, Callable[[str], bool]]
      - update_feedback(self, damage_taken, kills, health_ratio, elapsed_ms) -> None
      - tuning_snapshot(self) -> dict[str, float | int]
      - _nearest_enemy(self, player, enemies)
      - _apply_difficulty_bias(self, now, threat_ratio) -> None
      - _lerp(current, target, weight) -> float
      - _select_target(self, player, enemies)
      - _select_goal_target(self, player, target, powerups, now, threat)
      - _incoming_projectile(self, player, projectiles) -> bool
      - _hazard_ahead(self, player) -> bool
      - _maybe_jump(self, actions, now) -> None
      - _near_enemy(self, player, target) -> bool
      - _move_toward_target(self, player, target, pressed_keys, now) -> None
      - _move_toward_powerup(self, player, powerups, pressed_keys) -> None
      - _maybe_use_item(self, actions, player, now, threat_ratio) -> None
      - _maybe_use_mana(self, actions, player, now, threat_ratio) -> None
      - _stage_threat_ratio(self) -> float
      - _gap_or_edge_risk(self, player, world_width) -> bool
      - _avoid_edges(self, player, pressed_keys, world_width) -> None
      - _remember_target(self, name, distance) -> None
      - _maybe_set_explore_mode(self, now, player, hazards, platforms, world_width) -> None
      - _select_explore_target(self, player, hazards, platforms, world_width)
      - _maybe_force_feature_tests(self, actions, now, player) -> None
- functions:
  - _clamp(value, low, high) -> float

### `hololive_coliseum\ai_experience_manager.py`

- docstring: Track AI combat experiences and propose smarter next actions.
- imports:
  - __future__
  - dataclasses
  - math
  - typing
- globals:
  - (none)
- classes:
  - AgentExperience (bases: (none))
    doc: Stateful combat record for a single AI agent.
    class_vars:
      - actions
      - bias
      - engagements
      - last_action
      - last_damage_time
      - last_health
      - next_action
      - repeat_count
      - time_alive_ms
    methods:
      - (none)
  - AIExperienceManager (bases: (none))
    doc: Monitor AI agent outcomes and compute next-action hints.
    class_vars:
      - (none)
    methods:
      - __init__(self, experience_level) -> None
      - set_experience_level(self, level) -> None
      - record_action(self, agent, action) -> None
      - snapshot(self, agents) -> list[dict[str, Any]]
      - update_context(self, player, enemies, now, hazards, threat_level) -> None
      - _state(self, agent) -> AgentExperience
      - _plan_next_action(self, enemy, player, now, hazards, state, threat_level) -> tuple[str, dict[str, float]]
- functions:
  - (none)

### `hololive_coliseum\ai_experience_store.py`

- docstring: Persist AI experience snapshots for analysis across playthroughs.
- imports:
  - __future__
  - json
  - os
  - pathlib
  - time
  - typing
- globals:
  - (none)
- classes:
  - AIExperienceStore (bases: (none))
    doc: Append AI experience snapshots to disk for later review.
    class_vars:
      - (none)
    methods:
      - __init__(self, path) -> None
      - _load(self) -> None
      - _save(self) -> None
      - append_snapshot(self, snapshot) -> None
      - build_snapshot() -> dict[str, Any]
- functions:
  - (none)

### `hololive_coliseum\ai_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - AIManager (bases: (none))
    doc: Coordinate AI updates for enemy sprites.
    class_vars:
      - (none)
    methods:
      - __init__(self, enemies) -> None
      - update(self, player, now, hazards, projectiles)
- functions:
  - (none)

### `hololive_coliseum\ai_moderation_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - AIModerationManager (bases: (none))
    doc: Use simple rules to flag toxic chat messages.
    class_vars:
      - (none)
    methods:
      - __init__(self, banned_words)
      - check(self, message) -> bool
      - flagged(self)
- functions:
  - (none)

### `hololive_coliseum\ally_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - AllyManager (bases: (none))
    doc: Simple manager for friendly NPCs that follow the player.
    class_vars:
      - (none)
    methods:
      - __init__(self, allies) -> None
      - update(self, player, ground_y, now) -> None
- functions:
  - (none)

### `hololive_coliseum\animation_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - AnimationManager (bases: (none))
    doc: Track simple animation states and frames.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - set_state(self, state) -> None
      - update(self) -> None
- functions:
  - (none)

### `hololive_coliseum\api_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - APIManager (bases: (none))
    doc: Store webhook endpoints for third-party integrations.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_endpoint(self, name, url) -> None
      - get(self, name) -> str | None
- functions:
  - (none)

### `hololive_coliseum\appearance_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - AppearanceManager (bases: (none))
    doc: Store visual appearance selections for entities.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - set_skin(self, entity, skin) -> None
      - get_skin(self, entity) -> str | None
- functions:
  - (none)

### `hololive_coliseum\arena_ai_player.py`

- docstring: Background arena AI players used for fun balancing.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - ArenaAIPlayer (bases: (none))
    doc: Simple agent that scores arena states for fun balancing.  ``aggression`` favours faster paced matches, ``creativity`` rewards varied encounters, and ``teamwork`` values supportive play. ``preferred_archetypes`` highlights the playstyles this agent represents, while ``adaptability`` controls how much future projections drift from an initial evaluation. All numeric attributes are expected on ``[0.0, 1.0]`` and are automatically clamped at runtime.
    class_vars:
      - adaptability
      - aggression
      - creativity
      - name
      - preferred_archetypes
      - teamwork
    methods:
      - evaluate_arena(self, snapshot) -> float
      - playtest_arena(self, snapshot) -> Mapping[str, object]
- functions:
  - _clamp(value) -> float

### `hololive_coliseum\arena_manager.py`

- docstring: Arena orchestration utilities.
- imports:
  - .arena_ai_player
  - __future__
  - collections
  - dataclasses
  - math
  - typing
- globals:
  - (none)
- classes:
  - ArenaFunSnapshot (bases: (none))
    doc: Immutable snapshot of the arena fun telemetry.
    class_vars:
      - ai_projection
      - baseline_fun
      - fun_level
      - fun_momentum
    methods:
      - as_dict(self) -> dict[str, float]
  - ArenaFunReport (bases: (none))
    doc: Detailed fun telemetry emitted after background AI playtests.
    class_vars:
      - ai_consensus
      - ai_projection
      - baseline_fun
      - fun_level
      - fun_momentum
      - rounds_tested
      - volatility
    methods:
      - as_dict(self) -> dict[str, float]
  - ArenaFunForecast (bases: (none))
    doc: Forward-looking fun outlook based on background AI telemetry.
    class_vars:
      - ai_alignment
      - archetype_focus
      - expected_fun
      - recommended_focus
      - risk_band
      - volatility_band
    methods:
      - as_dict(self) -> dict[str, object]
  - ArenaFunDirective (bases: (none))
    doc: Recommendation describing how to tweak a specific class for fun gains.
    class_vars:
      - action
      - class_name
      - rationale
      - stat_bias
      - weight
    methods:
      - as_dict(self) -> dict[str, object]
  - ArenaFunTuningPlan (bases: (none))
    doc: Holistic fun plan derived from background AI telemetry.
    class_vars:
      - ai_alignment
      - archetype_focus
      - baseline_fun
      - baseline_shift
      - directives
      - focus
      - fun_momentum
      - target_fun
      - volatility
    methods:
      - as_dict(self) -> dict[str, object]
  - ArenaFunSeasonSummary (bases: (none))
    doc: Summary describing how background AI matches influenced fun.
    class_vars:
      - ai_participation
      - ai_projection
      - baseline_fun
      - fun_momentum
      - highlighted_archetypes
      - rounds_played
      - season_fun
      - win_leaders
    methods:
      - as_dict(self) -> dict[str, object]
  - ArenaManager (bases: (none))
    doc: Handle PvP arena rankings, fun tracking, and AI-driven balancing.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - record_win(self, player) -> None
      - record_match_feedback(self, player, fun_rating) -> float
      - simulate_background_balancing(self, arena_snapshot) -> float
      - get_ai_feedback(self) -> dict[str, float]
      - calibrate_fun_baseline(self) -> float
      - capture_fun_snapshot(self) -> ArenaFunSnapshot
      - get_fun_momentum(self) -> float
      - run_ai_playtests(self, snapshots) -> ArenaFunReport
      - generate_fun_report(self, rounds_tested) -> ArenaFunReport
      - generate_fun_forecast(self) -> ArenaFunForecast
      - generate_fun_tuning_plan(self, classes) -> ArenaFunTuningPlan
      - get_ai_archetype_focus(self, limit) -> tuple[str, ...]
      - _build_season_summary(self, matches, participation_rate) -> ArenaFunSeasonSummary
      - _top_ai_wins(self, limit) -> tuple[tuple[str, int], ...]
      - simulate_ai_matches(self, snapshots) -> ArenaFunSeasonSummary
      - reset_ai_season(self) -> None
      - get_ai_season_wins(self) -> dict[str, int]
      - _extract_scalar(source, key, default) -> object | None
      - _build_fun_directives(self, ai_feedback) -> list[ArenaFunDirective]
      - _derive_stat_bias(action, focus, stats) -> tuple[tuple[str, float], ...]
      - _update_baseline(self, weight) -> None
      - _refresh_momentum(self) -> None
      - _record_consensus(self, value) -> None
      - _calculate_volatility(self) -> float
      - _record_archetypes(self, archetypes) -> None
      - top_player(self) -> str | None
- functions:
  - _clamp(value) -> float

### `hololive_coliseum\asset_pack.py`

- docstring: Resolve asset pack paths and folders for sprite loading.
- imports:
  - __future__
  - os
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - resolve_asset_dir() -> str
  - ensure_asset_dirs(asset_dir) -> None
  - asset_path(asset_dir, category, base, direction) -> str

### `hololive_coliseum\auth_manager.py`

- docstring: Authentication helper storing salted password hashes and expiring tokens.
- imports:
  - __future__
  - hashlib
  - secrets
  - time
  - typing
- globals:
  - (none)
- classes:
  - AuthManager (bases: (none))
    doc: Handle account credentials with hashed passwords and login limits.
    class_vars:
      - (none)
    methods:
      - __init__(self, max_attempts, token_lifetime, time_func) -> None
      - _hash(password, salt) -> str
      - register(self, username, password) -> None
      - login(self, username, password) -> str | None
      - verify(self, token) -> bool
      - logout(self, token) -> None
- functions:
  - (none)

### `hololive_coliseum\auto_balancer.py`

- docstring: Automatically balance class statistics.
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - AutoBalancer (bases: (none))
    doc: Adjust class stat dictionaries toward the average.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - balance(self, classes) -> dict[str, dict[str, float]]
- functions:
  - _clamp(value) -> float

### `hololive_coliseum\auto_dev_blueprint_manager.py`

- docstring: Blueprint orchestration for functionality and mechanics planning.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevBlueprintManager (bases: (none))
    doc: Synthesise creation, functionality, and mechanics insights into blueprints.
    class_vars:
      - creation_weight
      - functionality_weight
      - gap_penalty_factor
      - mechanics_weight
      - risk_penalty_factor
      - synthesis_weight
    methods:
      - blueprint_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _clamp(value, minimum, maximum) -> float
  - _unique_strings() -> tuple[str, ...]
  - _priority(score, gap_index) -> str
  - _merge_network_requirements(functionality, creation, systems, design, network, security, modernization) -> dict[str, Any]
  - _merge_holographic_requirements(functionality, creation, systems, design, transmission) -> dict[str, Any]

### `hololive_coliseum\auto_dev_boss_manager.py`

- docstring: Determine boss encounters for the auto-development pipeline.
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - AutoDevBossManager (bases: (none))
    doc: Select thematic bosses based on monster and roadmap data.
    class_vars:
      - (none)
    methods:
      - select_boss(self, monsters) -> dict[str, Any]
      - _enrage_condition(self, projection, monster) -> str
      - _strategies(self, monster, threat) -> tuple[str, ...]
      - _spawn_support(self, spawn_plan, monster) -> dict[str, Any]
      - _phase_transitions(self, threat, spawn_plan, projection) -> dict[str, Any]
      - _trade_hooks(self, trade_skills, monster) -> tuple[str, ...]
- functions:
  - (none)

### `hololive_coliseum\auto_dev_codebase_analyzer.py`

- docstring: Analyse auto-dev modules to highlight weak areas and mitigation steps.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevCodebaseAnalyzer (bases: (none))
    doc: Provide a deterministic assessment of codebase health signals.
    class_vars:
      - complexity_threshold
      - min_test_ratio
      - warning_threshold
    methods:
      - evaluate(self, modules, tests) -> dict[str, Any]
      - _instability_index(self, complexities, incidents) -> float
      - _weakness_signals(self, complexities, test_flags, docstring_flags, incidents) -> list[str]
      - _mitigation_plan(self, weakness_signals, docstring_ratio, test_ratio, instability_index) -> list[str]
      - _debt_profile(self, complexities, test_flags, docstring_flags, incidents, instability_index) -> dict[str, Any]
      - _stability_outlook(self, instability_index, missing_tests, incidents, high_complexity) -> str
      - _module_scorecards(self, modules, complexities, test_flags, docstring_flags, incidents) -> list[dict[str, Any]]
      - _module_label(self, module, index) -> str
      - _functionality_gaps(self, modules, complexities, test_flags, docstring_flags, total_modules) -> tuple[float, list[str]]
      - _mechanics_alignment_score(self, functionality_gap_index, instability_index) -> float
      - _design_fragility(self, modules, functionality_gaps, scorecards, modernization_targets) -> tuple[float, list[str], list[str]]
      - _systems_fragility(self, modules, functionality_gap_index, mechanics_alignment_score, design_fragility_index, debt_profile, modernization_targets) -> tuple[float, list[str], list[str], float]
      - _modernization_targets(self, scorecards, debt_profile, mitigation_plan) -> list[dict[str, Any]]
- functions:
  - _as_float(value, default) -> float
  - _bool(value) -> bool
  - _count_flags(values) -> int
  - _missing_indices(flags) -> tuple[int, ...]
  - _risk_level(score) -> str

### `hololive_coliseum\auto_dev_continuity_manager.py`

- docstring: Long-range continuity planning for the auto-dev orchestration.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevContinuityManager (bases: (none))
    doc: Synthesize continuity, security, and holographic guidance.
    class_vars:
      - horizon_days
      - mid_window_days
      - short_window_days
    methods:
      - continuity_plan(self) -> dict[str, Any]
      - _timeline(self, priority, mitigation_priority, network_security_score, debt_risk, guardrail_severity, grade, module_progress) -> list[dict[str, Any]]
      - _continuity_index(self, network_security_score, resilience_index, debt_risk, mitigation_score) -> float
      - _continuity_risks(self, network_security_score, debt_risk, guardrail_severity, research_penalty, codebase_outlook) -> dict[str, Any]
      - _holographic_actions(self, guardrails, enhancements, diagnostics, lithographic) -> dict[str, Any]
      - _network_security_playbooks(self, security_auto_dev, upgrades, backlog) -> list[dict[str, Any]]
      - _codebase_continuity_actions(self, codebase, progress, mitigation_tasks) -> dict[str, Any]
      - _managerial_overwatch(self, guidance, resilience_overwatch, continuity_index) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _normalise_strings(values) -> list[str]

### `hololive_coliseum\auto_dev_convergence_manager.py`

- docstring: Convergence manager that aligns creation, functionality, and mechanics planning.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevConvergenceManager (bases: (none))
    doc: Blend functionality, mechanics, and creation telemetry into convergence briefs.
    class_vars:
      - creation_weight
      - design_weight
      - dynamics_weight
      - experience_weight
      - functionality_weight
      - gap_penalty_factor
      - holographic_bonus_factor
      - innovation_weight
      - mechanics_weight
      - network_bonus_factor
      - research_bonus_factor
      - risk_penalty_factor
      - synthesis_weight
      - systems_weight
    methods:
      - convergence_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _clamp(value, minimum, maximum) -> float
  - _normalise_strings(values) -> tuple[str, ...]
  - _merge_network_requirements() -> dict[str, Any]
  - _merge_holographic_requirements(transmission) -> dict[str, Any]
  - _priority(score, risk_index, gap_index) -> str
  - _merge_threads() -> tuple[str, ...]
  - _merge_actions() -> tuple[str, ...]
  - _cohesion_index() -> float

### `hololive_coliseum\auto_dev_creation_manager.py`

- docstring: Blend functionality and mechanics telemetry into creation blueprints.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevCreationManager (bases: (none))
    doc: Combine auto-dev signals into actionable creation briefs.
    class_vars:
      - alignment_weight
      - design_weight
      - experience_weight
      - functionality_weight
      - gap_penalty_factor
      - innovation_weight
      - mechanics_weight
      - risk_penalty_factor
      - systems_weight
    methods:
      - creation_blueprint(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _clamp(value, minimum, maximum) -> float
  - _normalise_strings(values) -> tuple[str, ...]
  - _priority(score, gap_index, risk_index) -> str
  - _merge_network_requirements() -> dict[str, Any]
  - _merge_holographic_requirements(transmission) -> dict[str, Any]
  - _concept_portfolio(functionality, innovation, gameplay) -> tuple[dict[str, Any], ...]
  - _prototype_requirements(design, functionality, modernization, optimization) -> tuple[dict[str, Any], ...]

### `hololive_coliseum\auto_dev_design_manager.py`

- docstring: Blend functionality and mechanics signals into actionable design blueprints.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevDesignManager (bases: (none))
    doc: Fuse functionality, mechanics, and networking signals into design briefs.
    class_vars:
      - dynamics_weight
      - experience_weight
      - fragility_penalty_factor
      - functionality_weight
      - gameplay_weight
      - innovation_weight
      - interaction_weight
      - mechanics_weight
      - network_bonus_factor
      - risk_penalty_factor
    methods:
      - design_blueprint(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _clamp(value, minimum, maximum) -> float
  - _priority(score) -> str
  - _normalise_strings(values) -> tuple[str, ...]
  - _merge_requirements() -> dict[str, Any]
  - _merge_holographic_requirements(transmission) -> dict[str, Any]

### `hololive_coliseum\auto_dev_dynamics_manager.py`

- docstring: Assess cross-domain system dynamics for the auto-dev workflow.
- imports:
  - __future__
  - dataclasses
  - itertools
  - typing
- globals:
  - (none)
- classes:
  - AutoDevDynamicsManager (bases: (none))
    doc: Blend functionality, mechanics, and network data into systems dynamics.
    class_vars:
      - experience_weight
      - functionality_weight
      - innovation_weight
      - integrity_weight
      - mechanics_weight
      - network_weight
      - resilience_weight
      - risk_penalty_factor
      - security_weight
    methods:
      - dynamics_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _as_mapping(value) -> Mapping[str, Any]
  - _normalise_strings(values) -> tuple[str, ...]
  - _unique_from_sources() -> tuple[str, ...]
  - _clamp(value, minimum, maximum) -> float
  - _priority(score, risk) -> str
  - _threat_modifier(level) -> float

### `hololive_coliseum\auto_dev_evolution_manager.py`

- docstring: Synthesize auto-dev signals into actionable evolution plans.
- imports:
  - __future__
  - statistics
  - typing
- globals:
  - (none)
- classes:
  - AutoDevEvolutionManager (bases: (none))
    doc: Create evolution roadmaps from auto-dev guidance and telemetry.
    class_vars:
      - (none)
    methods:
      - __init__(self, horizon) -> None
      - evolution_brief(self) -> dict[str, Any]
      - _utilisation_percent(self, guidance, research) -> float
      - _objectives(self, guidance, roadmap, focus, quests) -> Iterable[str]
      - _resource_focus(self, utilisation, spawn_state, quests) -> dict[str, Any]
      - _confidence(self, guidance, roadmap, focus, research, monsters, spawn_plan, quests) -> float
      - _summary(self, guidance, threat_tier, spawn_state) -> str
- functions:
  - _threat_summary(monsters) -> tuple[str, float]
  - _spawn_pressure(plan) -> str

### `hololive_coliseum\auto_dev_execution_manager.py`

- docstring: Blend implementation readiness into execution orchestration telemetry.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevExecutionManager (bases: (none))
    doc: Fuse implementation, convergence, and guardrail telemetry into execution briefs.
    class_vars:
      - (none)
    methods:
      - execution_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _clamp(value, minimum, maximum) -> float
  - _normalise_strings(values) -> list[str]
  - _merge_network_requirements() -> dict[str, Any]
  - _merge_holographic_requirements(transmission) -> dict[str, Any]
  - _threat_penalty(level) -> float
  - _priority(score, gap_index, risk_index) -> str
  - _stability_state(score, risk_index, resilience_score, continuity_percent) -> str
  - _velocity_index(implementation_velocity, applied_fixes, scheduled_fixes, continuity_windows) -> float
  - _execution_tracks(implementation_tracks, convergence_tracks, creation_tracks, gameplay_loops, systems_threads) -> tuple[str, ...]
  - _execution_actions(implementation_actions, convergence_actions, creation_actions, gameplay_actions, mitigation_tasks, continuity_actions) -> tuple[str, ...]
  - _execution_windows(implementation_windows, continuity_timeline) -> tuple[str, ...]
  - _execution_backlog(implementation_backlog, continuity_actions) -> tuple[dict[str, Any], ...]
  - _debt_penalty(risk_score) -> float

### `hololive_coliseum\auto_dev_experience_manager.py`

- docstring: Experience design synthesis for the Coliseum auto-dev pipeline.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevExperienceManager (bases: (none))
    doc: Blend mechanics, innovation, and governance data into experience arcs.
    class_vars:
      - cohesion_weight
      - novelty_weight
      - risk_weight
      - systems_weight
    methods:
      - experience_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _normalise_strings(values) -> tuple[str, ...]
  - _priority_value(priority) -> float
  - _threat_penalty(threat) -> float
  - _experience_priority(score) -> str
  - _window_strings(timeline) -> tuple[str, ...]
  - _concepts(concepts) -> tuple[Mapping[str, Any], ...]

### `hololive_coliseum\auto_dev_feedback_manager.py`

- docstring: Collect Coliseum match telemetry to guide MMO auto-development.
- imports:
  - __future__
  - collections
  - json
  - os
  - pathlib
  - typing
- globals:
  - (none)
- classes:
  - AutoDevFeedbackManager (bases: (none))
    doc: Record arena feedback and surface insights for MMO generation.
    class_vars:
      - (none)
    methods:
      - __init__(self, path, max_history) -> None
      - _load(self) -> None
      - _save(self) -> None
      - start_match(self, character, map_name) -> None
      - record_hazard(self, hazard_type) -> None
      - finalize(self, result, score, duration, account) -> dict[str, Any]
      - get_trending_hazard(self) -> str | None
      - get_favorite_character(self) -> str | None
      - get_average_score(self) -> float
      - get_average_duration(self) -> float
      - hazard_challenge(self, base_target) -> dict[str, object] | None
      - estimate_recommended_level(self, base_level) -> int
      - region_insight(self) -> dict[str, Any]
- functions:
  - (none)

### `hololive_coliseum\auto_dev_focus_manager.py`

- docstring: Synthesize MMO auto-dev focus areas from existing insights.
- imports:
  - __future__
  - collections.abc
  - typing
- globals:
  - (none)
- classes:
  - AutoDevFocusManager (bases: (none))
    doc: Calculate sprint focus priorities from auto-development data.
    class_vars:
      - (none)
    methods:
      - __init__(self, max_focus, history_limit) -> None
      - analyse(self) -> Dict[str, Any]
      - recent_focus(self) -> List[Dict[str, Any]]
      - latest(self) -> Dict[str, Any] | None
      - _clone(self, entry) -> Dict[str, Any]
      - _build_priorities(self, scoreboard) -> List[Dict[str, Any]]
      - _build_context(self) -> Dict[str, Any]
      - _extract_projection_focus(self, projection) -> Iterable[Dict[str, Any]]
- functions:
  - _clean_hazard(value) -> str

### `hololive_coliseum\auto_dev_functionality_manager.py`

- docstring: Assemble functionality expansion briefs for the auto-dev workflow.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevFunctionalityManager (bases: (none))
    doc: Blend mechanics, innovation, and experience data into functionality briefs.
    class_vars:
      - experience_weight
      - innovation_weight
      - novelty_weight
      - resilience_weight
      - risk_penalty_factor
    methods:
      - functionality_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _normalise_strings(values) -> tuple[str, ...]
  - _timeline_windows(timeline) -> tuple[str, ...]
  - _priority_from_score(score) -> str

### `hololive_coliseum\auto_dev_gameplay_manager.py`

- docstring: Synthesize functionality, dynamics, and playstyle data into gameplay loops.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevGameplayManager (bases: (none))
    doc: Blend functionality, dynamics, and playstyle data into gameplay loops.
    class_vars:
      - dynamics_weight
      - experience_weight
      - functionality_weight
      - innovation_weight
      - mechanics_weight
      - playstyle_weight
      - resilience_bonus_factor
      - risk_penalty_factor
    methods:
      - gameplay_blueprint(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _normalise_strings(values) -> tuple[str, ...]
  - _priority(score) -> str
  - _archetype_label(data, index) -> str

### `hololive_coliseum\auto_dev_governance_manager.py`

- docstring: Blend managerial intelligence signals into an actionable governance brief.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevGovernanceManager (bases: (none))
    doc: Convert pipeline telemetry into backend governance directives.
    class_vars:
      - baseline_score
      - debt_penalty_scale
      - holographic_threshold
    methods:
      - governance_brief(self) -> dict[str, Any]
      - _oversight_score(self, network_security, projected_security, alignment, continuity_percent, resilience_score, debt_risk, holographic_score, threat_level) -> float
      - _oversight_actions(self, network_security, threat_level, debt_risk, holographic_score, network_tasks, guardrail_actions) -> tuple[str, ...]
      - _risk_flags(self, network_security, threat_level, debt_risk, continuity_percent, governance_outlook) -> tuple[str, ...]
      - _codebase_directives(self, modernization_targets) -> tuple[dict[str, Any], ...]
      - _holographic_directives(self, guardrails, waveform, adjustments) -> tuple[str, ...]
      - _managerial_backlog(self, codebase_tasks, network_tasks, continuity_actions) -> tuple[str, ...]
- functions:
  - _as_float(value, default) -> float
  - _normalise_actions(values) -> tuple[str, ...]
  - _threat_modifier(threat) -> float
  - _governance_state(score) -> str

### `hololive_coliseum\auto_dev_guidance_manager.py`

- docstring: Provide managerial guidance that links all auto-dev insights together.
- imports:
  - __future__
  - statistics
  - typing
- globals:
  - (none)
- classes:
  - AutoDevGuidanceManager (bases: (none))
    doc: Fuse encounter, quest and research data into executive guidance.
    class_vars:
      - (none)
    methods:
      - __init__(self, threat_weight, processing_weight) -> None
      - compose_guidance(self) -> dict[str, Any]
      - _risk(self, threat, spawn_danger, utilisation, network_signal) -> float
      - _directives(self, monsters, mob_ai, boss_plan, quests) -> Iterable[str]
      - _priority(self, risk_index) -> str
      - _insight_chain(self, mob_ai, quests, boss_plan) -> list[str]
      - _network_signal(self, network) -> float
      - _intelligence_rating(self, risk_index, network_signal, quests) -> str
      - _managerial_threads(self, monsters, spawn_plan, mob_ai, boss_plan, quests, research, network) -> tuple[str, ...]
      - _self_evolution_vector(self, risk_index, research, mob_ai, network) -> dict[str, Any]
      - _intelligence_score(self, risk_index, network_signal, quests, research, network) -> float
      - _backend_guidance_vector(self, research, network, directives, risk_index) -> tuple[str, ...]
      - _governance_outlook(self, intelligence_score, priority) -> str
      - _intelligence_breakdown(self, risk_index, network_signal, utilisation, research, quests, network) -> dict[str, Any]
      - _backend_alignment_score(self, risk_index, network_signal, utilisation, research, network) -> float
      - _guidance_backbone(self, threads, directives, breakdown) -> tuple[str, ...]
- functions:
  - _average_threat(monsters) -> float
  - _spawn_pressure(plan) -> float
  - _processing_percent(research) -> float

### `hololive_coliseum\auto_dev_implementation_manager.py`

- docstring: Translate functionality and creation telemetry into implementation briefs.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevImplementationManager (bases: (none))
    doc: Fuse functionality, creation, and convergence data into implementation plans.
    class_vars:
      - convergence_weight
      - creation_weight
      - design_weight
      - functionality_weight
      - systems_weight
    methods:
      - implementation_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _clamp(value, minimum, maximum) -> float
  - _normalise_strings(values) -> tuple[str, ...]
  - _merge_network_requirements(primary) -> dict[str, Any]
  - _merge_holographic_requirements(transmission) -> dict[str, Any]
  - _priority(score, gap_index, risk_index) -> str
  - _readiness(score, gap_index, risk_index) -> str
  - _delivery_windows(prototype_requirements, mitigation_windows, remediation_schedule, modernization_timeline) -> tuple[str, ...]
  - _backlog(scheduled, modernization_targets) -> tuple[dict[str, Any], ...]
  - _codebase_alignment(codebase) -> dict[str, Any]
  - _security_alignment(security) -> dict[str, Any]
  - _research_implications(research) -> dict[str, Any]

### `hololive_coliseum\auto_dev_innovation_manager.py`

- docstring: Innovation planning for the Coliseum auto-dev pipeline.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevInnovationManager (bases: (none))
    doc: Synthesize functionality blueprints from mechanics and modernization data.
    class_vars:
      - modernization_weight
      - novelty_weight
      - risk_weight
    methods:
      - innovation_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _normalise_strings(values) -> tuple[str, ...]
  - _alignment_score(alignment) -> float
  - _priority_from_score(score) -> str

### `hololive_coliseum\auto_dev_integrity_manager.py`

- docstring: Synthesize integrity signals across codebase, network, and holography.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevIntegrityManager (bases: (none))
    doc: Blend telemetry into an integrity report for the auto-dev pipeline.
    class_vars:
      - coverage_weight
      - holographic_weight
      - security_weight
    methods:
      - integrity_report(self) -> dict[str, Any]
      - _priority(self, coverage_gap, security_gap, holographic_gap, debt_risk, modernization_priority, optimization_priority) -> str
- functions:
  - _as_float(value, default) -> float
  - _clamp_ratio(value) -> float
  - _string_sequence(values, limit) -> tuple[str, ...]
  - _collect_actions() -> tuple[str, ...]
  - _target_names(targets) -> tuple[str, ...]

### `hololive_coliseum\auto_dev_intelligence_manager.py`

- docstring: Synthesize auto-dev signals into managerial general intelligence.
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - AutoDevIntelligenceManager (bases: (none))
    doc: Translate auto-dev outputs into actionable oversight guidance.
    class_vars:
      - (none)
    methods:
      - __init__(self, utilisation_ceiling) -> None
      - synthesise(self) -> dict[str, Any]
      - _processing_channels(self, research, guidance, evolution, network) -> dict[str, Any]
      - _orchestration_pipeline(self, monsters, spawn_plan, mob_ai, boss_plan, quests, research) -> dict[str, Any]
      - _management_playbook(self, backend_guidance, pipeline, percent, raw_percent, network) -> dict[str, Any]
      - _processing_percent(self, research, guidance, evolution, network) -> float
      - _raw_processing_percent(self, research, guidance, evolution, network) -> float
      - _load_state(self, percent) -> str
      - _resource_recommendation(self, load_state, percent) -> str
      - _encounter_alignment(self, monsters, spawn_plan, mob_ai, boss_plan) -> dict[str, Any]
      - _quest_alignment(self, quests) -> dict[str, Any]
      - _encounter_blueprint(self, monsters, spawn_plan, mob_ai, boss_plan) -> dict[str, Any]
      - _quest_synergy(self, quests, boss_plan) -> dict[str, Any]
      - _monster_catalog(self, monsters) -> dict[str, Any]
      - _monster_creation(self, monsters) -> dict[str, Any]
      - _spawn_overview(self, spawn_plan) -> dict[str, Any]
      - _spawn_tactics(self, spawn_plan) -> dict[str, Any]
      - _mob_ai_development(self, mob_ai) -> dict[str, Any]
      - _ai_development_plan(self, mob_ai, monsters, spawn_plan) -> dict[str, Any]
      - _boss_outlook(self, boss_plan, spawn_plan, quests) -> dict[str, Any]
      - _boss_spawn_strategy(self, boss_plan, spawn_plan, quests) -> dict[str, Any]
      - _quest_matrix(self, quests, boss_plan) -> dict[str, Any]
      - _quest_generation(self, quests, boss_plan) -> dict[str, Any]
      - _group_mechanics(self, monsters, spawn_plan) -> dict[str, Any]
      - _mob_ai_training(self, mob_ai, monsters, spawn_plan) -> dict[str, Any]
      - _boss_pressure(self, boss_plan, spawn_plan, monsters) -> dict[str, Any]
      - _quest_dependency(self, quests, boss_plan) -> dict[str, Any]
      - _processing_overview(self, percent, raw_percent, research_view) -> dict[str, Any]
      - _evolution_alignment(self, guidance, evolution) -> dict[str, Any]
      - _research_view(self, research) -> dict[str, Any]
      - _backend_guidance(self, guidance, evolution, research_view) -> dict[str, Any]
      - _competitive_analysis(self, research) -> dict[str, Any]
      - _group_spawn_coordination(self, monsters, spawn_plan) -> dict[str, Any]
      - _ai_innovation_focus(self, mob_ai, monsters) -> dict[str, Any]
      - _boss_spawn_readiness(self, boss_plan, spawn_plan) -> dict[str, Any]
      - _quest_trade_skill_alignment(self, quests, boss_plan) -> dict[str, Any]
      - _network_health(self, network) -> dict[str, Any]
      - _network_security(self, network) -> dict[str, Any]
      - _network_upgrade_plan(self, network) -> dict[str, Any]
      - _network_processing(self, network) -> dict[str, Any]
      - _network_security_automation(self, network) -> dict[str, Any]
      - _holographic_transmission(self, network) -> dict[str, Any]
      - _network_verification_layers(self, network) -> dict[str, Any]
      - _managerial_overview(self, backend_guidance, evolution_alignment, processing_overview, group_coordination, competitive_research, network) -> dict[str, Any]
      - _monster_forge_detail(self, monsters) -> dict[str, Any]
      - _group_spawn_mechanics_detail(self, spawn_plan, monsters) -> dict[str, Any]
      - _mob_ai_innovation_plan(self, mob_ai, spawn_plan) -> dict[str, Any]
      - _boss_spawn_matrix_detail(self, boss_plan, spawn_plan, quests) -> dict[str, Any]
      - _quest_tradecraft_detail(self, quests, boss_plan, spawn_plan) -> dict[str, Any]
      - _research_pressure(self, research) -> dict[str, Any]
      - _managerial_alignment(self, backend_guidance, management_playbook, monster_forge, group_spawn_mechanics_detail) -> dict[str, Any]
      - _competitive_pressure(self, research, processed_percent, raw_percent) -> dict[str, Any]
      - _network_security_overview(self, security, automation, upgrade_plan) -> dict[str, Any]
      - _holographic_signal_health(self, network, holographic, verification) -> dict[str, Any]
      - _monster_mutation_paths(self, monsters) -> dict[str, Any]
      - _group_spawn_support(self, spawn_plan, quests) -> dict[str, Any]
      - _ai_modularity_map(self, mob_ai, spawn_plan) -> dict[str, Any]
      - _boss_spawn_alerts(self, boss_plan, spawn_plan, network) -> dict[str, Any]
      - _quest_trade_dependencies(self, quests, boss_plan) -> dict[str, Any]
      - _research_benchmarking(self, research) -> dict[str, Any]
      - _managerial_guidance_map(self, management_playbook, backend_guidance, research_benchmarking, group_support) -> dict[str, Any]
      - _self_evolution_actions(self, pipeline, managerial_alignment, boss_alerts, research_benchmarking) -> tuple[str, ...]
      - _self_evolution_dashboard(self, backend_guidance, management_playbook, pipeline, network) -> dict[str, Any]
      - _directives(self, guidance, evolution) -> Iterable[str]
- functions:
  - _as_tuple(items) -> tuple[str, ...]

### `hololive_coliseum\auto_dev_interaction_manager.py`

- docstring: Fuse functionality, mechanics, and gameplay signals into interaction briefs.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevInteractionManager (bases: (none))
    doc: Blend gameplay, functionality, and network signals into interaction briefs.
    class_vars:
      - dynamics_weight
      - experience_weight
      - functionality_weight
      - gameplay_weight
      - gap_penalty_factor
      - innovation_weight
      - mechanics_weight
      - network_weight
      - playstyle_weight
      - research_penalty_factor
      - resilience_weight
      - security_weight
    methods:
      - interaction_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _clamp(value, minimum, maximum) -> float
  - _normalise_strings(values) -> tuple[str, ...]
  - _priority(score) -> str
  - _loop_names(loops) -> tuple[str, ...]

### `hololive_coliseum\auto_dev_iteration_manager.py`

- docstring: Manager for blending functionality and mechanics into iteration cycles.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevIterationManager (bases: (none))
    doc: Blend functionality, mechanics, and creation signals into iteration guidance.
    class_vars:
      - (none)
    methods:
      - iteration_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _clamp(value, minimum, maximum) -> float
  - _dedupe(values) -> tuple[Any, ...]
  - _priority(score, gap_index, risk_index) -> str
  - _merge_network_requirements() -> dict[str, Any]
  - _merge_holographic_requirements(transmission) -> dict[str, Any]
  - _iteration_cycles(functionality, mechanics, creation, blueprint) -> tuple[str, ...]
  - _iteration_actions(functionality, mechanics, creation, blueprint, network_auto_dev, security) -> tuple[str, ...]
  - _iteration_threads(functionality, creation, blueprint, execution) -> tuple[str, ...]
  - _iteration_windows(creation, blueprint, implementation) -> tuple[str, ...]
  - _iteration_focus(codebase, functionality, creation, blueprint) -> dict[str, Any]
  - _iteration_research(research, innovation, network_auto_dev) -> dict[str, Any]

### `hololive_coliseum\auto_dev_mechanics_manager.py`

- docstring: Synthesize mechanics expansion briefs for the auto-dev workflow.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevMechanicsManager (bases: (none))
    doc: Blend encounter, research, and governance data into mechanics plans.
    class_vars:
      - cohesion_weight
      - novelty_weight
      - risk_weight
    methods:
      - mechanics_blueprint(self) -> dict[str, Any]
      - _novelty_score(self, hazards, quest_tags, functionality_tracks, research, modernization) -> float
      - _cohesion_score(self, guidance, resilience, optimization, efficiency_score) -> float
      - _risk_score(self, codebase, security, resilience) -> float
- functions:
  - _as_float(value, default) -> float
  - _normalise_strings(values) -> tuple[str, ...]
  - _collect_from_mappings(values) -> tuple[str, ...]
  - _threat_value(level) -> float
  - _priority_from_score(score) -> str

### `hololive_coliseum\auto_dev_mitigation_manager.py`

- docstring: Translate auto-dev telemetry into actionable mitigation tasks.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - _DEF_OWNERS
- classes:
  - AutoDevMitigationManager (bases: (none))
    doc: Generate mitigation and upgrade plans based on manager reports.
    class_vars:
      - coverage_target
      - pressure_threshold
      - security_target
    methods:
      - derive_actions(self) -> dict[str, Any]
      - _stability_score(self, coverage, security_score, pressure_index, risk_index) -> float
      - _priority(self, stability_score, guidance_priority) -> str
      - _codebase_tasks(self, codebase, coverage) -> list[dict[str, Any]]
      - _extend_from_debt_profile(self, tasks, debt_profile) -> None
      - _network_tasks(self, network, security_score) -> list[str]
      - _research_tasks(self, research, pressure_index) -> list[str]
      - _intelligence_tasks(self, guidance, risk_index) -> list[str]
      - _holographic_upgrades(self, network) -> list[str]
      - _execution_windows(self, codebase_tasks, network_tasks, research_tasks) -> list[dict[str, Any]]
- functions:
  - _as_float(value, default) -> float
  - _normalise_tasks(tasks, owner) -> list[dict[str, Any]]

### `hololive_coliseum\auto_dev_mob_ai_manager.py`

- docstring: Generate AI behaviour directives for auto-generated mobs.
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - AutoDevMobAIManager (bases: (none))
    doc: Produce behavioural presets for monster groups.
    class_vars:
      - (none)
    methods:
      - ai_directives(self, monsters) -> dict[str, Any]
      - _behaviour(self, monster, spawn_danger) -> str
      - _abilities(self, hazard, projection_focus) -> tuple[str, ...]
      - _coordination_matrix(self, directives, spawn_danger) -> dict[str, Any]
      - _evolution_threads(self, monsters) -> tuple[str, ...]
      - _group_support(self, monsters) -> dict[str, Any]
- functions:
  - (none)

### `hololive_coliseum\auto_dev_modernization_manager.py`

- docstring: Combine codebase and network insights into modernization directives.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevModernizationManager (bases: (none))
    doc: Derive modernization actions from codebase and networking signals.
    class_vars:
      - modernization_threshold
      - security_baseline
    methods:
      - modernization_brief(self) -> dict[str, Any]
      - _prioritised_targets(self, targets) -> tuple[dict[str, Any], ...]
      - _priority(self, targets, codebase) -> str
      - _network_alignment(self, network, security, transmission) -> dict[str, Any]
      - _holographic_enhancements(self, transmission, remediation) -> tuple[str, ...]
      - _research_allocation(self, research, targets) -> dict[str, Any]
      - _mitigation_support(self, mitigation, remediation) -> tuple[str, ...]
      - _weakness_resolutions(self, codebase, mitigation, remediation) -> tuple[str, ...]
      - _timeline(self, targets, remediation) -> tuple[dict[str, Any], ...]
      - _modernization_actions(self, targets, holographic, mitigation_support) -> tuple[str, ...]
- functions:
  - _as_float(value, default) -> float
  - _dedupe(values) -> tuple[Any, ...]
  - _risk_weight(level) -> float

### `hololive_coliseum\auto_dev_monster_manager.py`

- docstring: Generate monster rosters for MMO auto-development planning.
- imports:
  - __future__
  - collections
  - typing
- globals:
  - (none)
- classes:
  - AutoDevMonsterManager (bases: (none))
    doc: Create monster templates from hazards and trade skill data.
    class_vars:
      - (none)
    methods:
      - __init__(self, max_monsters) -> None
      - generate_monsters(self) -> list[dict[str, Any]]
      - _select_trade_skill(self, hazard, trade_skills) -> str
      - _ai_focus(self, hazard, weakness) -> str
      - _spawn_synergy(self, count, hazard) -> str
      - _group_role(self, index, hazard, count) -> str
      - _creation_blueprint(self, hazard, weakness, synergy, group_role) -> dict[str, Any]
      - _ai_development_path(self, ai_focus, blueprint) -> dict[str, Any]
- functions:
  - _normalise(text) -> str

### `hololive_coliseum\auto_dev_network_manager.py`

- docstring: Auto-dev networking analytics for MMO planning.
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - AutoDevNetworkManager (bases: (none))
    doc: Summarise latency, reliability, bandwidth, and security posture.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - assess_network(self) -> dict[str, Any]
      - _latency_summary(self, nodes) -> dict[str, Any]
      - _reliability_summary(self, nodes) -> dict[str, Any]
      - _bandwidth_summary(self, samples) -> dict[str, Any]
      - _security_summary(self, events) -> dict[str, Any]
      - _network_health(self, latency, reliability, bandwidth, security) -> dict[str, Any]
      - _relay_plan(self, nodes, reliability, security) -> dict[str, Any]
      - _processing_summary(self, bandwidth, research_percent, auto_dev_load, incident_count) -> dict[str, Any]
      - _recommendations(self, network_health, relay_plan, security, bandwidth) -> list[str]
      - _security_automation(self, security, nodes, events) -> dict[str, Any]
      - _holographic_channels(self, bandwidth, detail, research_percent, auto_dev_load, incident_count) -> dict[str, Any]
      - _verification_layers(self, security, holographic) -> dict[str, Any]
      - _upgrade_backlog(self, nodes, relay_plan, security, health) -> dict[str, Any]
      - _security_auto_dev_brief(self, automation, backlog, verification) -> dict[str, Any]
      - _holographic_diagnostics(self, holographic, verification) -> dict[str, Any]
      - _resilience_matrix(self, health, reliability, security) -> dict[str, Any]
      - _zero_trust_blueprint(self, security_auto_dev, security) -> dict[str, Any]
      - _anomaly_signals(self, events, nodes) -> dict[str, Any]
      - _holographic_signal_matrix(self, holographic, verification) -> dict[str, Any]
      - _upgrade_paths(self, backlog, security_auto_dev, holographic) -> tuple[str, ...]
      - _extract_research_percent(self, research) -> float
      - _network_security_score(self, security_auto_dev, security, verification) -> float
      - _network_security_upgrades(self, security_auto_dev, backlog) -> tuple[str, ...]
      - _holographic_enhancements(self, holographic, security_auto_dev, verification) -> dict[str, Any]
      - _transmission_guardrails(self, diagnostics, verification, health, security_auto_dev, enhancements) -> dict[str, Any]
      - _lithographic_integrity(self, diagnostics, guardrails) -> dict[str, Any]
- functions:
  - _safe_average(values) -> float
  - _as_tuple(values) -> tuple[str, ...]

### `hololive_coliseum\auto_dev_network_upgrade_manager.py`

- docstring: Derive network upgrade and security automation tasks for the auto-dev loop.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevNetworkUpgradeManager (bases: (none))
    doc: Synthesize networking, security, and holographic directives.
    class_vars:
      - security_threshold
      - utilization_threshold
    methods:
      - plan_auto_dev(self) -> dict[str, Any]
      - _upgrade_tracks(self, network) -> tuple[str, ...]
      - _security_automation(self, security, mitigation) -> tuple[str, ...]
      - _holographic_integration(self, transmission) -> dict[str, Any]
      - _processing_focus(self, network, research) -> dict[str, Any]
      - _readiness_score(self, network, security, processing_focus) -> float
      - _priority(self, security, processing_focus) -> str
      - _codebase_links(self, codebase) -> tuple[str, ...]
      - _next_steps(self, upgrade_tracks, security_automation, holographic_actions, codebase_links) -> tuple[str, ...]
- functions:
  - _as_float(value, default) -> float
  - _dedupe(values) -> tuple[Any, ...]

### `hololive_coliseum\auto_dev_optimization_manager.py`

- docstring: Blend modernization, security, and remediation into optimisation briefs.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevOptimizationManager (bases: (none))
    doc: Blend telemetry into optimisation tasks for managerial planning.
    class_vars:
      - debt_threshold
      - security_floor
    methods:
      - optimization_brief(self) -> dict[str, Any]
      - _codebase_focus(self, codebase, mitigation, remediation) -> dict[str, Any]
      - _network_security_focus(self, network, security, network_auto_dev) -> dict[str, Any]
      - _holographic_plan(self, transmission, resilience, remediation) -> dict[str, Any]
      - _remediation_support(self, remediation) -> dict[str, Any]
      - _research_signal(self, research) -> dict[str, Any]
      - _modernization_dependencies(self, modernization, codebase) -> tuple[dict[str, Any], ...]
      - _fix_windows(self, remediation, modernization) -> tuple[str, ...]
      - _managerial_focus(self, guidance, resilience, research_signal) -> str
      - _optimization_actions(self, codebase_focus, network_focus, holographic_plan, dependencies, remediation_support) -> tuple[str, ...]
      - _priority(self, codebase, modernization, mitigation, security, network_focus) -> str
- functions:
  - _as_float(value, default) -> float
  - _collect_strings(values) -> tuple[str, ...]
  - _dedupe_strings(values) -> tuple[str, ...]

### `hololive_coliseum\auto_dev_pipeline.py`

- docstring: High-level orchestration for the Coliseum auto-dev managers.  This module stitches together the specialised managers that drive the MMO auto-development loop.  Each manager focuses on a narrow responsibility—monster generation, spawn planning, mob AI, boss escalation, quest support, research, or network posture.  ``AutoDevPipeline`` coordinates their outputs into a single plan that encounter designers and tooling can consume when simulating a new region.  The pipeline remains intentionally deterministic: every helper derives values from the supplied focus, scenarios, and trade skills so that tests can assert on the resulting structure.  Nevertheless, the orchestration aims to model the interplay between the systems by propagating insights (for example, spawn synergies feed mob AI projections, and research utilisation informs networking upgrades).
- imports:
  - .auto_dev_blueprint_manager
  - .auto_dev_boss_manager
  - .auto_dev_codebase_analyzer
  - .auto_dev_continuity_manager
  - .auto_dev_convergence_manager
  - .auto_dev_creation_manager
  - .auto_dev_design_manager
  - .auto_dev_dynamics_manager
  - .auto_dev_evolution_manager
  - .auto_dev_execution_manager
  - .auto_dev_experience_manager
  - .auto_dev_functionality_manager
  - .auto_dev_gameplay_manager
  - .auto_dev_governance_manager
  - .auto_dev_guidance_manager
  - .auto_dev_implementation_manager
  - .auto_dev_innovation_manager
  - .auto_dev_integrity_manager
  - .auto_dev_interaction_manager
  - .auto_dev_iteration_manager
  - .auto_dev_mechanics_manager
  - .auto_dev_mitigation_manager
  - .auto_dev_mob_ai_manager
  - .auto_dev_modernization_manager
  - .auto_dev_monster_manager
  - .auto_dev_network_manager
  - .auto_dev_network_upgrade_manager
  - .auto_dev_optimization_manager
  - .auto_dev_playstyle_manager
  - .auto_dev_quest_manager
  - .auto_dev_remediation_manager
  - .auto_dev_research_manager
  - .auto_dev_resilience_manager
  - .auto_dev_security_manager
  - .auto_dev_self_evolution_manager
  - .auto_dev_spawn_manager
  - .auto_dev_synthesis_manager
  - .auto_dev_systems_manager
  - .auto_dev_transmission_manager
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevPipeline (bases: (none))
    doc: Coordinate the auto-dev managers into a coherent planning loop.
    class_vars:
      - blueprint_manager
      - boss_manager
      - codebase_analyzer
      - continuity_manager
      - convergence_manager
      - creation_manager
      - design_manager
      - dynamics_manager
      - evolution_manager
      - execution_manager
      - experience_manager
      - functionality_manager
      - gameplay_manager
      - governance_manager
      - guidance_manager
      - implementation_manager
      - innovation_manager
      - integrity_manager
      - interaction_manager
      - iteration_manager
      - mechanics_manager
      - mitigation_manager
      - mob_ai_manager
      - modernization_manager
      - monster_manager
      - network_manager
      - network_upgrade_manager
      - optimization_manager
      - playstyle_manager
      - quest_manager
      - remediation_manager
      - research_manager
      - resilience_manager
      - security_manager
      - self_evolution_manager
      - spawn_manager
      - synthesis_manager
      - systems_manager
      - transmission_manager
    methods:
      - build_plan(self) -> dict[str, Any]
      - _overview(self, monsters, spawn_plan, boss_plan, guidance, network) -> dict[str, Any]
      - _weakness_analysis(self, guidance, network, research, codebase) -> dict[str, Any]
      - _stability_report(self, codebase, network, mitigation, remediation, research) -> dict[str, Any]
      - _backend_dashboard(self, guidance, network, mitigation, remediation) -> dict[str, Any]
      - _codebase_fix_summary(self, codebase, remediation) -> dict[str, Any]
      - _functionality_gap_report(self) -> dict[str, Any]
      - _managerial_intelligence_matrix(self, guidance, resilience, mitigation, remediation, network, continuity, security, modernization, optimization, integrity, mechanics, innovation, experience, functionality, dynamics, playstyle, gameplay, design, systems, creation, blueprint, synthesis, convergence, implementation, execution, iteration) -> dict[str, Any]
- functions:
  - _normalise_trade_skills(skills) -> list[str]
  - _roadmap_focus(focus) -> dict[str, Any]
  - _projection_focus(monsters, spawn_plan, trade_skills) -> dict[str, Any]
  - _intensity_entries(intensities) -> Iterable[tuple[float, str]]
  - _copy_dict(data) -> dict[str, Any]

### `hololive_coliseum\auto_dev_playstyle_manager.py`

- docstring: Derive playstyle archetypes from functionality and dynamics telemetry.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevPlaystyleManager (bases: (none))
    doc: Blend functionality, experience, and dynamics data into playstyle briefs.
    class_vars:
      - experience_weight
      - functionality_weight
      - innovation_weight
      - resilience_weight
      - risk_penalty_factor
      - stability_weight
      - synergy_weight
    methods:
      - playstyle_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _normalise_strings(values) -> tuple[str, ...]
  - _priority(score) -> str
  - _archetype_name(base, focus, index) -> str

### `hololive_coliseum\auto_dev_projection_manager.py`

- docstring: Forecast MMO auto-dev focus areas from recent telemetry.
- imports:
  - .auto_dev_feedback_manager
  - __future__
  - collections
  - typing
- globals:
  - (none)
- classes:
  - AutoDevProjectionManager (bases: (none))
    doc: Convert auto-dev telemetry into short-term hazard projections.
    class_vars:
      - (none)
    methods:
      - __init__(self, feedback_manager, tuning_manager, window) -> None
      - projection_summary(self, limit) -> Dict[str, Any]
      - _focus(self, limit) -> List[Dict[str, Any]]
      - _aggregate_hazards(self) -> Counter[str]
      - _recent_history(self) -> Sequence[Dict[str, Any]]
      - _recommended_powerups(self, hazard) -> tuple[str, ...]
      - _spawn_multiplier_for_weight(weight) -> float
- functions:
  - (none)

### `hololive_coliseum\auto_dev_quest_manager.py`

- docstring: Generate MMO quests from trade skills and encounter plans.
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - AutoDevQuestManager (bases: (none))
    doc: Assemble quest hooks that react to trade skills and bosses.
    class_vars:
      - (none)
    methods:
      - __init__(self, max_quests) -> None
      - generate_quests(self, trade_skills) -> list[dict[str, Any]]
      - _objective(self, skill, boss) -> str
      - _reward(self, spawn_plan) -> str
      - _supports_boss(self, objective, boss) -> bool
      - _difficulty(self, spawn_plan, index) -> str
      - _tags(self, skill, boss) -> tuple[str, ...]
      - _spawn_dependency(self, spawn_plan, skill, index) -> dict[str, Any]
      - _trade_synergy(self, skill, spawn_plan, boss) -> dict[str, Any]
      - _support_threads(self, spawn_plan, boss) -> tuple[str, ...]
- functions:
  - (none)

### `hololive_coliseum\auto_dev_remediation_manager.py`

- docstring: Apply mitigation plans to simulate fixes within the auto-dev pipeline.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevRemediationManager (bases: (none))
    doc: Implement mitigation actions to improve stability projections.
    class_vars:
      - codebase_throughput
      - network_throughput
      - research_throughput
    methods:
      - implement_fixes(self) -> dict[str, Any]
      - _apply_codebase_tasks(self, tasks, applied, scheduled, counts) -> None
      - _apply_network_tasks(self, tasks, applied, scheduled, counts) -> None
      - _apply_research_tasks(self, tasks, applied, scheduled, counts) -> None
      - _apply_guidance_tasks(self, tasks, applied, scheduled, counts) -> None
      - _stability_projection(self, codebase, network, research, guidance, counts) -> dict[str, Any]
      - _network_hardening(self, network, applied_network) -> dict[str, Any]
      - _research_balancing(self, research, applied_research) -> dict[str, Any]
      - _holographic_adjustments(self, network, applied_network) -> list[str]
      - _codebase_progress(self, applied, scorecards) -> tuple[dict[str, Any], ...]
- functions:
  - _as_float(value, default) -> float
  - _normalise_codebase_tasks(tasks) -> list[dict[str, Any]]
  - _normalise_strings(values) -> list[str]

### `hololive_coliseum\auto_dev_research_manager.py`

- docstring: Track background research that powers the auto-dev roadmap.
- imports:
  - __future__
  - os
  - statistics
  - typing
- globals:
  - (none)
- classes:
  - AutoDevResearchManager (bases: (none))
    doc: Record processing budgets used to study other games.
    class_vars:
      - (none)
    methods:
      - __init__(self, default_percent) -> None
      - record_utilization(self, percent) -> None
      - record_competitive_research(self, percent) -> None
      - update_from_intensity(self, intensity) -> None
      - capture_runtime_utilization(self) -> float
      - intelligence_brief(self) -> Dict[str, object]
      - _recommendation(self, average) -> str
      - _focus_from_source(self, source) -> str
      - _competitive_view(self) -> Dict[str, object]
      - _runtime_percent(self) -> float
      - _volatility(self) -> float
      - _trend_direction(self) -> str
      - _pressure_index(self, latest, average, volatility) -> float
      - _weakness_signals(self, latest, pressure_index, volatility) -> list[str]
      - sources(self) -> Dict[str, float]
      - samples(self) -> Sequence[float]
      - latest_sample(self) -> float | None
- functions:
  - (none)

### `hololive_coliseum\auto_dev_resilience_manager.py`

- docstring: Assess resilience of the auto-dev loop using multi-domain telemetry.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevResilienceManager (bases: (none))
    doc: Combine telemetry to score resilience and surface stabilisation advice.
    class_vars:
      - codebase_weight
      - network_weight
      - remediation_weight
      - research_penalty_weight
    methods:
      - assess_resilience(self) -> dict[str, Any]
      - _resilience_index(self, coverage, security_score, uptime, guardrail_severity, mitigation_score, instability, research_pressure, utilisation, mitigation_priority, network_status, applied_counts) -> float
      - _penalty(self, instability, research_pressure, utilisation, mitigation_priority, network_status, security_score) -> float
      - _research_penalty(self, pressure, utilisation) -> float
      - _grade(self, index) -> str
      - _resilience_actions(self, coverage, security_score, guardrail_severity, research_pressure, utilisation, mitigation_priority, applied_counts) -> tuple[str, ...]
      - _stability_risks(self, coverage, security_score, network_status, research_pressure, utilisation, trend, debt_risk, instability) -> tuple[str, ...]
      - _holographic_readiness(self, phase, efficiency, guardrail_severity, actions) -> dict[str, Any]
      - _network_security_focus(self, security_score, network, guardrail_severity, network_tasks) -> dict[str, Any]
      - _managerial_overwatch(self, guidance, grade, scheduled_counts, mitigation_priority) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _normalise_sequence(values) -> tuple[Mapping[str, Any], ...]
  - _count_domains(fixes) -> dict[str, int]

### `hololive_coliseum\auto_dev_roadmap_manager.py`

- docstring: Aggregate auto-dev insights into actionable MMO roadmaps.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - RoadmapEntry (bases: (none))
    doc: Container for a single roadmap iteration.
    class_vars:
      - focus
      - iteration
      - metrics
      - priority_actions
      - projection_focus
      - scenarios
      - support_plan
    methods:
      - as_dict(self) -> Dict[str, Any]
  - AutoDevRoadmapManager (bases: (none))
    doc: Compile consolidated MMO auto-dev roadmaps from existing insights.
    class_vars:
      - (none)
    methods:
      - __init__(self, max_history) -> None
      - compile_iteration(self) -> Dict[str, Any]
      - recent_history(self) -> List[Dict[str, Any]]
      - latest(self) -> Dict[str, Any] | None
      - _determine_focus(self, feedback, projection_focus, scenarios, feedback_manager) -> str
      - _gather_metrics(self, feedback, feedback_manager) -> Dict[str, Any]
      - _build_priority_actions(self, hazard, feedback, projection_focus, support_plan) -> List[Dict[str, Any]]
      - _normalise_projection_focus(projection) -> List[Dict[str, Any]]
- functions:
  - _clean_powerups(raw) -> tuple[str, ...]

### `hololive_coliseum\auto_dev_scenario_manager.py`

- docstring: Build actionable auto-dev scenarios from projections and objectives.
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - AutoDevScenarioManager (bases: (none))
    doc: Synthesize MMO auto-dev scenario briefs for designers.
    class_vars:
      - DEFAULT_OBJECTIVES
    methods:
      - __init__(self, projection_manager, objective_manager) -> None
      - scenario_briefs(self, limit) -> List[Dict[str, Any]]
      - _focus_entries(self, limit) -> List[Dict[str, Any]]
      - _counter_plan(self, focus_entry) -> Dict[str, Any]
      - _objective_recommendations(self, hazard) -> List[Dict[str, Any]]
      - _training_focus(hazard, objectives) -> str
      - _fallback_brief(self) -> Dict[str, Any] | None
- functions:
  - (none)

### `hololive_coliseum\auto_dev_security_manager.py`

- docstring: Security orchestration manager for the auto-dev pipeline.
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - AutoDevSecurityManager (bases: (none))
    doc: Derive actionable hardening steps from pipeline telemetry.
    class_vars:
      - (none)
    methods:
      - security_brief(self) -> dict[str, Any]
      - _threat_level(self, security_score, guardrail_status, mitigation_priority, anomaly_count) -> str
      - _automation_directives(self, network, mitigation) -> dict[str, Any]
      - _hardening_tasks(self, codebase, remediation) -> tuple[dict[str, Any], ...]
      - _holographic_lattice(self, network, remediation, mitigation_priority) -> dict[str, Any]
      - _intel_brief(self, research, codebase, threat_level, mitigation_priority) -> dict[str, Any]
      - _network_security_actions(self, network, automation, hardening) -> tuple[str, ...]
      - _governance_alignment(self, guidance, mitigation, threat_level) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _as_tuple(values) -> tuple[Any, ...]

### `hololive_coliseum\auto_dev_self_evolution_manager.py`

- docstring: Blend managerial telemetry into a self-evolution blueprint.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevSelfEvolutionManager (bases: (none))
    doc: Fuse pipeline outputs into actionable self-evolution directives.
    class_vars:
      - horizon
    methods:
      - blueprint(self) -> dict[str, Any]
      - _readiness_index(self, intelligence_score, security_score, coverage, stability_score) -> float
      - _readiness_state(self, readiness, governance_state) -> str
      - _upgrade_directives(self, network) -> tuple[str, ...]
      - _security_enhancements(self, security) -> tuple[str, ...]
      - _holographic_directives(self, transmission) -> tuple[str, ...]
      - _codebase_focus(self, codebase, mitigation, remediation) -> dict[str, Any]
      - _research_focus(self, research, mitigation) -> dict[str, Any]
      - _oversight(self, governance) -> dict[str, Any]
      - _progress_overview(self, remediation) -> dict[str, Any]
      - _domain_counts(self, entries) -> dict[str, int]
      - _managerial_threads(self, guidance) -> tuple[str, ...]
      - _composite_score(self, intelligence_score, security_score, stability_score, readiness_index) -> float
      - _next_actions(self, upgrades, security, holographic, codebase_tasks, research_tasks) -> tuple[str, ...]
- functions:
  - _as_float(value, default) -> float
  - _dedupe(values) -> tuple[Any, ...]

### `hololive_coliseum\auto_dev_spawn_manager.py`

- docstring: Plan monster group spawns for MMO auto-development.
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - AutoDevSpawnManager (bases: (none))
    doc: Create spawn schedules that respond to projected danger.
    class_vars:
      - (none)
    methods:
      - __init__(self, base_group_size) -> None
      - plan_groups(self, monsters) -> dict[str, Any]
      - _danger_from_scenarios(self, scenarios) -> float
      - _entry_point(self, index) -> str
      - _cohort_matrix(self, monsters, groups) -> dict[str, Any]
      - _escalation_plan(self, reinforcement_curve, danger_scale) -> dict[str, Any]
      - _group_roles(self, monsters) -> tuple[str, ...]
      - _group_threads(self, monsters) -> tuple[str, ...]
- functions:
  - (none)

### `hololive_coliseum\auto_dev_synthesis_manager.py`

- docstring: Synthesis manager that aligns creation and mechanics planning outputs.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevSynthesisManager (bases: (none))
    doc: Blend creation and mechanics telemetry into actionable synthesis briefs.
    class_vars:
      - creation_weight
      - design_weight
      - dynamics_weight
      - experience_weight
      - functionality_weight
      - gap_penalty_factor
      - innovation_weight
      - mechanics_weight
      - novelty_bonus_factor
      - risk_penalty_factor
      - security_bonus_factor
      - systems_weight
    methods:
      - synthesis_brief(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _clamp(value, minimum, maximum) -> float
  - _priority(score, risk_index, gap_index) -> str
  - _normalise_strings(values) -> tuple[str, ...]
  - _merge_network_requirements() -> dict[str, Any]
  - _merge_holographic_requirements(transmission) -> dict[str, Any]

### `hololive_coliseum\auto_dev_systems_manager.py`

- docstring: Synthesize design, functionality, and networking data into systems briefs.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevSystemsManager (bases: (none))
    doc: Fuse design, functionality, and telemetry into systems planning briefs.
    class_vars:
      - design_weight
      - dynamics_weight
      - experience_weight
      - fragility_penalty_factor
      - functionality_weight
      - gameplay_weight
      - innovation_weight
      - interaction_weight
      - mechanics_weight
      - network_bonus_factor
      - risk_penalty_factor
    methods:
      - systems_blueprint(self) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _clamp(value, minimum, maximum) -> float
  - _priority(score, fragility) -> str
  - _normalise_strings(values) -> tuple[str, ...]
  - _merge_network_requirements() -> dict[str, Any]
  - _merge_holographic_requirements(transmission) -> dict[str, Any]
  - _architecture_overview(network, transmission, security, governance, self_evolution) -> dict[str, Any]

### `hololive_coliseum\auto_dev_transmission_manager.py`

- docstring: Calibrate holographic transmissions for the auto-dev networking stack.
- imports:
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - AutoDevTransmissionManager (bases: (none))
    doc: Derive holographic compression and security directives from telemetry.
    class_vars:
      - aggressive_threshold
      - base_algorithm
      - baseline_level
      - secure_threshold
    methods:
      - calibrate(self, network) -> dict[str, Any]
      - _compression_profile(self, efficiency, phase, encrypted_channels, layer_count, directive) -> dict[str, Any]
      - _phase_alignment(self, phase, integrity, phase_directives, holographic_upgrades) -> dict[str, Any]
      - _security_layers(self, layer_count, severity_focus, integrity, verification_layers) -> dict[str, Any]
      - _utilization_projection(self, research, applied_fixes, mitigation_priority) -> float
      - _bandwidth_budget(self, average_bandwidth, compression_level, auto_load, resilience_score) -> float
      - _notes(self, compression, security_layers, upgrades, adjustments) -> tuple[str, ...]
      - _guardrail_review(self, guardrails, adjustments) -> dict[str, Any]
      - _lithographic_snapshot(self, diagnostics, guardrails, network_snapshot) -> dict[str, Any]
      - _spectral_waveform(self, diagnostics, holographic, enhancements, guardrails) -> dict[str, Any]
      - _lattice_overlay(self, lattice, waveform, guardrails) -> dict[str, Any]
- functions:
  - _as_float(value, default) -> float
  - _as_int(value, default) -> int

### `hololive_coliseum\auto_dev_tuning_manager.py`

- docstring: Derive arena tuning directives from auto-dev telemetry.
- imports:
  - .auto_dev_feedback_manager
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - AutoDevTuningManager (bases: (none))
    doc: Translate auto-dev feedback into gameplay adjustments.
    class_vars:
      - COUNTER_POWERUPS
      - MIN_DELAY_MS
    methods:
      - __init__(self, feedback_manager) -> None
      - recommend_spawn_timers(self, base_timers) -> Dict[str, int]
      - support_plan(self) -> Dict[str, object] | None
      - _current_challenge(self) -> Dict[str, int] | None
      - _multiplier_for_target(target) -> float
- functions:
  - (none)

### `hololive_coliseum\auto_skill_manager.py`

- docstring: Auto-generate skills using level and stat inputs.
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - AutoSkillManager (bases: (none))
    doc: Generate skills based on level and stats.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - generate(self, base_name, level, stats) -> dict
- functions:
  - (none)

### `hololive_coliseum\ban_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - BanManager (bases: (none))
    doc: Maintain a list of banned users.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - ban(self, user) -> None
      - unban(self, user) -> None
      - is_banned(self, user) -> bool
- functions:
  - (none)

### `hololive_coliseum\billing_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - BillingManager (bases: (none))
    doc: Track player purchases and subscriptions.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_purchase(self, user_id, item) -> None
      - get_purchases(self, user_id) -> list[str]
- functions:
  - (none)

### `hololive_coliseum\blockchain.py`

- docstring: (none)
- imports:
  - .accounts
  - base64
  - cryptography.exceptions
  - cryptography.fernet
  - cryptography.hazmat.primitives
  - cryptography.hazmat.primitives.asymmetric
  - hashlib
  - json
  - os
  - time
  - typing
  - uuid
- globals:
  - BALANCE_FILE
  - CHAIN_FILE
  - CONTRACT_FILE
  - DIFFICULTY
  - SAVE_DIR
- classes:
  - (none)
- functions:
  - _load_json(path, default) -> Any
  - _save_json(path, data) -> None
  - load_chain() -> List[Dict[str, Any]]
  - save_chain(chain) -> None
  - load_balances() -> Dict[str, int]
  - save_balances(data) -> None
  - get_balance(user_id) -> int
  - _hash_block(data) -> str
  - hash_region(region) -> str
  - _mine_block(block) -> None
  - mine_dummy_block(difficulty) -> Dict[str, Any]
  - add_seed(seed) -> Dict[str, Any]
  - add_region(region) -> Dict[str, Any]
  - add_game(players, winner, bet, game_id, signing_keys) -> Dict[str, Any]
  - add_vote(account_id, choice, category) -> Dict[str, Any]
  - search(game_id, user_id) -> List[Dict[str, Any]]
  - add_contract(request_id, players, bet) -> None
  - fulfill_contract(request_id, winner) -> Dict[str, Any] | None
  - verify_chain(chain) -> bool
  - merge_chain(remote) -> None
  - add_message(sender, recipient, message, admin_public_key_pem) -> Dict[str, Any]
  - decrypt_message(block, private_key_pem) -> str
  - admin_decrypt(block, admin_private_key_pem) -> str

### `hololive_coliseum\bot_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - BotManager (bases: (none))
    doc: Spawn and update automated bot players for testing.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - add_bot(self, name) -> None
      - remove_bot(self, name) -> None
      - list_bots(self)
- functions:
  - (none)

### `hololive_coliseum\buff_manager.py`

- docstring: (none)
- imports:
  - .status_effects
- globals:
  - (none)
- classes:
  - BuffManager (bases: (none))
    doc: Wrapper managing buff and debuff status effects.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_buff(self, target, effect) -> None
      - update(self, now) -> None
- functions:
  - (none)

### `hololive_coliseum\camera_manager.py`

- docstring: Camera manager tracking viewport offset.
- imports:
  - __future__
  - pygame
  - random
  - typing
- globals:
  - (none)
- classes:
  - CameraManager (bases: (none))
    doc: Store a camera offset that follows a target rect and can shake.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - shake(self, duration, magnitude) -> None
      - update(self) -> None
      - follow(self, rect, screen_size) -> None
      - follow_bounds(self, rect, screen_size, world_size) -> None
      - apply(self, rect) -> pygame.Rect
  - ThirdPersonCamera (bases: CameraManager)
    doc: Camera that keeps the target lower on screen for a 3rd-person view.
    class_vars:
      - (none)
    methods:
      - follow(self, rect, screen_size) -> None
- functions:
  - (none)

### `hololive_coliseum\chat_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ChatManager (bases: (none))
    doc: Manage an in-game chat box with message history.
    class_vars:
      - (none)
    methods:
      - __init__(self, max_messages)
      - toggle(self) -> None
      - show(self) -> None
      - hide(self) -> None
      - send(self, user, msg) -> None
      - history(self, limit)
      - clear(self) -> None
- functions:
  - (none)

### `hololive_coliseum\cheat_detection_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - CheatDetectionManager (bases: (none))
    doc: Detect basic suspicious activity such as impossible speed.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - check_speed(self, speed, max_speed) -> bool
- functions:
  - (none)

### `hololive_coliseum\class_generator.py`

- docstring: Generate unique MMO class templates.
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ClassGenerator (bases: (none))
    doc: Create class definitions while ensuring unique names.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - create(self, name, stats) -> dict[str, int]
- functions:
  - (none)

### `hololive_coliseum\class_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ClassManager (bases: (none))
    doc: Store MMO character classes and their base stats.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_class(self, name, stats) -> None
      - get_stats(self, name) -> dict[str, int] | None
      - list_classes(self) -> list[str]
- functions:
  - (none)

### `hololive_coliseum\cluster_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ClusterManager (bases: (none))
    doc: Track servers participating in a multi-node cluster.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - register(self, address) -> None
      - unregister(self, address) -> None
- functions:
  - (none)

### `hololive_coliseum\combat_manager.py`

- docstring: Combat related helpers.
- imports:
  - .damage_manager
  - .damage_number
  - .status_effects
  - __future__
  - pygame
  - typing
- globals:
  - (none)
- classes:
  - CombatManager (bases: (none))
    doc: Manage combat turns and collision handling.
    class_vars:
      - (none)
    methods:
      - __init__(self, status_manager, team_manager) -> None
      - add(self, actor) -> None
      - _is_invincible(self, actor, now) -> bool
      - remove(self, actor) -> None
      - next_actor(self)
      - handle_collisions(self, player, enemies, projectiles, melee_attacks, now, damage_numbers) -> list
- functions:
  - (none)

### `hololive_coliseum\companion_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - CompanionManager (bases: (none))
    doc: Assign a single companion to each player.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - assign(self, player_id, companion) -> None
      - get(self, player_id)
- functions:
  - (none)

### `hololive_coliseum\crafting_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - CraftingManager (bases: (none))
    doc: Manage crafting recipes and craft items from an inventory.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_recipe(self, name, ingredients, result) -> None
      - craft(self, name, inventory) -> str | None
- functions:
  - (none)

### `hololive_coliseum\crafting_station.py`

- docstring: Interactable station that crafts items using a recipe.
- imports:
  - __future__
- globals:
  - (none)
- classes:
  - CraftingStation (bases: (none))
    doc: Craft items when the player interacts with the station.
    class_vars:
      - (none)
    methods:
      - __init__(self, crafting_manager, recipe) -> None
      - interact(self, inventory) -> str | None
- functions:
  - (none)

### `hololive_coliseum\currency_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - CurrencyManager (bases: (none))
    doc: Track balances of in-game currency.
    class_vars:
      - (none)
    methods:
      - __init__(self, starting)
      - add(self, amount) -> int
      - spend(self, amount) -> bool
      - get_balance(self) -> int
- functions:
  - (none)

### `hololive_coliseum\daily_task_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - DailyTaskManager (bases: (none))
    doc: Manage daily quests with automatic reset.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - add_task(self, name) -> None
      - complete(self, name) -> None
      - reset(self) -> None
- functions:
  - (none)

### `hololive_coliseum\damage_manager.py`

- docstring: (none)
- imports:
  - random
- globals:
  - (none)
- classes:
  - DamageManager (bases: (none))
    doc: Compute final damage values and apply them to targets.
    class_vars:
      - (none)
    methods:
      - calculate(self, base, defense, multiplier, crit_chance, crit_multiplier, return_crit) -> int | tuple[int, bool]
      - apply(self, target, base) -> int
- functions:
  - (none)

### `hololive_coliseum\damage_number.py`

- docstring: Sprites for floating damage indicators.
- imports:
  - __future__
  - pygame
- globals:
  - (none)
- classes:
  - DamageNumber (bases: pygame.sprite.Sprite)
    doc: Display a floating number for recent damage.  Critical hits render in yellow to stand out from normal red numbers.
    class_vars:
      - (none)
    methods:
      - __init__(self, value, pos, critical) -> None
      - update(self, now) -> None
  - CheerText (bases: pygame.sprite.Sprite)
    doc: Floating cheer text for hype moments.
    class_vars:
      - (none)
    methods:
      - __init__(self, text, pos) -> None
      - update(self, now) -> None
- functions:
  - (none)

### `hololive_coliseum\data_protection_manager.py`

- docstring: Encryption and signing helpers for network packets.
- imports:
  - .transmission_manager
  - cryptography.hazmat.primitives.ciphers.aead
  - hashlib
  - hmac
  - json
  - os
  - time
  - typing
  - uuid
- globals:
  - (none)
- classes:
  - DataProtectionManager (bases: (none))
    doc: Manage packet encryption, signing and basic replay protection.
    class_vars:
      - (none)
    methods:
      - __init__(self, key, secret, level, algorithm, sign_key, max_age, time_func, sanitize_fields) -> None
      - encrypt(self, data) -> bytes
      - decrypt(self, data) -> bytes
      - _sign(self, msg) -> str
      - _sanitize(self, msg) -> None
      - encode(self, msg) -> bytes
      - decode(self, packet) -> dict[str, Any] | None
      - rotate_keys(self, key, secret, sign_key) -> None
- functions:
  - (none)

### `hololive_coliseum\device_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - DeviceManager (bases: (none))
    doc: Handle haptic and motion device details.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - register(self, name, info) -> None
      - get(self, name)
- functions:
  - (none)

### `hololive_coliseum\distributed_state_manager.py`

- docstring: (none)
- imports:
  - .cluster_manager
  - .node_manager
  - .shared_state_manager
  - .transmission_manager
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - DistributedStateManager (bases: (none))
    doc: Share game state deltas with peer servers and ingest remote updates.
    class_vars:
      - (none)
    methods:
      - __init__(self, state, nodes, transmission, cluster, history_size) -> None
      - register_node(self, host, port) -> None
      - unregister_node(self, host, port) -> None
      - broadcast(self) -> List[Dict[str, Any]]
      - nodes_pending_ack(self) -> List[Tuple[str, int]]
      - acknowledge(self, node, sequence) -> None
      - resend_pending(self) -> List[Dict[str, Any]]
      - prepare_handshake(self, host, port) -> List[Dict[str, Any]]
      - prepare_catch_up(self, host, port, sequence) -> List[Dict[str, Any]]
      - apply_remote(self, packet) -> Dict[str, Any]
      - state_copy(self) -> Dict[str, Any]
      - sync_plan(self) -> Dict[str, Any]
      - peer_status(self) -> List[Dict[str, Any]]
      - _load_nodes(self) -> List[Tuple[str, int]]
      - _serialise_nodes(nodes) -> List[List[Any]]
      - _ingest_nodes(self, nodes) -> None
      - _ingest_cluster(self, addresses) -> None
      - _build_state_payload(self, delta, nodes) -> Dict[str, Any]
      - _build_transmission(self, node, packet, delta) -> Dict[str, Any]
      - _build_snapshot_transmission(self, node) -> Dict[str, Any]
      - _record_history(self, sequence, delta, packet) -> None
- functions:
  - (none)

### `hololive_coliseum\dungeon_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - DungeonManager (bases: (none))
    doc: Handle dungeon lockouts for players.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - set_lockout(self, player_id, dungeon, expires) -> None
      - can_enter(self, player_id, dungeon, now) -> bool
- functions:
  - (none)

### `hololive_coliseum\dynamic_content_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - DynamicContentManager (bases: (none))
    doc: Generate basic random quests or items.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - create(self, kind) -> str
      - list_content(self)
- functions:
  - (none)

### `hololive_coliseum\economy_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - EconomyManager (bases: (none))
    doc: Keep track of item prices.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - set_price(self, item, price) -> None
      - get_price(self, item) -> int
      - remove_price(self, item) -> None
- functions:
  - (none)

### `hololive_coliseum\effect_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - EffectManager (bases: (none))
    doc: Track triggered visual effects.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - trigger(self, effect) -> None
- functions:
  - (none)

### `hololive_coliseum\emote_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - EmoteManager (bases: (none))
    doc: Keep a table of available emotes.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - get(self, name)
      - add(self, name, value) -> None
- functions:
  - (none)

### `hololive_coliseum\environment_manager.py`

- docstring: Manage weather, day/night cycle, and resulting ambient lighting.
- imports:
  - __future__
  - math
  - random
  - typing
- globals:
  - MAX_OVERLAY_ALPHA
  - WEATHER_FRICTION
  - WEATHER_TINTS
- classes:
  - EnvironmentManager (bases: (none))
    doc: Track weather, day/night cycle, and calculate ambient lighting.
    class_vars:
      - (none)
    methods:
      - __init__(self, day_length_ms)
      - update(self, now) -> None
      - is_day(self) -> bool
      - set(self, key, value) -> None
      - get(self, key, default)
      - attach_forecast_manager(self, forecast) -> None
      - upcoming_weather(self, steps) -> list[str]
      - get_light_level(self) -> float
      - ambient_overlay(self) -> Tuple[int, int, int, int]
      - randomize_weather(self) -> str
      - _update_lighting(self) -> None
- functions:
  - (none)

### `hololive_coliseum\equipment_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - EquipmentManager (bases: (none))
    doc: Manage equipment slots and selection order for a player.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - equip(self, slot, item) -> None
      - unequip(self, slot) -> None
      - get(self, slot)
- functions:
  - (none)

### `hololive_coliseum\event_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - EventManager (bases: (none))
    doc: Track triggered world events.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - trigger(self, name) -> None
      - get_history(self)
- functions:
  - (none)

### `hololive_coliseum\event_modifier_manager.py`

- docstring: Derive arena modifiers from MMO world region data.
- imports:
  - .world_region_manager
  - __future__
  - typing
- globals:
  - BIOME_RULES
  - DEFAULT_CONFIG
- classes:
  - EventModifierManager (bases: (none))
    doc: Compute arena modifiers using stored MMO regions.
    class_vars:
      - (none)
    methods:
      - __init__(self, region_manager) -> None
      - refresh(self) -> Dict[str, Any]
      - get_config(self) -> Dict[str, Any]
- functions:
  - (none)

### `hololive_coliseum\experience_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ExperienceManager (bases: (none))
    doc: Handle experience gain and leveling.
    class_vars:
      - (none)
    methods:
      - __init__(self, level, xp, threshold) -> None
      - add_xp(self, amount) -> bool
- functions:
  - (none)

### `hololive_coliseum\friend_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - FriendManager (bases: (none))
    doc: Keep track of friends.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - add_friend(self, user) -> None
      - remove_friend(self, user) -> None
      - is_friend(self, user) -> bool
      - list_friends(self)
- functions:
  - (none)

### `hololive_coliseum\game.py`

- docstring: Main game module handling menus, gameplay loop and networking.
- imports:
  - .accessibility_manager
  - .accounts
  - .achievement_manager
  - .ai_autoplayer
  - .ai_experience_manager
  - .ai_experience_store
  - .ai_manager
  - .ally_manager
  - .auto_dev_feedback_manager
  - .auto_dev_pipeline
  - .auto_dev_projection_manager
  - .auto_dev_tuning_manager
  - .camera_manager
  - .chat_manager
  - .combat_manager
  - .damage_number
  - .economy_manager
  - .environment_manager
  - .event_manager
  - .event_modifier_manager
  - .game_state_manager
  - .gravity_zone
  - .hazard_manager
  - .hazards
  - .healing_zone
  - .hud_manager
  - .input_manager
  - .item_manager
  - .iteration_manager
  - .keybind_manager
  - .level_manager
  - .loot_manager
  - .map_manager
  - .melee_attack
  - .menu_manager
  - .menus
  - .mining_manager
  - .mmo_backend_manager
  - .network
  - .node_registry
  - .npc_manager
  - .objective_manager
  - .placeholder_sprites
  - .player
  - .powerup
  - .projectile
  - .reputation_manager
  - .save_manager
  - .score_manager
  - .screenshot_manager
  - .shared_state_manager
  - .sound_manager
  - .spawn_manager
  - .state_verification_manager
  - .status_effects
  - .team_manager
  - .voting_manager
  - .weather_forecast_manager
  - .world_generation_manager
  - .world_player_manager
  - cryptography.hazmat.primitives
  - math
  - os
  - pygame
  - random
- globals:
  - CHARACTER_PLAN_FILE
- classes:
  - Game (bases: MenuMixin)
    doc: Main game class with menus, AI opponents, networking and settings.
    class_vars:
      - (none)
    methods:
      - __init__(self, width, height)
      - last_hazard_damage(self) -> int
      - last_hazard_damage(self, value) -> None
      - last_enemy_damage(self) -> int
      - last_enemy_damage(self, value) -> None
      - score(self) -> int
      - score(self, value) -> None
      - best_score(self) -> int
      - best_score(self, value) -> None
      - key_bindings(self) -> dict[str, int]
      - _setup_level(self) -> None
      - apply_event_modifiers(self) -> None
      - _cycle_volume(self) -> None
      - _cycle_window_size(self) -> None
      - _cycle_display_mode(self) -> None
      - _cycle_hud_size(self) -> None
      - _apply_font_scale(self) -> None
      - _sync_player_selection_lists(self) -> None
      - _toggle_fullscreen(self) -> None
      - _apply_display_mode(self) -> pygame.Surface
      - _get_arena_backdrop(self) -> pygame.Surface
      - _get_ground_surface(self, width) -> pygame.Surface
      - _draw_stage_barriers(self) -> None
      - _draw_world_sprites(self, group) -> None
      - _draw_revive_glow(self, now) -> None
      - _apply_pending_respawn(self, now) -> None
      - _handle_fall_deaths(self, now) -> None
      - open_vote_menu(self) -> None
      - _set_state(self, state) -> None
      - _unlock_mmo(self) -> None
      - _ensure_mmo_world(self) -> None
      - _enter_mmo_mode(self) -> None
      - _mmo_nearest_region(self, pos) -> dict[str, object] | None
      - _mmo_regions(self) -> list[dict[str, object]]
      - _mmo_selected_region(self) -> dict[str, object] | None
      - _mmo_find_region(self, name) -> dict[str, object] | None
      - _mmo_region_distance(self, region, player_pos) -> float
      - _mmo_region_threat(self, region) -> float
      - _mmo_region_weather(self, region, now) -> tuple[str, list[str]]
      - _mmo_cycle_sort(self) -> None
      - _mmo_region_resources(self, region) -> tuple[str, int]
      - _mmo_infra_items(self) -> list[dict[str, object]]
      - _mmo_patrol_entries(self) -> list[dict[str, object]]
      - _mmo_set_waypoint_for_region(self, region_name) -> None
      - _mmo_collect_resource(self, resource, amount) -> None
      - _mmo_supply_tick(self) -> None
      - _mmo_survey_items(self) -> list[dict[str, object]]
      - _mmo_region_influence(self, region) -> tuple[str, int]
      - _mmo_add_shipment(self, resource, amount) -> None
      - _mmo_recipes(self) -> list[dict[str, object]]
      - _mmo_can_craft(self, recipe) -> bool
      - _mmo_start_craft(self, recipe) -> None
      - _mmo_market_tick(self) -> None
      - _mmo_crafting_tick(self) -> None
      - _mmo_post_order(self, resource) -> None
      - _mmo_record_stat(self, key, amount) -> None
      - _mmo_campaigns(self) -> list[dict[str, object]]
      - _mmo_update_campaigns(self) -> None
      - _mmo_timeline_items(self, now) -> list[dict[str, object]]
      - _mmo_region_events(self, region_name) -> list[dict[str, object]]
      - _mmo_region_contracts(self, region_name) -> list[dict[str, object]]
      - _mmo_seed_economy(self) -> None
      - _mmo_seed_operations(self) -> None
      - _mmo_append_operation(self) -> None
      - _mmo_seed_guilds(self) -> None
      - _mmo_seed_contracts(self) -> None
      - _mmo_append_contract(self) -> None
      - _mmo_seed_events(self) -> None
      - _mmo_spawn_world_event(self) -> None
      - _mmo_roster_entries(self) -> list[dict[str, object]]
      - _mmo_seed_expeditions(self) -> None
      - _mmo_redeploy_expedition(self, expedition, now) -> None
      - _mmo_update_expeditions(self, now) -> None
      - _mmo_add_alert(self, message) -> None
      - _mmo_flash_notice(self, message) -> None
      - _mmo_prune_alerts(self, now) -> None
      - _mmo_idle_agents(self) -> list[str]
      - _mmo_seed_directives(self) -> None
      - _mmo_assign_directive(self, directive) -> None
      - _mmo_update_directives(self, now) -> None
      - _mmo_seed_bounties(self) -> None
      - _mmo_assign_bounty(self, bounty) -> None
      - _mmo_update_bounties(self, now) -> None
      - _mmo_project_catalog(self) -> list[dict[str, object]]
      - _mmo_training_catalog(self) -> list[dict[str, object]]
      - _mmo_seed_projects(self) -> None
      - _mmo_append_project(self) -> None
      - _mmo_seed_training(self) -> None
      - _mmo_append_training(self) -> None
      - _mmo_start_training(self, training) -> None
      - _mmo_apply_training_reward(self, training) -> None
      - _mmo_update_training(self, now) -> None
      - _mmo_can_start_project(self, project) -> bool
      - _mmo_start_project(self, project) -> None
      - _mmo_apply_project_reward(self, project) -> None
      - _mmo_update_projects(self, now) -> None
      - _mmo_adjust_influence(self, region_name, delta) -> None
      - _mmo_influence_value(self, region) -> int
      - _mmo_influence_entries(self) -> list[dict[str, object]]
      - _mmo_update_influence(self, now) -> None
      - _mmo_toggle_shipment_escort(self, shipment) -> None
      - _update_mmo_world(self, now) -> None
      - _mmo_build_outpost(self, region) -> None
      - _mmo_open_trade_route(self, region) -> None
      - _mmo_dispatch_operation(self, region) -> None
      - _mmo_focus_selected(self) -> None
      - _mmo_cycle_filter(self) -> None
      - _mmo_toggle_favorite(self) -> None
      - _mmo_pulse_color(self, base, now, amount) -> tuple[int, int, int]
      - _mmo_draw_row_highlight(self, panel, y, height) -> None
      - _mmo_draw_status_badge(self, panel, y, status) -> None
      - _mmo_progress_ratio(self, item) -> float
      - _mmo_draw_progress_bar(self, x, y, width, height, ratio) -> None
      - _mmo_ensure_starfield(self) -> None
      - _mmo_draw_starfield(self) -> None
      - _mmo_help_pages(self) -> list[list[str]]
      - _mmo_draw_overlay_footer(self) -> None
      - _mmo_draw_tour(self) -> None
      - _mmo_set_waypoint(self) -> None
      - _mmo_clear_waypoint(self) -> None
      - _mmo_log_event(self, message) -> None
      - _mmo_floating_message(self, message) -> None
      - _mmo_notify(self, message) -> None
      - _mmo_draw_help(self) -> None
      - _mmo_draw_details(self, region) -> None
      - _mmo_draw_minimap(self, regions) -> None
      - _mmo_apply_action(self) -> None
      - _mmo_draw_event_log(self) -> None
      - _mmo_draw_flash_messages(self) -> None
      - _mmo_draw_floating_messages(self) -> None
      - _mmo_draw_notifications(self) -> None
      - _mmo_draw_market(self) -> None
      - _mmo_draw_factions(self) -> None
      - _mmo_draw_operations(self) -> None
      - _mmo_draw_hub_settings(self) -> None
      - _mmo_draw_guilds(self) -> None
      - _mmo_draw_events(self) -> None
      - _mmo_draw_contracts(self) -> None
      - _mmo_draw_intel(self) -> None
      - _mmo_draw_infrastructure(self) -> None
      - _mmo_draw_patrols(self) -> None
      - _mmo_draw_timeline(self) -> None
      - _mmo_draw_logistics(self) -> None
      - _mmo_draw_survey(self) -> None
      - _mmo_draw_diplomacy(self) -> None
      - _mmo_draw_research(self) -> None
      - _mmo_draw_crafting(self) -> None
      - _mmo_draw_market_orders(self) -> None
      - _mmo_draw_strategy(self) -> None
      - _mmo_draw_campaign(self) -> None
      - _mmo_tab_layout(self) -> tuple[list[list[tuple[str, str, str]]], int]
      - _mmo_draw_tab_bar(self) -> None
      - _mmo_draw_favorites(self) -> None
      - _clear_mmo_toggles(self) -> None
      - _mmo_draw_quest_log(self) -> None
      - _mmo_draw_growth_report(self) -> None
      - _mmo_draw_party(self) -> None
      - _mmo_draw_network_status(self) -> None
      - _mmo_draw_expeditions(self) -> None
      - _mmo_draw_roster(self) -> None
      - _mmo_draw_command(self) -> None
      - _mmo_draw_bounties(self) -> None
      - _mmo_draw_fleet(self) -> None
      - _mmo_draw_projects(self) -> None
      - _mmo_draw_academy(self) -> None
      - _mmo_draw_influence(self) -> None
      - _mmo_draw_alerts(self) -> None
      - _mmo_draw_panel(self, regions) -> None
      - _update_mmo_controls(self) -> None
      - _mmo_sync_region(self) -> None
      - _mmo_spawn_region(self) -> None
      - _bump_ai_progression(self) -> None
      - _log_ai_experience(self) -> None
      - _setup_mmo_agents(self) -> None
      - _update_mmo_agents(self) -> None
      - _autoplay_mmo(self, now) -> None
      - _autoplay_mmo_overlays(self, now) -> None
      - _autoplay_mmo_cycle_aux(self, overlay) -> tuple[str | None, ...]
      - _autoplay_generation(self, now) -> None
      - _mmo_generate_plan(self, now) -> None
      - _mmo_extend_pipeline(self, now) -> str
      - _mmo_award_arena_grant(self) -> str
      - _build_post_victory_report(self, now) -> None
      - _mmo_remote_state(self, player_id) -> SharedStateManager
      - _broadcast_mmo_state(self, delta) -> None
      - _mmo_sync_state(self, now) -> None
      - _victory_report_lines(self) -> list[str]
      - _victory_briefing_lines(self) -> list[str]
      - _draw_victory_report(self) -> None
      - _draw_victory_briefing(self) -> None
      - _draw_victory_actions(self) -> None
      - _draw_mmo_world(self) -> None
      - _autoplay_menu_flow(self, now) -> None
      - apply_vote_balancing(self, character_name, character) -> None
      - _quick_start(self) -> None
      - _goals_menu_options(self) -> list[str]
      - _info_menu_options(self, state) -> list[str]
      - _page_option_labels(self) -> set[str]
      - _page_count(self, total, page_size) -> int
      - _character_filter_label(self) -> str
      - _map_filter_label(self) -> str
      - _character_preview_data(self, name) -> dict[str, object]
      - _character_role_from_stats(self, attack, defense, mana, speed) -> str
      - _filtered_characters(self) -> list[str]
      - _cycle_character_filter(self) -> None
      - _map_preview_data(self, name) -> dict[str, object]
      - _chapter_preview_data(self, name) -> dict[str, object]
      - _map_matches_filter(self, name, data) -> bool
      - _filtered_maps(self) -> list[str]
      - _cycle_map_filter(self) -> None
      - _paged_characters(self) -> list[str]
      - _paged_maps(self) -> list[str]
      - _character_menu_options(self) -> list[str]
      - _map_menu_options(self) -> list[str]
      - _victory_menu_options(self) -> list[str]
      - _victory_actions_options(self) -> list[str]
      - _menu_options_for_state(self, state) -> list[str] | None
      - _handle_menu_selection(self, options) -> None
      - _autoplay_complete_rebind(self) -> None
      - _autoplay_menu_choice_order(self, options) -> list[str]
      - _autoplay_preview_items(self) -> list[str]
      - _autoplay_state_complete(self, state) -> bool
      - _autoplay_collection_complete(self, state) -> bool
      - _autoplay_vote_category_complete(self, category) -> bool
      - _autoplay_vote_complete(self) -> bool
      - _autoplay_menu_playing(self, now) -> bool
      - _autoplay_update_learning(self, now) -> None
      - _autoplay_monitor(self, now) -> None
      - _autoplay_trace(self, message) -> None
      - _autoplay_log(self, line) -> None
      - _autoplay_record_feature(self, name) -> None
      - _autoplay_trace_inputs(self, pressed_keys, actions, now) -> None
      - _draw_autoplay_trace(self) -> None
      - execute_account_option(self, option) -> None
      - start_node(self) -> None
      - stop_node(self) -> None
      - _poll_network(self) -> None
      - _trigger_holo_hype(self, now) -> None
      - _end_holo_hype(self) -> None
      - _draw_holo_hype_banner(self, now) -> None
      - _spawn_holo_cheer(self, text, pos) -> None
      - _draw_stage_ribbons(self, now) -> None
      - _draw_holo_spotlight(self, now) -> None
      - _draw_stage_lights(self, now) -> None
      - _draw_holo_sparkles(self, now) -> None
      - _draw_holo_confetti(self, now) -> None
      - _draw_fan_glow(self, now) -> None
      - _draw_holo_highlight(self, now) -> None
      - _draw_arena_intro(self, now) -> None
      - _draw_fan_sign_wave(self, now) -> None
      - _draw_audience_wave(self, now) -> None
      - _draw_arena_corner_badge(self, now) -> None
      - _handle_collisions(self) -> None
      - _handle_powerup_collision(self) -> None
      - _apply_objective_rewards(self, rewards) -> None
      - run(self)
      - _hud_resource_summary(self) -> list[tuple[str, object]]
      - _hud_status_effects(self, now) -> list[dict[str, object]]
      - _hud_insights(self) -> list[str]
      - _hud_network_line(self) -> str | None
      - _hud_auto_dev_summary(self) -> list[tuple[str, object]]
      - _hud_minimap_data(self) -> dict[str, object] | None
      - _hud_world_activity(self) -> list[str]
- functions:
  - load_character_names() -> list[str]
  - main()

### `hololive_coliseum\game_state_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - GameStateManager (bases: (none))
    doc: Simple helper to track the current and previous game states.
    class_vars:
      - (none)
    methods:
      - __init__(self, initial) -> None
      - change(self, state) -> None
      - revert(self) -> None
- functions:
  - (none)

### `hololive_coliseum\gathering_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - GatheringManager (bases: (none))
    doc: Generate resource nodes and gather items via a timing mini-game.
    class_vars:
      - (none)
    methods:
      - __init__(self, profession_manager, inventory) -> None
      - add_resource(self, name, common, rare) -> None
      - gather(self, name, timing) -> str | None
- functions:
  - (none)

### `hololive_coliseum\geo_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - GeoManager (bases: (none))
    doc: Track GPS coordinates for AR-style events.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - update(self, lat, lon) -> None
      - last(self)
- functions:
  - (none)

### `hololive_coliseum\goal_analysis_manager.py`

- docstring: Analyze `.gguf` snapshot chains to mark completed goals.  This manager simulates running an auxiliary neural network over a series of saved game snapshots.  For the prototype it simply searches for goal text inside each `.gguf` file, but the structure allows a real model to be plugged in later.
- imports:
  - __future__
  - pathlib
  - typing
- globals:
  - (none)
- classes:
  - GoalAnalysisManager (bases: (none))
    doc: Determines which goals have been satisfied by examining snapshots.
    class_vars:
      - (none)
    methods:
      - __init__(self, goal_file)
      - analyze(self, snapshots) -> Dict[str, bool]
      - _load_goals(self) -> list[str]
      - mark_completed(self, completion) -> None
- functions:
  - (none)

### `hololive_coliseum\gravity_zone.py`

- docstring: (none)
- imports:
  - pygame
- globals:
  - (none)
- classes:
  - GravityZone (bases: pygame.sprite.Sprite)
    doc: Rectangular zone that modifies gravity for sprites inside it.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, multiplier) -> None
- functions:
  - (none)

### `hololive_coliseum\guild_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - GuildManager (bases: (none))
    doc: Track multiple guilds and their member ranks.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - create(self, name, owner) -> None
      - delete(self, name) -> None
      - add_member(self, guild, user, rank) -> None
      - remove_member(self, guild, user) -> None
      - set_rank(self, guild, user, rank) -> None
      - get_rank(self, guild, user)
      - list_members(self, guild)
      - list_guilds(self)
- functions:
  - (none)

### `hololive_coliseum\hazard_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - HazardManager (bases: (none))
    doc: Manage hazard sprites, apply effects, and log interactions.
    class_vars:
      - (none)
    methods:
      - __init__(self, status_manager, analytics, objective_manager)
      - set_damage_multiplier(self, multiplier) -> None
      - set_analytics(self, analytics) -> None
      - set_objective_manager(self, objective_manager) -> None
      - _record_hazard(self, hazard, label) -> None
      - _scaled_damage(self, base) -> int
      - load_from_data(self, hazard_data)
      - apply_to_player(self, player, now)
      - apply_to_enemy(self, enemy, now)
      - clear(self)
- functions:
  - (none)

### `hololive_coliseum\hazards.py`

- docstring: (none)
- imports:
  - pygame
- globals:
  - (none)
- classes:
  - SpikeTrap (bases: pygame.sprite.Sprite)
    doc: Rectangular hazard that damages sprites on contact.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, damage) -> None
  - IceZone (bases: pygame.sprite.Sprite)
    doc: Zone with slippery surface reducing friction.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, friction) -> None
  - LavaZone (bases: pygame.sprite.Sprite)
    doc: Hazard zone that deals periodic damage while touched.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, damage, interval) -> None
  - AcidPool (bases: pygame.sprite.Sprite)
    doc: Hazard zone that damages and slows sprites.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, damage, interval, friction) -> None
  - PoisonZone (bases: pygame.sprite.Sprite)
    doc: Hazard zone that poisons sprites for damage over time.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect) -> None
  - FireZone (bases: pygame.sprite.Sprite)
    doc: Hazard zone that ignites sprites causing burn damage.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect) -> None
  - FrostZone (bases: pygame.sprite.Sprite)
    doc: Hazard zone that freezes sprites temporarily.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, duration) -> None
  - QuicksandZone (bases: pygame.sprite.Sprite)
    doc: Hazard zone that drags sprites downward and slows movement.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, pull, friction) -> None
  - LightningZone (bases: pygame.sprite.Sprite)
    doc: Hazard zone that periodically zaps and knocks sprites upward.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, damage, interval, force) -> None
  - BouncePad (bases: pygame.sprite.Sprite)
    doc: Pad that launches sprites upward when touched.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, force) -> None
  - TeleportPad (bases: pygame.sprite.Sprite)
    doc: Pad that relocates sprites to a target position.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, target) -> None
  - WindZone (bases: pygame.sprite.Sprite)
    doc: Zone that pushes sprites horizontally.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, force) -> None
  - SilenceZone (bases: pygame.sprite.Sprite)
    doc: Hazard zone that temporarily blocks special attacks.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, duration) -> None
  - RegenZone (bases: pygame.sprite.Sprite)
    doc: Area that restores health to sprites standing inside.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, heal, interval) -> None
- functions:
  - (none)

### `hololive_coliseum\healing_zone.py`

- docstring: (none)
- imports:
  - math
  - pygame
- globals:
  - (none)
- classes:
  - HealingZone (bases: pygame.sprite.Sprite)
    doc: Zone that heals players standing inside it.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, heal_rate, duration) -> None
      - update(self) -> None
- functions:
  - (none)

### `hololive_coliseum\health_manager.py`

- docstring: (none)
- imports:
  - pygame
- globals:
  - (none)
- classes:
  - HealthManager (bases: (none))
    doc: Track, modify and regenerate a character's health.
    class_vars:
      - (none)
    methods:
      - __init__(self, max_health) -> None
      - take_damage(self, amount, blocking, parrying, now) -> int
      - heal(self, amount) -> int
      - update(self, now) -> int
- functions:
  - (none)

### `hololive_coliseum\holographic_compression.py`

- docstring: Holographic packet compression with anchors and lightweight encryption.
- imports:
  - base64
  - bz2
  - cryptography.hazmat.primitives
  - cryptography.hazmat.primitives.asymmetric
  - hashlib
  - json
  - lzma
  - math
  - os
  - typing
  - zlib
- globals:
  - ANCHOR
  - ANCHOR_POINTS
  - BUFFER_SIZE
- classes:
  - (none)
- functions:
  - _triangulation_profile(anchors) -> Dict[str, object]
  - _layer_metadata(raw) -> List[Dict[str, object]]
  - _spectral_hint(raw) -> Dict[str, float]
  - _phase_signature(raw) -> Dict[str, float]
  - _stability_index(anchors) -> float
  - _bandwidth_profile(layers, spectral, phase, payload_size) -> Dict[str, float]
  - _telemetry_signature(layers, spectral, phase) -> Dict[str, object]
  - _rle_encode(data) -> bytes
  - _rle_decode(data) -> bytes
  - _pointcloud_encode(data, buffer_size, level, algorithm) -> Tuple[str, str, str]
  - _pointcloud_decode(part1, part2, buffer_size, algorithm) -> bytes
  - _xor(data, key) -> bytes
  - compress_packet(msg, key, level, algorithm, sign_key) -> bytes
  - decompress_packet(packet, key) -> Dict[str, Any] | None

### `hololive_coliseum\housing_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - HousingManager (bases: (none))
    doc: Track player houses and data.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - add_house(self, player_id, data) -> None
      - get_house(self, player_id)
- functions:
  - (none)

### `hololive_coliseum\hud_manager.py`

- docstring: Draw the heads-up display showing player status, timer, score and overlays.
- imports:
  - __future__
  - collections.abc
  - math
  - pygame
- globals:
  - FLASH_DURATION
- classes:
  - HUDManager (bases: (none))
    doc: Render status bars, combos and the arena overlay panels.
    class_vars:
      - (none)
    methods:
      - __init__(self, font) -> None
      - _draw_text(self, screen, text, color, pos) -> None
      - _draw_panel(self, screen, rect) -> None
      - draw(self, screen, player, score, elapsed, combo, objectives, resource_summary, status_effects, insights, auto_dev_summary, world_activity, cooldowns, minimap, hype_meter, hype_label, threat_rating, threat_label) -> None
      - _draw_resource_panel(self, screen, summary) -> pygame.Rect
      - _draw_threat_chip(self, screen, threat, label) -> None
      - _draw_status_panel(self, screen, effects) -> None
      - _draw_insight_banner(self, screen, insights) -> None
      - _draw_auto_dev_panel(self, screen, summary, anchor) -> None
      - _draw_world_ticker(self, screen, events) -> None
      - _draw_combo_meter(self, screen, combo) -> None
      - _draw_hype_panel(self, screen, meter, label) -> None
      - _draw_cooldown_panel(self, screen, cooldowns, anchor) -> None
      - _draw_minimap(self, screen, data) -> pygame.Rect
- functions:
  - (none)

### `hololive_coliseum\input_manager.py`

- docstring: Helpers for querying keyboard and controller input bindings.
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - InputManager (bases: (none))
    doc: Store keyboard and controller bindings and check pressed actions.
    class_vars:
      - (none)
    methods:
      - __init__(self, key_bindings, controller_bindings, joysticks, mode) -> None
      - get(self, action) -> int | None
      - set(self, action, key) -> None
      - set_button(self, action, button) -> None
      - set_mode(self, mode) -> None
      - pressed(self, action, keys) -> bool
- functions:
  - (none)

### `hololive_coliseum\instance_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - InstanceManager (bases: (none))
    doc: Create and destroy simple gameplay instances.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - create(self, players) -> int
      - destroy(self, iid) -> None
- functions:
  - (none)

### `hololive_coliseum\interaction_generator.py`

- docstring: Generate simple interactable templates.
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - InteractionGenerator (bases: (none))
    doc: Create interaction records with unique names.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - create(self, base_name, message) -> dict[str, str]
- functions:
  - (none)

### `hololive_coliseum\interaction_manager.py`

- docstring: Manage simple interactable actions.
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - InteractionManager (bases: (none))
    doc: Register interactions and trigger their responses.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - register(self, interaction) -> None
      - interact(self, name) -> str
- functions:
  - (none)

### `hololive_coliseum\inventory_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - InventoryManager (bases: (none))
    doc: Track items collected during play.  An optional ``capacity`` limits how many total items may be stored. This mirrors inventory restrictions common in MMOs while keeping earlier levels lightweight.
    class_vars:
      - (none)
    methods:
      - __init__(self, capacity) -> None
      - total_items(self) -> int
      - add(self, item, count) -> bool
      - remove(self, item, count) -> bool
      - has(self, item) -> bool
      - count(self, item) -> int
      - to_dict(self) -> dict[str, int]
      - load_from_dict(self, data) -> None
- functions:
  - (none)

### `hololive_coliseum\item_manager.py`

- docstring: (none)
- imports:
  - dataclasses
- globals:
  - (none)
- classes:
  - Item (bases: (none))
    doc: Base item carrying a name, slot type and stat modifiers.
    class_vars:
      - name
      - slot
      - stats
    methods:
      - (none)
  - Weapon (bases: Item)
    doc: Weapon automatically assigned to the ``weapon`` slot.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Sword (bases: Weapon)
    doc: Classic melee blade.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Bow (bases: Weapon)
    doc: Ranged weapon using arrows.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Wand (bases: Weapon)
    doc: Mystic focus for spellcasters.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Axe (bases: Weapon)
    doc: Heavy chopping weapon.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Spear (bases: Weapon)
    doc: Long thrusting weapon.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Helmet (bases: Item)
    doc: Head gear that equips to the ``head`` slot.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Armor (bases: Item)
    doc: Body armor that equips to the ``chest`` slot.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Boots (bases: Item)
    doc: Footwear for the ``boots`` slot.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Shield (bases: Item)
    doc: Offhand equipment stored in the ``offhand`` slot.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Tome (bases: Item)
    doc: Magic book for the ``offhand`` slot.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Orb (bases: Item)
    doc: Mystic orb held in the ``offhand`` slot.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Quiver (bases: Item)
    doc: Arrow container for the ``offhand`` slot.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - Ring (bases: Item)
    doc: Accessory occupying the ``ring`` slot.
    class_vars:
      - (none)
    methods:
      - __init__(self, name, stats)
  - ItemManager (bases: (none))
    doc: Register and look up items by name.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_item(self, item) -> None
      - get(self, name) -> Item | None
      - list_items(self) -> list[Item]
- functions:
  - (none)

### `hololive_coliseum\iteration_manager.py`

- docstring: Save per-run game state snapshots for future upgrades.
- imports:
  - __future__
  - json
  - os
  - time
  - typing
- globals:
  - (none)
- classes:
  - IterationManager (bases: (none))
    doc: Persist game state snapshots as timestamped `.gguf` files.
    class_vars:
      - (none)
    methods:
      - __init__(self, directory) -> None
      - save(self, state) -> str
      - list(self) -> List[str]
      - load(self, path) -> dict[str, Any]
- functions:
  - (none)

### `hololive_coliseum\keybind_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - KeybindManager (bases: (none))
    doc: Store and modify input bindings.
    class_vars:
      - (none)
    methods:
      - __init__(self, defaults)
      - get(self, action) -> int | None
      - set(self, action, key) -> None
      - reset(self) -> None
      - to_dict(self) -> dict[str, int]
      - load_from_dict(self, data) -> None
- functions:
  - (none)

### `hololive_coliseum\level_manager.py`

- docstring: (none)
- imports:
  - .gravity_zone
  - .platform
  - .player
  - .save_manager
- globals:
  - (none)
- classes:
  - LevelManager (bases: (none))
    doc: Handle level initialization and reset logic.
    class_vars:
      - (none)
    methods:
      - __init__(self, game)
      - setup_level(self) -> None
- functions:
  - (none)

### `hololive_coliseum\leveling_manager.py`

- docstring: Track MMO player experience and levels.
- imports:
  - .experience_manager
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - LevelingManager (bases: (none))
    doc: Store :class:`ExperienceManager` instances for MMO players.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - _get_mgr(self, player_id) -> ExperienceManager
      - add_xp(self, player_id, amount) -> bool
      - get_level(self, player_id) -> int
      - get_xp(self, player_id) -> int
- functions:
  - (none)

### `hololive_coliseum\load_balancer_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - LoadBalancerManager (bases: (none))
    doc: Select the least busy server for new matches.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - update_load(self, server, load) -> None
      - best_server(self) -> str | None
- functions:
  - (none)

### `hololive_coliseum\localization_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - LocalizationManager (bases: (none))
    doc: Provide basic string localization using language dictionaries.
    class_vars:
      - (none)
    methods:
      - __init__(self, default_lang) -> None
      - set(self, lang, key, text) -> None
      - translate(self, key, lang) -> str
- functions:
  - (none)

### `hololive_coliseum\logging_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - LoggingManager (bases: (none))
    doc: Collect log events for later analysis.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - log(self, event) -> None
- functions:
  - (none)

### `hololive_coliseum\loot_manager.py`

- docstring: (none)
- imports:
  - random
- globals:
  - (none)
- classes:
  - LootManager (bases: (none))
    doc: Generate loot drops using simple tables.
    class_vars:
      - (none)
    methods:
      - __init__(self, tables) -> None
      - add_table(self, enemy_type, drops) -> None
      - roll_loot(self, enemy_type)
- functions:
  - (none)

### `hololive_coliseum\mail_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - MailManager (bases: (none))
    doc: Simple per-user mailbox.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - send_mail(self, to, message) -> None
      - inbox(self, user)
      - clear(self, user) -> None
- functions:
  - (none)

### `hololive_coliseum\mana_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ManaManager (bases: (none))
    doc: Track and spend a character's mana resource.
    class_vars:
      - (none)
    methods:
      - __init__(self, max_mana) -> None
      - use(self, amount) -> bool
      - regen(self, amount) -> int
- functions:
  - (none)

### `hololive_coliseum\map_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - MapManager (bases: (none))
    doc: Store available maps with hazard definitions and track the active one.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_map(self, name, data) -> None
      - set_current(self, name) -> bool
      - get_current(self) -> dict | None
- functions:
  - (none)

### `hololive_coliseum\matchmaking_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - MatchmakingManager (bases: (none))
    doc: Pair players into groups for matches.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - join(self, player_id) -> None
      - match(self, size) -> list[str] | None
- functions:
  - (none)

### `hololive_coliseum\melee_attack.py`

- docstring: (none)
- imports:
  - pygame
- globals:
  - MELEE_LIFETIME
  - MELEE_SIZE
- classes:
  - MeleeAttack (bases: pygame.sprite.Sprite)
    doc: Temporary hitbox representing a melee swing.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, facing, owner, from_enemy) -> None
      - update(self) -> None
- functions:
  - (none)

### `hololive_coliseum\menu_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - MenuManager (bases: (none))
    doc: Track the current menu index and provide navigation helpers.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - reset(self) -> None
      - move(self, direction, count) -> None
- functions:
  - (none)

### `hololive_coliseum\menus.py`

- docstring: Menu rendering helpers used by :class:`~hololive_coliseum.game.Game`.
- imports:
  - __future__
  - math
  - pathlib
  - pygame
  - random
- globals:
  - MENU_BG_COLOR
  - MENU_BORDER_COLOR
  - MENU_HIGHLIGHT_COLOR
  - MENU_TEXT_COLOR
- classes:
  - MenuMixin (bases: (none))
    doc: Provides drawing helpers for the game's various menus.
    class_vars:
      - (none)
    methods:
      - _menu_pattern_surface(self) -> pygame.Surface
      - _draw_menu_emblem(self) -> None
      - _draw_menu_emblem_triangles(self, surface, center, palette, now) -> None
      - _menu_contrast_enabled(self) -> bool
      - _menu_palette(self) -> dict[str, tuple[int, int, int]]
      - _draw_background(self) -> None
      - _draw_ambient_glow(self) -> None
      - _draw_menu_particles(self) -> None
      - _draw_menu_vignette(self) -> None
      - _draw_option_label(self, label, idx, center) -> None
      - _draw_icon_glow(self, rect) -> None
      - _draw_title(self, text, center) -> None
      - _draw_border(self) -> None
      - _draw_input_prompt(self, text) -> None
      - _draw_menu_header(self, title) -> None
      - _draw_menu_badges(self, banner_height, palette) -> None
      - _draw_panel_sheen(self, rect) -> None
      - _draw_panel_shadow(self, rect) -> None
      - _draw_end_flash(self, until, color) -> None
      - _draw_summary_cards(self, entries) -> None
      - _draw_menu(self) -> None
      - _draw_main_menu(self) -> None
      - _draw_option_menu(self, title, options) -> None
      - _draw_character_menu(self) -> None
      - _draw_map_menu(self) -> None
      - _draw_chapter_menu(self) -> None
      - _draw_settings_menu(self) -> None
      - _draw_key_bindings_menu(self) -> None
      - _draw_controller_bindings_menu(self) -> None
      - _draw_rebind_prompt(self) -> None
      - _draw_rebind_controller_prompt(self) -> None
      - _draw_node_menu(self) -> None
      - _draw_accessibility_menu(self) -> None
      - _draw_accounts_menu(self) -> None
      - _draw_lobby_menu(self) -> None
      - _draw_pause_menu(self) -> None
      - _draw_game_over_menu(self) -> None
      - _draw_victory_menu(self) -> None
      - _draw_inventory_menu(self) -> None
      - _draw_equipment_menu(self) -> None
      - _draw_how_to_play(self) -> None
      - _draw_credits(self) -> None
      - _draw_goals_menu(self) -> None
      - _draw_scoreboard_menu(self) -> None
      - _draw_achievements_menu(self) -> None
- functions:
  - (none)

### `hololive_coliseum\migration_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - MigrationManager (bases: (none))
    doc: Handle player transfers between servers.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - request_transfer(self, user_id, dest) -> None
      - complete_transfer(self, user_id) -> str | None
- functions:
  - (none)

### `hololive_coliseum\minigame_manager.py`

- docstring: Mini-games that award bonuses for quick reactions.
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ReactionMinigame (bases: (none))
    doc: Reaction test that awards a crafting material on success.
    class_vars:
      - (none)
    methods:
      - __init__(self, target_ms, material, inventory, tolerance) -> None
      - attempt(self, reaction_ms) -> str | None
  - MinigameManager (bases: (none))
    doc: Run small standalone mini-games.
    class_vars:
      - (none)
    methods:
      - play_reaction(self, target_ms, reaction_ms, material, inventory) -> str | None
- functions:
  - (none)

### `hololive_coliseum\mining_manager.py`

- docstring: Background proof-of-work mining used to grow future MMORPG features.
- imports:
  - .blockchain
  - .world_generation_manager
  - .world_seed_manager
  - __future__
  - threading
  - time
  - typing
- globals:
  - (none)
- classes:
  - MiningManager (bases: (none))
    doc: Run a lightweight mining loop in a background thread.  When enabled, the manager repeatedly performs proof-of-work on dummy blocks to generate hashes for the expanding game world. The workload is extremely small but demonstrates how clients could volunteer spare resources for world generation in later iterations of the project. When supplied with a :class:`WorldGenerationManager`, each mined hash immediately spawns a new region so the MMO can grow on its own.
    class_vars:
      - (none)
    methods:
      - __init__(self, seed_manager, world_gen, player_id) -> None
      - start(self, intensity) -> None
      - _mine_loop(self, delay) -> None
      - stop(self) -> None
- functions:
  - (none)

### `hololive_coliseum\mmo_backend_manager.py`

- docstring: SQLite-backed storage for MMO hub state, players, and regions.
- imports:
  - __future__
  - json
  - os
  - sqlite3
  - time
  - typing
- globals:
  - (none)
- classes:
  - MMOBackendManager (bases: (none))
    doc: Persist MMO hub data and snapshots in a lightweight SQLite database.
    class_vars:
      - (none)
    methods:
      - __init__(self, path) -> None
      - _configure(self) -> None
      - _migrate(self) -> None
      - upsert_player(self, player_id, pos) -> None
      - upsert_regions(self, regions) -> None
      - record_snapshot(self, sequence, state, digests) -> None
      - prune_snapshots(self, keep) -> None
      - latest_snapshot(self) -> dict[str, Any] | None
      - record_plan(self, summary, plan) -> None
      - latest_plan(self) -> dict[str, Any] | None
      - upsert_outpost(self, outpost) -> None
      - record_route(self, route) -> None
      - record_operation(self, operation) -> None
      - close(self) -> None
- functions:
  - (none)

### `hololive_coliseum\mmo_builder.py`

- docstring: Helpers to assemble core MMO managers automatically.  `MMOBuilder` instantiates a set of managers that power the self-building MMO systems. It wires together world seed, generation, region, player and voting managers so games can start with minimal setup code.
- imports:
  - .voting_manager
  - .world_generation_manager
  - .world_player_manager
  - .world_region_manager
  - .world_seed_manager
  - __future__
  - dataclasses
- globals:
  - (none)
- classes:
  - MMOBuilder (bases: (none))
    doc: Constructs the core managers for the MMO subsystems.
    class_vars:
      - (none)
    methods:
      - build(self) -> dict[str, object]
- functions:
  - (none)

### `hololive_coliseum\mount_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - MountManager (bases: (none))
    doc: Store mounts and track which is active for each player.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - add_mount(self, player_id, mount) -> None
      - set_active(self, player_id, mount) -> bool
      - get_active(self, player_id)
- functions:
  - (none)

### `hololive_coliseum\name_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - NameManager (bases: (none))
    doc: Handle naming conventions and renames.
    class_vars:
      - (none)
    methods:
      - __init__(self, name) -> None
      - rename(self, new_name) -> None
- functions:
  - (none)

### `hololive_coliseum\network.py`

- docstring: Networking helpers for discovery and game state synchronization.  Packets include a claimed sender ID and the manager cross-checks it against the socket address to provide basic anti-spoofing protection. After a brief handshake, all packets carry a session token so unsolicited traffic is ignored.
- imports:
  - .ban_manager
  - .blockchain
  - .data_protection_manager
  - .node_manager
  - .save_manager
  - .state_sync
  - .sync_manager
  - json
  - os
  - socket
  - time
  - typing
  - uuid
- globals:
  - (none)
- classes:
  - NetworkManager (bases: (none))
    doc: Simple UDP networking manager for multiplayer.  Hosts respond to broadcast discovery packets so clients can automatically find available games on the local network. Router nodes keep track of game hosts **and** individual clients so the mesh knows which players are online at any moment. After an initial handshake, peers exchange a session token which is attached to all future packets so strangers cannot inject data. Hosts consult a ban list to drop packets from abusive IDs. Compression, encryption and signing are performed via a dedicated :class:`DataProtectionManager` instance for efficient packet handling that can also strip sensitive fields before encoding. State updates run through :class:`StateSync` which supports per-field tolerances to avoid transmitting insignificant changes.
    class_vars:
      - (none)
    methods:
      - __init__(self, host, address, secret, encrypt_key, sign_key, relay_mode, relay_addr, node_manager, tolerances, rate_limit, sanitize_fields, client_id, ban_manager) -> None
      - _encode(self, msg) -> bytes
      - _decode(self, data) -> dict[str, Any] | None
      - rotate_keys(self, key, secret, sign_key) -> None
      - broadcast_announce(self, nodes) -> None
      - register_game(self, nodes) -> None
      - register_client(self, nodes) -> None
      - unregister_client(self, nodes) -> None
      - refresh_nodes(self) -> None
      - broadcast_games(self, nodes) -> None
      - broadcast_clients(self, nodes) -> None
      - broadcast_relays(self, nodes) -> None
      - broadcast_nodes(self, targets) -> None
      - broadcast_block(self, block, nodes) -> None
      - send_chain(self, addr) -> None
      - offer_relay(self, nodes) -> None
      - request_relays(node, timeout, process_host, secret) -> List[Tuple[str, int]]
      - request_chain(node, timeout, process_host, secret) -> List[dict[str, Any]]
      - send_via_relay(self, data, dest) -> None
      - _normalize_addr(addr) -> Tuple[str, int]
      - broadcast_records(self, best_time, best_score, nodes) -> None
      - request_games(node, timeout, process_host, secret) -> List[Tuple[str, int]]
      - request_clients(node, timeout, process_host, secret) -> List[Tuple[str, int]]
      - request_nodes(node, timeout, process_host, secret) -> List[Tuple[str, int]]
      - sync_time(node, timeout, process_host, secret) -> float | None
      - send_state(self, data) -> None
      - send_reliable(self, data, addr, max_retries, importance) -> None
      - send_chat(self, user, msg, addr, reliable) -> None
      - process_reliable(self) -> None
      - poll(self) -> List[Tuple[Tuple[str, int], dict[str, Any]]]
      - discover(timeout, port, broadcast_address, process_host, secret) -> List[Tuple[str, int]]
      - ping_node(addr, timeout, process_host, secret) -> float | None
      - select_best_node(nodes, ping_func, timeout) -> Tuple[str, int] | None
- functions:
  - (none)

### `hololive_coliseum\node_manager.py`

- docstring: (none)
- imports:
  - .node_registry
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - NodeManager (bases: (none))
    doc: Wrapper class managing known network nodes.
    class_vars:
      - (none)
    methods:
      - load_nodes(self) -> List[Tuple[str, int]]
      - save_nodes(self, nodes) -> None
      - add_node(self, node) -> None
      - prune_nodes(self, ping_func, timeout) -> None
- functions:
  - (none)

### `hololive_coliseum\node_registry.py`

- docstring: (none)
- imports:
  - json
  - os
  - typing
- globals:
  - DEFAULT_NODES
  - NODES_FILE
  - SAVE_DIR
- classes:
  - (none)
- functions:
  - load_nodes() -> List[Tuple[str, int]]
  - save_nodes(nodes) -> None
  - add_node(node) -> None
  - prune_nodes(ping_func, timeout) -> None

### `hololive_coliseum\notification_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - NotificationManager (bases: (none))
    doc: Manage popup notifications for the UI.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - push(self, message) -> None
      - pop(self)
- functions:
  - (none)

### `hololive_coliseum\npc_manager.py`

- docstring: (none)
- imports:
  - pygame
- globals:
  - (none)
- classes:
  - NPCManager (bases: (none))
    doc: Maintain groups of enemies and allied NPCs.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - clear(self) -> None
      - add_enemy(self, sprite) -> None
      - add_ally(self, sprite) -> None
- functions:
  - (none)

### `hololive_coliseum\objective_manager.py`

- docstring: Track rotating arena objectives linked to MMO world regions.
- imports:
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - Objective (bases: (none))
    doc: Store progress for a single arena objective.
    class_vars:
      - description
      - key
      - progress
      - rewarded
      - rewards
      - scope
      - target
    methods:
      - to_dict(self) -> Dict[str, object]
      - from_dict(cls, key, data) -> 'Objective'
      - record(self, amount) -> None
      - completed(self) -> bool
  - ObjectiveManager (bases: (none))
    doc: Coordinate rotating objectives for the arena and MMO.
    class_vars:
      - EVENT_MAP
      - ORDER
    methods:
      - __init__(self) -> None
      - load_from_dict(self, data) -> None
      - to_dict(self) -> Dict[str, object]
      - ensure_region_objectives(self, region, fallback_name) -> None
      - record_event(self, event, amount) -> List[Dict[str, int]]
      - summary(self, limit) -> List[str]
- functions:
  - (none)

### `hololive_coliseum\onboarding_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - OnboardingManager (bases: (none))
    doc: Guide new players through initial setup.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - show(self, step) -> None
      - history(self)
- functions:
  - (none)

### `hololive_coliseum\party_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - PartyManager (bases: (none))
    doc: Handle party invites and membership.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - create_party(self, host) -> None
      - join(self, host, member) -> None
      - get_party(self, host)
- functions:
  - (none)

### `hololive_coliseum\patch_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - PatchManager (bases: (none))
    doc: Store the current client version and hotfix level.
    class_vars:
      - (none)
    methods:
      - __init__(self, version) -> None
      - update_version(self, version) -> None
- functions:
  - (none)

### `hololive_coliseum\pet_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - PetManager (bases: (none))
    doc: Manage collectible pets for each player.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - add_pet(self, player_id, pet) -> None
      - list_pets(self, player_id)
- functions:
  - (none)

### `hololive_coliseum\physics.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - AIR_FRICTION
  - GRAVITY
  - GROUND_FRICTION
  - MAX_FALL_SPEED
  - MAX_MOVE_SPEED
  - MOVE_ACCEL
- classes:
  - (none)
- functions:
  - apply_gravity(vy, multiplier) -> float
  - accelerate(vx, direction) -> float
  - apply_friction(vx, on_ground, multiplier) -> float

### `hololive_coliseum\placeholder_sprites.py`

- docstring: Create placeholder sprite files at runtime when assets are missing.
- imports:
  - __future__
  - math
  - os
  - pygame
  - typing
- globals:
  - DEFAULT_SIZE
  - MAP_SIZE
- classes:
  - (none)
- functions:
  - ensure_placeholder_sprites(image_dir, character_names, chapter_count, enemy_names, map_names, force) -> None
  - _filename_base(name) -> str
  - _short_label(name, limit) -> str
  - _map_filename(name) -> str
  - _create_sprite_pair(image_dir, base, label, theme_name, force) -> None
  - _create_single(image_dir, filename, label, size, color, direction, theme_name, force) -> None
  - _render_label(surface, label) -> None
  - _paint_gradient(surface, color) -> None
  - _accent_palette(base) -> tuple[tuple[int, int, int], tuple[int, int, int]]
  - _paint_panels(surface, accent, shade) -> None
  - _paint_highlights(surface) -> None
  - _paint_badge_stripes(surface, accent) -> None
  - _paint_emblem(surface, direction, accent, motif) -> None
  - _paint_motif(surface, motif, center, radius) -> None
  - _motif_for_name(name) -> str
  - _paint_frame(surface, shade) -> None
  - _color_from_name(name) -> tuple[int, int, int]

### `hololive_coliseum\platform.py`

- docstring: (none)
- imports:
  - pygame
  - random
- globals:
  - (none)
- classes:
  - Platform (bases: pygame.sprite.Sprite)
    doc: Static platform that players and enemies can stand on.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, theme)
      - _build_surface(self, size, theme) -> pygame.Surface
      - _theme_colors(self, theme) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
  - MovingPlatform (bases: Platform)
    doc: Platform that moves back and forth along a vector.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, offset, speed) -> None
      - update(self) -> None
  - CrumblingPlatform (bases: Platform)
    doc: Platform that disappears shortly after being stepped on.
    class_vars:
      - (none)
    methods:
      - __init__(self, rect, delay) -> None
      - start_crumble(self) -> None
      - update(self) -> None
- functions:
  - (none)

### `hololive_coliseum\player.py`

- docstring: Player character implementations with movement and combat helpers.
- imports:
  - .currency_manager
  - .equipment_manager
  - .experience_manager
  - .health_manager
  - .inventory_manager
  - .mana_manager
  - .platform
  - .skill_manager
  - .stamina_manager
  - .stats_manager
  - __future__
  - os
  - pygame
  - random
- globals:
  - CHARACTER_CLASSES
  - DODGE_COOLDOWN
  - DODGE_DURATION
  - DODGE_SPEED
  - JUMP_VELOCITY
  - MAX_JUMPS
  - MELEE_COOLDOWN
  - MOVE_SPEED
  - PARRY_COOLDOWN
  - PARRY_DURATION
  - PROJECTILE_COOLDOWN
  - Player
  - SPECIAL_COOLDOWN
  - SPRINT_MULTIPLIER
  - STAMINA_COST_ATTACK
  - STAMINA_COST_BLOCK
  - STAMINA_COST_DODGE
  - STAMINA_COST_SPRINT
  - VFX_DIR
  - _VFX_CACHE
  - _VFX_FRAME_CACHE
- classes:
  - PlayerCharacter (bases: pygame.sprite.Sprite)
    doc: Base controllable character sprite.  Provides movement, combat mechanics and resource tracking. Subclasses override :py:meth:`special_attack` to implement unique abilities.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path, color) -> None
      - handle_input(self, keys, now, key_bindings, action_pressed) -> None
      - shoot(self, now, target)
      - melee_attack(self, now)
      - _special_impl(self, now)
      - special_attack(self, now)
      - parry(self, now) -> bool
      - dodge(self, now, direction) -> bool
      - apply_gravity(self) -> None
      - _is_invincible(self, now) -> bool
      - take_damage(self, amount) -> None
      - use_mana(self, amount) -> bool
      - use_stamina(self, amount) -> bool
      - regen_mana(self, amount) -> None
      - use_item(self, name) -> bool
      - health(self) -> int
      - health(self, value) -> None
      - mana(self) -> int
      - mana(self, value) -> None
      - draw_status(self, surface, x, y) -> None
      - draw_health_bar(self, surface, camera) -> None
      - cooldown_status(self, now) -> list[dict[str, object]]
      - gain_xp(self, amount) -> bool
      - set_gravity_multiplier(self, multiplier) -> None
      - set_friction_multiplier(self, multiplier) -> None
      - update(self, ground_y, now) -> None
      - begin_revive(self, spawn, now) -> None
  - GuraPlayer (bases: PlayerCharacter)
    doc: Player subclass implementing Gura's special trident attack.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - WatsonPlayer (bases: PlayerCharacter)
    doc: Watson Amelia with a time-dash special attack.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
      - update(self, ground_y, now) -> None
  - InaPlayer (bases: PlayerCharacter)
    doc: Ninomae Ina'nis with a tentacle grapple special attack.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - KiaraPlayer (bases: PlayerCharacter)
    doc: Takanashi Kiara's fiery leap that explodes on landing.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
      - update(self, ground_y, now) -> None
  - CalliopePlayer (bases: PlayerCharacter)
    doc: Mori Calliope's returning scythe projectile.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - FaunaPlayer (bases: PlayerCharacter)
    doc: Ceres Fauna creates a healing field to restore health.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - KroniiPlayer (bases: PlayerCharacter)
    doc: Ouro Kronii parry lasts longer as a special.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
      - update(self, ground_y, now) -> None
  - IRySPlayer (bases: PlayerCharacter)
    doc: IRyS deploys a shield that blocks projectiles.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
      - update(self, ground_y, now) -> None
  - MumeiPlayer (bases: PlayerCharacter)
    doc: Nanashi Mumei summons a slowing flock.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - BaelzPlayer (bases: PlayerCharacter)
    doc: Hakos Baelz triggers random chaos effects.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
      - update(self, ground_y, now) -> None
  - FubukiPlayer (bases: PlayerCharacter)
    doc: Shirakami Fubuki fires an ice shard that slows enemies.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - MatsuriPlayer (bases: PlayerCharacter)
    doc: Natsuiro Matsuri launches a firework that explodes overhead.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - MikoPlayer (bases: PlayerCharacter)
    doc: Sakura Miko fires a piercing beam that passes through enemies.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - AquaPlayer (bases: PlayerCharacter)
    doc: Minato Aqua fires a water blast that explodes.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - PekoraPlayer (bases: PlayerCharacter)
    doc: Usada Pekora tosses an explosive carrot.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - MarinePlayer (bases: PlayerCharacter)
    doc: Houshou Marine's anchor boomerang.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - SuiseiPlayer (bases: PlayerCharacter)
    doc: Hoshimachi Suisei shoots a piercing star.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - AyamePlayer (bases: PlayerCharacter)
    doc: Nakiri Ayame performs a swift dash.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
      - update(self, ground_y, now) -> None
  - NoelPlayer (bases: PlayerCharacter)
    doc: Shirogane Noel smashes the ground sending a shockwave forward.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - FlarePlayer (bases: PlayerCharacter)
    doc: Shiranui Flare fires a burning fireball.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - SubaruPlayer (bases: PlayerCharacter)
    doc: Oozora Subaru launches a stunning blast.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - SoraPlayer (bases: PlayerCharacter)
    doc: Tokino Sora unleashes a melodic note that weaves upward.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path) -> None
      - _special_impl(self, now)
  - Enemy (bases: PlayerCharacter)
    doc: AI controlled opponent sharing the player mechanics.
    class_vars:
      - AI_LEVELS
    methods:
      - __init__(self, x, y, image_path, difficulty, faction, reputation_reward) -> None
      - _special_impl(self, now)
      - take_damage(self, amount) -> None
      - _patrol(self, settings) -> None
      - shoot(self, now, target)
      - melee_attack(self, now)
      - handle_ai(self, target, now, hazards, projectiles)
  - BossEnemy (bases: Enemy)
    doc: Enemy variant used for boss fights with periodic special attacks.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, image_path, difficulty, faction, reputation_reward) -> None
      - _special_impl(self, now)
      - handle_ai(self, target, now, hazards, projectiles)
- functions:
  - _load_vfx_surface(name, size, draw_fn) -> pygame.Surface
  - _load_vfx_frames(name, size, draw_fn, frame_count) -> list[pygame.Surface]
  - _load_vfx_frameset(name, size, draw_fn, frame_count) -> tuple[pygame.Surface, list[pygame.Surface]]
  - _apply_vfx_sequence(sprite, name, size, draw_fn) -> None
  - character_class_exists(name) -> bool
  - get_player_class(name) -> type[PlayerCharacter]

### `hololive_coliseum\powerup.py`

- docstring: Power-up sprites that grant health, mana, stamina, speed, shield, attack, defense, experience or extra lives.
- imports:
  - math
  - pygame
- globals:
  - (none)
- classes:
  - PowerUp (bases: pygame.sprite.Sprite)
    doc: Simple powerup that restores health, mana, stamina, speed, attack, defense, experience or grants a shield or extra life.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, effect) -> None
      - _build_sprite(self, effect) -> pygame.Surface
      - _colors_for_effect(self, effect) -> tuple[tuple[int, int, int], tuple[int, int, int]]
      - _draw_icon(self, surface, effect, color) -> None
      - update(self) -> None
- functions:
  - (none)

### `hololive_coliseum\profession_manager.py`

- docstring: (none)
- imports:
  - collections
- globals:
  - (none)
- classes:
  - ProfessionManager (bases: (none))
    doc: Track profession experience and provide levels.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - gain_xp(self, profession, amount) -> None
      - level_of(self, profession) -> int
- functions:
  - (none)

### `hololive_coliseum\projectile.py`

- docstring: (none)
- imports:
  - math
  - pygame
- globals:
  - EXPLODE_TIME
  - PROJECTILE_SPEED
- classes:
  - Projectile (bases: pygame.sprite.Sprite)
    doc: Simple projectile moving in a given direction.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction, from_enemy, owner) -> None
      - set_animation(self, style, color, speed) -> None
      - set_frame_animation(self, frames) -> None
      - _apply_image(self, image) -> None
      - _animate(self) -> None
      - update(self) -> None
  - VisualEffect (bases: Projectile)
    doc: Short-lived visual-only sprite for special attacks.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, size, color, duration, follow, style, image, frames, frame_ms) -> None
      - update(self) -> None
  - ExplodingProjectile (bases: Projectile)
    doc: Projectile that disappears after a short duration.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
      - update(self) -> None
  - GrappleProjectile (bases: Projectile)
    doc: Projectile that pulls enemies toward the shooter on contact.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
  - BoomerangProjectile (bases: Projectile)
    doc: Projectile that returns to the shooter after a short delay.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction, owner) -> None
      - update(self) -> None
  - ExplosionProjectile (bases: Projectile)
    doc: Short-lived projectile that damages enemies in an area.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, radius) -> None
      - update(self) -> None
  - FreezingProjectile (bases: Projectile)
    doc: Projectile that slows enemies on hit.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
  - FlockProjectile (bases: Projectile)
    doc: Projectile that slows enemies by summoning a flock.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
  - PiercingProjectile (bases: Projectile)
    doc: Projectile that passes through enemies instead of disappearing.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
  - PoisonProjectile (bases: Projectile)
    doc: Projectile that poisons enemies on hit.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
  - BurningProjectile (bases: ExplodingProjectile)
    doc: Projectile that ignites enemies causing burn damage.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
  - StunningProjectile (bases: ExplodingProjectile)
    doc: Projectile that stuns enemies on hit.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
  - WaterProjectile (bases: ExplodingProjectile)
    doc: Water blast that slows enemies before dissipating.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
  - BouncyProjectile (bases: ExplodingProjectile)
    doc: Projectile that arcs upward then drops like a bouncing bomb.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
      - update(self) -> None
  - FireworkProjectile (bases: ExplodingProjectile)
    doc: Projectile that rises then bursts into an explosion.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y) -> None
      - update(self) -> None
  - ShockwaveProjectile (bases: ExplodingProjectile)
    doc: Ground-level wave that slides horizontally.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
  - MelodyProjectile (bases: ExplodingProjectile)
    doc: Projectile that oscillates vertically like a musical note.
    class_vars:
      - (none)
    methods:
      - __init__(self, x, y, direction) -> None
      - update(self) -> None
- functions:
  - (none)

### `hololive_coliseum\quest_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - QuestManager (bases: (none))
    doc: Track active and completed quests.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add(self, quest_id, objective) -> None
      - update_progress(self, quest_id, amount) -> None
      - complete(self, quest_id) -> None
      - is_completed(self, quest_id) -> bool
      - get_progress(self, quest_id) -> int
      - to_dict(self) -> dict
      - load_from_dict(self, data) -> None
- functions:
  - (none)

### `hololive_coliseum\raid_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - RaidManager (bases: (none))
    doc: Manage raid lockouts and groups.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - create_group(self, players) -> None
      - list_groups(self)
- functions:
  - (none)

### `hololive_coliseum\recursive_generator.py`

- docstring: Chain existing generators to build game data in one call.
- imports:
  - .auto_balancer
  - .class_generator
  - .skill_generator
  - .subclass_generator
  - .trade_skill_generator
  - __future__
- globals:
  - (none)
- classes:
  - RecursiveGenerator (bases: (none))
    doc: Generate classes, subclasses, skills and trade skills recursively.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - generate_all(self, base_classes, professions) -> dict[str, object]
- functions:
  - (none)

### `hololive_coliseum\replay_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ReplayManager (bases: (none))
    doc: Store and retrieve match replays.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - record(self, data) -> None
      - list_replays(self)
- functions:
  - (none)

### `hololive_coliseum\reputation_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ReputationManager (bases: (none))
    doc: Track faction reputation values for long-term progression.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - modify(self, faction, amount) -> int
      - get(self, faction) -> int
      - top(self, limit) -> list[tuple[str, int]]
      - to_dict(self) -> dict[str, int]
      - load_from_dict(self, data) -> None
- functions:
  - (none)

### `hololive_coliseum\resource_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ResourceManager (bases: (none))
    doc: Cache loaded assets so files are only read once.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - load(self, path, loader) -> object
      - unload(self, path) -> None
- functions:
  - (none)

### `hololive_coliseum\save_manager.py`

- docstring: Utility functions for reading and writing settings files.
- imports:
  - json
  - os
  - shutil
  - typing
- globals:
  - SAVE_DIR
- classes:
  - (none)
- functions:
  - _settings_file() -> str
  - _inventory_file() -> str
  - load_settings() -> dict[str, Any]
  - save_settings(data) -> None
  - wipe_saves() -> None
  - merge_records(data) -> dict[str, Any]
  - load_inventory() -> dict[str, int]
  - save_inventory(items) -> None

### `hololive_coliseum\score_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ScoreManager (bases: (none))
    doc: Track the current and best score for a run.
    class_vars:
      - (none)
    methods:
      - __init__(self, best_score, combo_window) -> None
      - reset(self) -> None
      - add(self, points) -> None
      - record_kill(self, now) -> None
      - update(self, now) -> None
      - finalize(self) -> int
- functions:
  - (none)

### `hololive_coliseum\screenshot_manager.py`

- docstring: Screenshot manager for saving captured images to disk.
- imports:
  - .save_manager
  - __future__
  - os
  - time
  - typing
- globals:
  - (none)
- classes:
  - ScreenshotManager (bases: (none))
    doc: Manage in-game screenshots stored under ``SavedGames/screenshots``.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - capture(self, surface, name) -> str
      - list_shots(self) -> List[str]
- functions:
  - (none)

### `hololive_coliseum\script_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ScriptManager (bases: (none))
    doc: Load and execute simple scripts for events and modding.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_script(self, name, code) -> None
      - remove_script(self, name) -> None
      - get_script(self, name) -> str | None
- functions:
  - (none)

### `hololive_coliseum\season_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - SeasonManager (bases: (none))
    doc: Track the current season and reset logic.
    class_vars:
      - (none)
    methods:
      - __init__(self, season)
      - next_season(self) -> None
      - current(self) -> int
- functions:
  - (none)

### `hololive_coliseum\session_manager.py`

- docstring: (none)
- imports:
  - uuid
- globals:
  - (none)
- classes:
  - SessionManager (bases: (none))
    doc: Track login sessions and prevent duplicates.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - create(self, user_id) -> str
      - remove(self, token) -> None
      - get_user(self, token) -> str | None
- functions:
  - (none)

### `hololive_coliseum\shared_state_manager.py`

- docstring: (none)
- imports:
  - .state_sync
  - .state_verification_manager
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - SharedStateManager (bases: (none))
    doc: Store shared state and compute/apply deltas.
    class_vars:
      - (none)
    methods:
      - __init__(self, tolerances, verifier) -> None
      - update(self) -> Dict[str, Any]
      - apply(self, delta) -> Dict[str, Any]
      - load_snapshot(self, snapshot, sequence) -> Dict[str, Any]
      - current_sequence(self) -> int
- functions:
  - (none)

### `hololive_coliseum\skill_generator.py`

- docstring: Generate basic skills for player classes.
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - SkillGenerator (bases: (none))
    doc: Create skill templates for classes.
    class_vars:
      - (none)
    methods:
      - generate(self, class_name, base_attack) -> list[dict[str, float]]
- functions:
  - (none)

### `hololive_coliseum\skill_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - Skill (bases: (none))
    doc: Simple callable skill with a cooldown.
    class_vars:
      - (none)
    methods:
      - __init__(self, cooldown_ms, execute)
  - SkillManager (bases: (none))
    doc: Manage a set of named skills and their cooldown timers.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - register(self, name, cooldown_ms, callback) -> None
      - use(self, name, now)
- functions:
  - (none)

### `hololive_coliseum\sound_manager.py`

- docstring: (none)
- imports:
  - os
  - pygame
- globals:
  - (none)
- classes:
  - SoundManager (bases: (none))
    doc: Manage mixer volume and track the last played sound.
    class_vars:
      - (none)
    methods:
      - __init__(self, volume)
      - play(self, name) -> None
      - stop(self) -> None
      - cycle_volume(self) -> float
      - adjust_volume(self, delta) -> float
- functions:
  - (none)

### `hololive_coliseum\spawn_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - SpawnManager (bases: (none))
    doc: Schedule NPC or item spawns.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - schedule(self, obj, time_ms) -> None
      - get_ready(self, now)
      - clear(self) -> None
- functions:
  - (none)

### `hololive_coliseum\stamina_manager.py`

- docstring: Track and spend a character's stamina resource.
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - StaminaManager (bases: (none))
    doc: Track and spend a character's stamina resource.
    class_vars:
      - (none)
    methods:
      - __init__(self, max_stamina) -> None
      - use(self, amount) -> bool
      - set_regen_step(self, step) -> None
      - regen(self, amount) -> int
- functions:
  - (none)

### `hololive_coliseum\state_sync.py`

- docstring: (none)
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - StateSync (bases: (none))
    doc: Compute diffs between game state snapshots for efficient networking.  Small floating‑point changes can be ignored by supplying per-field tolerances. This keeps packets tiny and reduces latency by avoiding updates for insignificant jitter.
    class_vars:
      - (none)
    methods:
      - __init__(self, tolerances) -> None
      - _has_changed(self, key, prev, new) -> bool
      - encode(self, state) -> Dict[str, Any]
      - apply(self, delta) -> Dict[str, Any]
- functions:
  - (none)

### `hololive_coliseum\state_verification_manager.py`

- docstring: (none)
- imports:
  - __future__
  - hashlib
  - json
  - typing
  - zlib
- globals:
  - (none)
- classes:
  - StateVerificationManager (bases: (none))
    doc: Compute checksums and hashes for verifying game state.
    class_vars:
      - (none)
    methods:
      - _encode(self, state) -> bytes
      - compute(self, state) -> Dict[str, str]
      - verify(self, state, digests) -> bool
- functions:
  - (none)

### `hololive_coliseum\stats_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - StatsManager (bases: (none))
    doc: Track base stats with temporary modifiers.
    class_vars:
      - (none)
    methods:
      - __init__(self, base_stats)
      - apply_modifier(self, stat, amount) -> None
      - remove_modifier(self, stat, amount) -> None
      - get(self, stat) -> int
      - to_dict(self) -> dict[str, int]
- functions:
  - (none)

### `hololive_coliseum\status_effects.py`

- docstring: Status effect classes used for temporary sprite modifiers.
- imports:
  - pygame
- globals:
  - (none)
- classes:
  - StatusEffect (bases: (none))
    doc: Base status effect applied to a sprite.
    class_vars:
      - (none)
    methods:
      - __init__(self, duration_ms, start_time) -> None
      - apply(self, target)
      - update(self, target, now) -> None
      - remove(self, target)
  - FreezeEffect (bases: StatusEffect)
    doc: Halve target speed for a short duration.
    class_vars:
      - (none)
    methods:
      - __init__(self, duration_ms, factor, start_time) -> None
      - apply(self, target)
      - remove(self, target) -> None
  - SlowEffect (bases: StatusEffect)
    doc: Reduce horizontal speed of the target.
    class_vars:
      - (none)
    methods:
      - __init__(self, duration_ms, factor) -> None
      - apply(self, target)
      - remove(self, target) -> None
  - SpeedEffect (bases: StatusEffect)
    doc: Temporarily increase target speed.
    class_vars:
      - (none)
    methods:
      - __init__(self, duration_ms, factor) -> None
      - apply(self, target) -> None
      - remove(self, target) -> None
  - ShieldEffect (bases: StatusEffect)
    doc: Make target temporarily invincible.
    class_vars:
      - (none)
    methods:
      - __init__(self, duration_ms) -> None
      - apply(self, target) -> None
      - remove(self, target) -> None
  - AttackEffect (bases: StatusEffect)
    doc: Temporarily increase the target's attack stat.
    class_vars:
      - (none)
    methods:
      - __init__(self, duration_ms, amount) -> None
      - apply(self, target) -> None
      - remove(self, target) -> None
  - DefenseEffect (bases: StatusEffect)
    doc: Temporarily increase the target's defense stat.
    class_vars:
      - (none)
    methods:
      - __init__(self, duration_ms, amount) -> None
      - apply(self, target) -> None
      - remove(self, target) -> None
  - PoisonEffect (bases: StatusEffect)
    doc: Inflict periodic damage on the target.
    class_vars:
      - (none)
    methods:
      - __init__(self, duration_ms, damage, interval_ms) -> None
      - update(self, target, now) -> None
  - BurnEffect (bases: StatusEffect)
    doc: Apply periodic burn damage to the target.
    class_vars:
      - (none)
    methods:
      - __init__(self, duration_ms, damage, interval_ms) -> None
      - update(self, target, now) -> None
  - StunEffect (bases: StatusEffect)
    doc: Temporarily prevent the target from moving.
    class_vars:
      - (none)
    methods:
      - __init__(self, duration_ms) -> None
      - apply(self, target) -> None
      - remove(self, target) -> None
  - SilenceEffect (bases: StatusEffect)
    doc: Temporarily prevent the target from using special attacks.
    class_vars:
      - (none)
    methods:
      - __init__(self, duration_ms) -> None
      - apply(self, target) -> None
      - remove(self, target) -> None
  - StatusEffectManager (bases: (none))
    doc: Keep track of active status effects on sprites.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_effect(self, target, effect) -> None
      - update(self, now) -> None
      - active_effects(self, target, now) -> list[dict[str, object]]
- functions:
  - (none)

### `hololive_coliseum\story_maps.py`

- docstring: (none)
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - create_story_maps(characters) -> Dict[str, Dict]

### `hololive_coliseum\subclass_generator.py`

- docstring: Generate subclasses from base class templates.
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - SubclassGenerator (bases: (none))
    doc: Produce subclass definitions with simple stat tweaks.
    class_vars:
      - (none)
    methods:
      - create(self, base, variant) -> dict[str, int]
- functions:
  - (none)

### `hololive_coliseum\support_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - SupportManager (bases: (none))
    doc: Track support tickets from players.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - submit(self, message) -> int
      - get(self, ticket_id) -> str | None
- functions:
  - (none)

### `hololive_coliseum\sync_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - SyncManager (bases: (none))
    doc: Maintain a time offset for client prediction.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - update(self, remote_time, local_time) -> None
      - to_local(self, remote_time) -> int
- functions:
  - (none)

### `hololive_coliseum\team_manager.py`

- docstring: Assign entities to teams and check ally relationships.
- imports:
  - __future__
- globals:
  - (none)
- classes:
  - TeamManager (bases: (none))
    doc: Track team memberships to prevent friendly fire.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - set_team(self, actor, team) -> None
      - get_team(self, actor) -> int | None
      - are_allies(self, a, b) -> bool
      - remove(self, actor) -> None
- functions:
  - (none)

### `hololive_coliseum\telemetry_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - TelemetryManager (bases: (none))
    doc: Collect gameplay analytics for heatmaps and metrics.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - log(self, event) -> None
      - get_events(self)
- functions:
  - (none)

### `hololive_coliseum\threat_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - ThreatManager (bases: (none))
    doc: Maintain simple threat tables for AI focus.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_threat(self, actor, amount) -> None
      - highest_threat(self)
- functions:
  - (none)

### `hololive_coliseum\title_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - TitleManager (bases: (none))
    doc: Manage unlockable titles and the active one.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - unlock(self, title) -> None
      - set_active(self, title) -> bool
      - get_active(self)
- functions:
  - (none)

### `hololive_coliseum\tournament_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - TournamentManager (bases: (none))
    doc: Schedule brackets for competitions.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - create_bracket(self, players) -> None
      - list_brackets(self)
- functions:
  - (none)

### `hololive_coliseum\trade_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - TradeManager (bases: (none))
    doc: Handle simple item trades between players.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - propose_trade(self, from_player, to_player, item) -> int
      - accept_trade(self, trade_id)
- functions:
  - (none)

### `hololive_coliseum\trade_skill_crafting_manager.py`

- docstring: Craft weapons and armor from trade skill blueprints.
- imports:
  - .item_manager
  - .trade_skill_generator
  - __future__
  - dataclasses
  - typing
- globals:
  - (none)
- classes:
  - CraftedItem (bases: (none))
    doc: Record linking a crafted item to the trade skill that produced it.
    class_vars:
      - name
      - product_type
      - quality
      - recipe_materials
      - stats
      - trade_skill
    methods:
      - as_dict(self) -> dict[str, object]
  - TradeSkillCraftingManager (bases: (none))
    doc: Produce gear blueprints based on available trade skills.
    class_vars:
      - (none)
    methods:
      - __init__(self, item_manager, generator) -> None
      - craft_items(self, trade_skills) -> tuple[CraftedItem, ...]
      - craft_summary(self, trade_skills) -> list[dict[str, object]]
      - _derive_stats(skill, product_type, index, level_band) -> dict[str, int]
      - _apply_gathering_modifiers(stats, product_type, modifiers) -> dict[str, int]
      - _create_item(item_name, product_type, stats) -> tuple[Optional[Weapon | Armor | Bow | Wand], str]
      - _quality_from_skill(skill, index) -> str
      - iter_crafted_items(self, trade_skills) -> Iterable[CraftedItem]
- functions:
  - (none)

### `hololive_coliseum\trade_skill_generator.py`

- docstring: Generate trade skills for professions.
- imports:
  - __future__
  - typing
- globals:
  - (none)
- classes:
  - TradeSkillGenerator (bases: (none))
    doc: Create trade skill entries with recipe hooks, levels, and experience.
    class_vars:
      - _GATHERING_SYNERGIES
      - _LEVEL_BANDS
      - _RECIPE_HINTS
      - _SPECIALISATIONS
    methods:
      - generate(self, profession) -> dict[str, object]
      - list_core_skills(self) -> tuple[str, ...]
      - level_band(self, profession) -> tuple[int, int]
      - is_gathering(self, profession) -> bool
      - gathering_synergy(self, profession) -> dict[str, dict[str, int]]
      - collect_gathering_bonuses(self, skills) -> dict[str, dict[str, int]]
      - iter_recipe_sources(self, skills) -> Iterable[tuple[str, dict[str, object]]]
      - _tier_for_band(band) -> str
- functions:
  - (none)

### `hololive_coliseum\transmission_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - TransmissionManager (bases: (none))
    doc: Helper managing holographic packet compression and decompression.  Supports ``zlib`` (default), ``bz2``, ``lzma`` or ``auto`` algorithms. ``auto`` picks the smallest result between zlib and lzma to limit bandwidth and processing requirements.
    class_vars:
      - (none)
    methods:
      - __init__(self, encrypt_key, level, algorithm, sign_key) -> None
      - compress(self, msg)
      - decompress(self, packet)
- functions:
  - (none)

### `hololive_coliseum\tutorial_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - TutorialManager (bases: (none))
    doc: Track steps completed in the tutorial.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - complete_step(self, step) -> None
      - progress(self)
- functions:
  - (none)

### `hololive_coliseum\ui_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - UIManager (bases: (none))
    doc: Track active UI elements for drawing.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - add(self, elem) -> None
      - remove(self, elem) -> None
- functions:
  - (none)

### `hololive_coliseum\voice_chat_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - VoiceChatManager (bases: (none))
    doc: Track users joined to voice chat channels.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - join(self, user, channel) -> None
      - leave(self, user, channel) -> None
- functions:
  - (none)

### `hololive_coliseum\voting_manager.py`

- docstring: Handle weekly blockchain votes exposed through the menu system.
- imports:
  - .blockchain
  - __future__
  - json
  - os
  - random
  - time
  - typing
- globals:
  - DEFAULT_CATEGORY
  - SAVE_DIR
  - VOTE_FILE
  - WEEK_SECONDS
- classes:
  - VotingManager (bases: (none))
    doc: Provide weekly voting for a given category with per-category cooldowns.
    class_vars:
      - (none)
    methods:
      - __init__(self, choices, category) -> None
      - get_options(self, limit) -> List[str]
      - can_vote(self, account_id) -> bool
      - cast_vote(self, account_id, choice) -> Dict[str, object]
      - get_vote_counts(self, include_choices) -> Dict[str, int]
      - get_winner(self) -> str | None
- functions:
  - _normalize_votes(raw) -> Dict[str, Dict[str, int]]
  - _load_votes() -> Dict[str, Dict[str, int]]
  - _save_votes(data) -> None

### `hololive_coliseum\war_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - WarManager (bases: (none))
    doc: Track faction war scores.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - add_points(self, faction, points) -> None
      - leading(self)
- functions:
  - (none)

### `hololive_coliseum\weather_forecast_manager.py`

- docstring: Produce deterministic weather forecasts for shared worlds and arenas.
- imports:
  - __future__
  - random
  - typing
- globals:
  - DEFAULT_WEATHER
- classes:
  - WeatherForecastManager (bases: (none))
    doc: Generate reproducible weather schedules for MMO regions and arenas.
    class_vars:
      - (none)
    methods:
      - __init__(self, seed, weather_types)
      - weather_types(self) -> tuple[str, ...]
      - forecast(self, steps) -> list[str]
      - next_weather(self) -> str
      - upcoming(self, steps) -> list[str]
      - reset(self) -> None
      - _ensure_cache(self, target) -> None
- functions:
  - (none)

### `hololive_coliseum\weekly_manager.py`

- docstring: (none)
- imports:
  - (none)
- globals:
  - (none)
- classes:
  - WeeklyManager (bases: (none))
    doc: Track weekly challenges with reset functionality.
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - add(self, name) -> None
      - complete(self, name) -> None
      - reset(self) -> None
- functions:
  - (none)

### `hololive_coliseum\world_generation_manager.py`

- docstring: Generate MMO regions from world seeds and dynamic content.
- imports:
  - .auto_dev_boss_manager
  - .auto_dev_evolution_manager
  - .auto_dev_focus_manager
  - .auto_dev_guidance_manager
  - .auto_dev_intelligence_manager
  - .auto_dev_mob_ai_manager
  - .auto_dev_monster_manager
  - .auto_dev_network_manager
  - .auto_dev_pipeline
  - .auto_dev_quest_manager
  - .auto_dev_research_manager
  - .auto_dev_roadmap_manager
  - .auto_dev_scenario_manager
  - .auto_dev_spawn_manager
  - .blockchain
  - .dynamic_content_manager
  - .item_manager
  - .leveling_manager
  - .objective_manager
  - .trade_skill_crafting_manager
  - .voting_manager
  - .world_region_manager
  - .world_seed_manager
  - __future__
  - math
  - random
  - typing
- globals:
  - GOLDEN_ANGLE
- classes:
  - WorldGenerationManager (bases: (none))
    doc: Create world regions using stored seeds and procedural content.
    class_vars:
      - (none)
    methods:
      - __init__(self, seed_manager, content_manager, region_manager, voting_manager, biome_manager, item_manager, level_manager, feedback_manager, tuning_manager, projection_manager, objective_manager, scenario_manager, roadmap_manager, focus_manager, monster_manager, spawn_manager, mob_ai_manager, boss_manager, quest_manager, research_manager, guidance_manager, evolution_manager, intelligence_manager, network_manager, crafting_manager, auto_dev_pipeline) -> None
      - set_pipeline_bias(self, plan) -> None
      - _biome_from_hazard(hazard) -> str | None
      - _apply_pipeline_bias(self, region) -> None
      - sync_world(self) -> None
      - generate_region_from_seed(self, seed, player_id) -> Dict[str, object]
      - generate_region(self, player_id) -> Dict[str, object]
      - _network_nodes(self, spawn_plan, focus_report, guidance) -> list[Dict[str, object]]
      - _network_bandwidth_samples(self, spawn_plan, monsters, research) -> list[float]
      - _network_security_events(self, boss_plan, quests, guidance) -> list[Dict[str, str]]
      - _summarise_monsters(self, monsters, trade_skills) -> Dict[str, object]
      - _summarise_spawn_plan(self, spawn_plan, monsters) -> Dict[str, object]
      - _summarise_mob_ai(self, mob_ai, monsters) -> Dict[str, object]
      - _summarise_boss_plan(self, boss_plan, spawn_plan, quests) -> Dict[str, object]
      - _summarise_quests(self, quests, trade_skills, boss_plan) -> Dict[str, object]
      - _derive_trade_skills(self, roadmap_entry, scenarios) -> list[str]
- functions:
  - (none)

### `hololive_coliseum\world_player_manager.py`

- docstring: Track MMO player positions and limit them to existing regions.
- imports:
  - .world_generation_manager
  - .world_region_manager
  - __future__
  - math
  - typing
- globals:
  - (none)
- classes:
  - WorldPlayerManager (bases: (none))
    doc: Record positions and block movement beyond generated regions.
    class_vars:
      - (none)
    methods:
      - __init__(self, world_manager, region_manager) -> None
      - set_position(self, player_id, pos) -> None
      - get_position(self, player_id) -> Tuple[float, float]
      - move_player(self, player_id, dx, dy) -> Tuple[float, float]
      - move_player_relative(self, player_id, forward, strafe, yaw) -> Tuple[float, float]
- functions:
  - (none)

### `hololive_coliseum\world_region_manager.py`

- docstring: Store generated regions and sync them through the blockchain.
- imports:
  - .blockchain
  - __future__
  - json
  - os
  - typing
- globals:
  - DEFAULT_REGION_FILE
  - DEFAULT_SAVE_DIR
  - REGION_FILE
  - SAVE_DIR
- classes:
  - WorldRegionManager (bases: (none))
    doc: Collect generated regions and merge them from the blockchain.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_region(self, region) -> None
      - get_regions(self) -> List[Dict[str, object]]
      - sync_with_blockchain(self) -> None
- functions:
  - _region_file() -> str
  - load_regions() -> List[Dict[str, object]]
  - save_regions(regions) -> None

### `hololive_coliseum\world_seed_manager.py`

- docstring: Store proof-of-work hashes as seeds for future MMO world generation.
- imports:
  - .blockchain
  - __future__
  - json
  - os
  - typing
- globals:
  - SAVE_DIR
  - SEED_FILE
- classes:
  - WorldSeedManager (bases: (none))
    doc: Collect hashes from background mining to seed future MMO worlds.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - add_seed(self, seed) -> None
      - get_seeds(self) -> List[str]
      - sync_with_blockchain(self) -> None
- functions:
  - load_seeds() -> List[str]
  - save_seeds(seeds) -> None

### `main.py`

- docstring: (none)
- imports:
  - hololive_coliseum.game
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - (none)

### `tests\conftest.py`

- docstring: (none)
- imports:
  - os
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - (none)

### `tests\test_accessibility_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.accessibility_manager
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_toggle_colorblind()

### `tests\test_accounts.py`

- docstring: (none)
- imports:
  - hololive_coliseum
  - os
  - pygame
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_register_and_delete_account(tmp_path, monkeypatch)
  - test_execute_account_option(tmp_path, monkeypatch)
  - test_accounts_manager_class(tmp_path, monkeypatch)
  - test_renew_key_updates_registry(tmp_path, monkeypatch)

### `tests\test_additional_managers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.accessibility_manager
  - hololive_coliseum.auth_manager
  - hololive_coliseum.ban_manager
  - hololive_coliseum.chat_manager
  - hololive_coliseum.cheat_detection_manager
  - hololive_coliseum.data_protection_manager
  - hololive_coliseum.effect_manager
  - hololive_coliseum.emote_manager
  - hololive_coliseum.input_manager
  - hololive_coliseum.logging_manager
  - hololive_coliseum.notification_manager
  - hololive_coliseum.sound_manager
  - hololive_coliseum.ui_manager
  - hololive_coliseum.voice_chat_manager
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_auth_and_ban_managers()
  - test_auth_login_limit()
  - test_auth_token_expiry()
  - test_auth_logout()
  - test_cheat_detection_and_logging()
  - test_data_protection_roundtrip()
  - test_data_protection_packet()
  - test_data_protection_replay()
  - test_data_protection_expiry()
  - test_data_protection_sanitization()
  - test_data_protection_rotate_keys()
  - test_ui_and_notification_managers()
  - test_input_and_accessibility()
  - test_chat_and_voice_managers()
  - test_emote_sound_effect()

### `tests\test_ai_npc_managers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.ai_manager
  - hololive_coliseum.ally_manager
  - hololive_coliseum.npc_manager
  - hololive_coliseum.player
  - os
  - pygame
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_ai_manager_actions(monkeypatch)
  - test_npc_and_ally_manager_groups()

### `tests\test_analysis_skill.py`

- docstring: (none)
- imports:
  - __future__
  - pathlib
  - tools.analysis_skill
  - tools.generate_codebase_analysis
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_project_analysis_skill_reports_basic_metrics(tmp_path) -> None
  - test_walk_py_files_skips_virtualenv_variants(tmp_path) -> None

### `tests\test_arena_fun_balancing.py`

- docstring: (none)
- imports:
  - hololive_coliseum
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_arena_ai_player_rating_stays_in_range() -> None
  - test_arena_ai_player_playtest_projection() -> None
  - test_arena_manager_updates_fun_with_feedback() -> None
  - test_auto_balancer_uses_background_ai_feedback() -> None
  - test_arena_manager_calibrates_baseline_with_ai() -> None
  - test_arena_manager_run_ai_playtests_generates_report() -> None
  - test_arena_manager_simulate_ai_matches_returns_summary() -> None
  - test_auto_balancer_considers_fun_baseline() -> None
  - test_auto_balancer_uses_fun_season_summary() -> None
  - test_arena_manager_generates_fun_forecast() -> None
  - test_auto_balancer_uses_fun_forecast_focus() -> None
  - test_auto_balancer_fun_forecast_scales_ai_feedback() -> None
  - test_auto_balancer_uses_fun_report_trends() -> None
  - test_arena_manager_generates_fun_tuning_plan() -> None
  - test_auto_balancer_honours_fun_plan_directives() -> None

### `tests\test_auto_dev_blueprint_manager.py`

- docstring: Unit tests for the auto-dev blueprint manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_blueprint_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_blueprint_brief_blends_creation_and_functionality() -> None

### `tests\test_auto_dev_codebase_analyzer.py`

- docstring: (none)
- imports:
  - __future__
  - hololive_coliseum.auto_dev_codebase_analyzer
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_analyzer_highlights_missing_tests_and_complexity() -> None

### `tests\test_auto_dev_continuity_manager.py`

- docstring: Tests for the auto-dev continuity manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_continuity_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_continuity_plan_highlights_network_playbooks() -> None

### `tests\test_auto_dev_convergence_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_convergence_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_convergence_manager_builds_brief() -> None

### `tests\test_auto_dev_creation_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_creation_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_creation_manager_produces_blueprint() -> None

### `tests\test_auto_dev_design_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_design_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_design_manager_returns_blueprint() -> None

### `tests\test_auto_dev_dynamics_manager.py`

- docstring: Unit tests for the auto-dev dynamics manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_dynamics_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_dynamics_brief_blends_functionality_mechanics_and_network() -> None

### `tests\test_auto_dev_encounters.py`

- docstring: Tests for the extended auto-dev encounter managers.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_boss_manager
  - hololive_coliseum.auto_dev_guidance_manager
  - hololive_coliseum.auto_dev_mob_ai_manager
  - hololive_coliseum.auto_dev_monster_manager
  - hololive_coliseum.auto_dev_quest_manager
  - hololive_coliseum.auto_dev_research_manager
  - hololive_coliseum.auto_dev_spawn_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - _sample_scenarios() -> list[dict[str, object]]
  - test_monster_manager_uses_trade_skills() -> None
  - test_spawn_manager_returns_groups() -> None
  - test_mob_ai_manager_uses_projection_powerups() -> None
  - test_boss_manager_prefers_focus_hazard() -> None
  - test_quest_manager_links_trade_skills_and_boss() -> None
  - test_research_manager_reports_average() -> None
  - test_research_manager_captures_runtime(monkeypatch) -> None
  - test_guidance_manager_blends_inputs() -> None

### `tests\test_auto_dev_evolution_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_evolution_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_evolution_brief_collects_signals()
  - test_evolution_brief_handles_missing_data()

### `tests\test_auto_dev_execution_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_execution_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_execution_manager_builds_brief() -> None

### `tests\test_auto_dev_experience_manager.py`

- docstring: Unit tests for the auto-dev experience manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_experience_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_experience_brief_extends_functionality_creation() -> None

### `tests\test_auto_dev_feedback_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_feedback_manager
  - json
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_feedback_manager_collects_and_persists(tmp_path, monkeypatch)

### `tests\test_auto_dev_focus_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_focus_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_analyse_combines_signals() -> None
  - test_history_respects_limit() -> None
  - test_analyse_without_signals_returns_empty() -> None

### `tests\test_auto_dev_functionality_manager.py`

- docstring: Unit tests for the auto-dev functionality manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_functionality_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_functionality_brief_blends_gameplay_and_backend_signals() -> None

### `tests\test_auto_dev_gameplay_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_gameplay_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_gameplay_manager_builds_loops() -> None

### `tests\test_auto_dev_governance_manager.py`

- docstring: Unit tests for the auto-dev governance manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_governance_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_governance_manager_compiles_brief() -> None

### `tests\test_auto_dev_implementation_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_implementation_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_implementation_manager_builds_brief() -> None

### `tests\test_auto_dev_innovation_manager.py`

- docstring: Unit tests for the auto-dev innovation manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_innovation_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_innovation_brief_fuses_functionality_and_mechanics() -> None

### `tests\test_auto_dev_integrity_manager.py`

- docstring: Unit tests for the auto-dev integrity manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_integrity_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_integrity_report_combines_integrity_signals() -> None

### `tests\test_auto_dev_intelligence_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_intelligence_manager
  - hololive_coliseum.auto_dev_network_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_intelligence_manager_compiles_signals() -> None
  - test_boss_strategy_populates_defaults_without_hints() -> None
  - test_intelligence_manager_handles_empty_inputs() -> None

### `tests\test_auto_dev_interaction_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_interaction_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_interaction_manager_compiles_brief() -> None

### `tests\test_auto_dev_iteration_manager.py`

- docstring: Unit tests for the auto-dev iteration manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_iteration_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_iteration_brief_merges_functionality_and_network_tracks() -> None

### `tests\test_auto_dev_mechanics_manager.py`

- docstring: (none)
- imports:
  - __future__
  - hololive_coliseum.auto_dev_mechanics_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_mechanics_blueprint_blends_encounter_signals() -> None

### `tests\test_auto_dev_mitigation_manager.py`

- docstring: Tests for the auto-dev mitigation manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_mitigation_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_mitigation_manager_generates_prioritised_tasks() -> None

### `tests\test_auto_dev_modernization_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_modernization_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_modernization_manager_builds_brief() -> None

### `tests\test_auto_dev_network_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_network_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_auto_dev_network_manager_produces_brief() -> None

### `tests\test_auto_dev_network_upgrade_manager.py`

- docstring: (none)
- imports:
  - __future__
  - hololive_coliseum.auto_dev_network_upgrade_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_network_upgrade_manager_compiles_directives() -> None
  - test_network_upgrade_manager_handles_sparse_inputs() -> None

### `tests\test_auto_dev_optimization_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_optimization_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_optimization_manager_builds_brief() -> None

### `tests\test_auto_dev_pipeline.py`

- docstring: Integration tests for the auto-dev orchestration pipeline.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_pipeline
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - _scenarios() -> list[dict[str, object]]
  - _network_nodes() -> list[dict[str, object]]
  - test_pipeline_builds_comprehensive_plan() -> None

### `tests\test_auto_dev_playstyle_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_playstyle_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_playstyle_manager_creates_archetypes() -> None

### `tests\test_auto_dev_projection_manager.py`

- docstring: (none)
- imports:
  - __future__
  - hololive_coliseum.auto_dev_feedback_manager
  - hololive_coliseum.auto_dev_projection_manager
  - hololive_coliseum.auto_dev_tuning_manager
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - feedback_manager(tmp_path)
  - test_projection_summary_highlights_top_hazards(feedback_manager)
  - test_projection_summary_empty_without_data()

### `tests\test_auto_dev_remediation_manager.py`

- docstring: Tests for the auto-dev remediation manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_remediation_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_remediation_manager_applies_high_priority_tasks() -> None

### `tests\test_auto_dev_resilience_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_resilience_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_resilience_manager_summarises_cross_domain_signals() -> None

### `tests\test_auto_dev_roadmap_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_roadmap_manager
- globals:
  - (none)
- classes:
  - DummyFeedback (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - get_trending_hazard(self) -> str
      - get_average_score(self) -> float
      - get_average_duration(self) -> float
- functions:
  - test_compile_iteration_combines_sources() -> None
  - test_history_respects_limit() -> None
  - test_compile_iteration_without_data_returns_empty() -> None

### `tests\test_auto_dev_scenario_manager.py`

- docstring: Tests for the auto-dev scenario manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_scenario_manager
  - hololive_coliseum.objective_manager
  - typing
- globals:
  - (none)
- classes:
  - DummyProjection (bases: (none))
    doc: Return predetermined focus entries for tests.
    class_vars:
      - (none)
    methods:
      - __init__(self, focus) -> None
      - projection_summary(self, limit) -> Dict[str, Any]
- functions:
  - build_objective_manager() -> ObjectiveManager
  - test_scenario_briefs_include_counter_plan_and_objectives() -> None
  - test_scenario_briefs_fallback_to_objectives_when_no_projection() -> None

### `tests\test_auto_dev_security_manager.py`

- docstring: Tests for the auto-dev security orchestration manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_security_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_security_manager_builds_security_brief() -> None

### `tests\test_auto_dev_self_evolution_manager.py`

- docstring: (none)
- imports:
  - __future__
  - hololive_coliseum.auto_dev_self_evolution_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_self_evolution_blueprint_compiles_directives() -> None
  - test_self_evolution_blueprint_handles_sparse_inputs() -> None

### `tests\test_auto_dev_synthesis_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_synthesis_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_synthesis_manager_builds_brief() -> None

### `tests\test_auto_dev_systems_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_dev_systems_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_systems_manager_returns_blueprint() -> None

### `tests\test_auto_dev_transmission_manager.py`

- docstring: Tests for the auto-dev transmission calibration manager.
- imports:
  - __future__
  - hololive_coliseum.auto_dev_transmission_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_transmission_manager_calibrates_holographic_channels() -> None

### `tests\test_auto_dev_tuning_manager.py`

- docstring: (none)
- imports:
  - json
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - _set_save_dir(tmp_path, monkeypatch)
  - test_tuning_reduces_defensive_spawn_delays()

### `tests\test_background_managers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.ad_manager
  - hololive_coliseum.api_manager
  - hololive_coliseum.billing_manager
  - hololive_coliseum.cluster_manager
  - hololive_coliseum.load_balancer_manager
  - hololive_coliseum.localization_manager
  - hololive_coliseum.matchmaking_manager
  - hololive_coliseum.migration_manager
  - hololive_coliseum.resource_manager
  - hololive_coliseum.script_manager
  - hololive_coliseum.support_manager
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_script_manager_basic()
  - test_localization_and_resources()
  - test_cluster_matchmaking_balance_and_migration()
  - test_billing_ad_api_support()

### `tests\test_balance.py`

- docstring: Combat balance tests for attack and defense scaling.
- imports:
  - hololive_coliseum.combat_manager
  - hololive_coliseum.player
  - pytest
- globals:
  - pygame
- classes:
  - (none)
- functions:
  - test_stats_affect_damage()

### `tests\test_blockchain.py`

- docstring: (none)
- imports:
  - hashlib
  - hololive_coliseum
  - json
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_add_and_search(tmp_path, monkeypatch)
  - test_contract_flow(tmp_path, monkeypatch)
  - test_verify_and_merge(tmp_path, monkeypatch)
  - test_message_encryption(tmp_path, monkeypatch)
  - test_region_blocks_store_hash(tmp_path, monkeypatch)
  - test_signed_blocks(tmp_path, monkeypatch)
  - test_add_seed_and_sync(tmp_path, monkeypatch)
  - test_add_region_and_sync(tmp_path, monkeypatch)
  - test_game_result_creates_seed(tmp_path, monkeypatch)
  - test_vote_block_and_characters(tmp_path, monkeypatch)

### `tests\test_camera_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum
  - pygame
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_camera_follow_and_apply()
  - test_third_person_camera_offsets_view()
  - test_camera_shake(monkeypatch)

### `tests\test_character_vote.py`

- docstring: (none)
- imports:
  - hololive_coliseum
  - hololive_coliseum.accounts
  - hololive_coliseum.game
  - hololive_coliseum.player
  - os
  - pytest
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_load_character_names(tmp_path, monkeypatch)
  - test_menu_vote_required(tmp_path, monkeypatch)
  - test_unknown_character_filtered(tmp_path, monkeypatch)
  - test_vote_balancing_modifies_stats(tmp_path, monkeypatch)

### `tests\test_class_item_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.class_manager
  - hololive_coliseum.item_manager
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_class_manager_basic()
  - test_class_manager_rejects_duplicates()
  - test_item_manager_basic()

### `tests\test_collision_immunity.py`

- docstring: Ensure invincibility prevents all damage types.
- imports:
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_invincible_blocks_all_damage(tmp_path, monkeypatch)
  - test_dodge_avoids_damage(tmp_path, monkeypatch)

### `tests\test_crafting_station.py`

- docstring: (none)
- imports:
  - hololive_coliseum.crafting_manager
  - hololive_coliseum.crafting_station
  - hololive_coliseum.inventory_manager
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_crafting_station_interaction()

### `tests\test_critical_hits.py`

- docstring: (none)
- imports:
  - hololive_coliseum.damage_manager
  - pytest
  - random
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_critical_hit_doubles_damage(monkeypatch)
  - test_calculate_returns_crit_flag(monkeypatch)
  - test_critical_hit_respects_multiplier(monkeypatch)

### `tests\test_crumbling_platform.py`

- docstring: (none)
- imports:
  - hololive_coliseum.platform
  - hololive_coliseum.player
  - pytest
- globals:
  - pygame
- classes:
  - (none)
- functions:
  - test_crumbling_platform_disappears()

### `tests\test_currency_persistence.py`

- docstring: (none)
- imports:
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_currency_persists_between_sessions(tmp_path, monkeypatch)

### `tests\test_currency_rewards.py`

- docstring: (none)
- imports:
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_enemy_kill_awards_currency(tmp_path, monkeypatch)

### `tests\test_damage_flash.py`

- docstring: (none)
- imports:
  - hololive_coliseum.hud_manager
  - pytest
- globals:
  - pygame
- classes:
  - DummyPlayer (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - draw_status(self, screen) -> None
- functions:
  - test_damage_flash(monkeypatch)

### `tests\test_damage_numbers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.projectile
  - os
  - pytest
  - sys
- globals:
  - pygame
- classes:
  - (none)
- functions:
  - test_damage_number_spawns(tmp_path, monkeypatch)
  - test_critical_damage_number_color(tmp_path, monkeypatch)

### `tests\test_distributed_state_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.cluster_manager
  - hololive_coliseum.distributed_state_manager
  - hololive_coliseum.shared_state_manager
  - hololive_coliseum.transmission_manager
- globals:
  - (none)
- classes:
  - MemoryNodeManager (bases: (none))
    doc: In-memory node registry for tests.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - load_nodes(self) -> list[tuple[str, int]]
      - add_node(self, node) -> None
- functions:
  - test_distributed_state_broadcast_and_apply_roundtrip() -> None
  - test_distributed_state_ack_tracking() -> None
  - test_distributed_state_resend_and_snapshot_fallback() -> None
  - test_distributed_state_handshake_bootstraps_new_node() -> None
  - test_distributed_state_sync_plan_reports_cluster() -> None
  - test_distributed_state_prepare_catch_up_returns_history() -> None
  - test_distributed_state_prepare_catch_up_snapshot_on_gap() -> None
  - test_distributed_state_peer_status_tracks_lag() -> None

### `tests\test_economy_managers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.crafting_manager
  - hololive_coliseum.economy_manager
  - hololive_coliseum.inventory_manager
  - hololive_coliseum.profession_manager
  - hololive_coliseum.trade_manager
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_crafting_manager_craft()
  - test_profession_levels()
  - test_trade_manager_accept()
  - test_economy_manager_prices()

### `tests\test_enemy_ai.py`

- docstring: (none)
- imports:
  - hololive_coliseum.game
  - hololive_coliseum.player
  - hololive_coliseum.projectile
  - os
  - pygame
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_enemy_difficulty_reaction(monkeypatch)
  - test_enemy_projectile_hits_player(tmp_path, monkeypatch)
  - test_enemy_dodges_projectile(monkeypatch)
  - test_enemy_dodges_close_player(monkeypatch)
  - test_enemy_blocks_projectile(monkeypatch)
  - test_enemy_retreats_when_low_health(monkeypatch)
  - test_hard_ai_leads_moving_target(monkeypatch)
  - test_boss_enemy_special_attack(monkeypatch)
  - test_enemy_patrols_when_far(monkeypatch)

### `tests\test_enemy_health_bar.py`

- docstring: Ensure enemies render a small green health bar when undamaged.
- imports:
  - hololive_coliseum.player
  - pygame
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_enemy_health_bar_draws_green_pixel(tmp_path)

### `tests\test_event_modifiers.py`

- docstring: (none)
- imports:
  - pytest
- globals:
  - (none)
- classes:
  - DummyRegionManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self, regions)
      - get_regions(self)
- functions:
  - test_event_modifier_defaults()
  - test_event_modifier_applies_to_game(tmp_path, monkeypatch)

### `tests\test_experience_gain.py`

- docstring: (none)
- imports:
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_enemy_kill_awards_experience(tmp_path, monkeypatch)

### `tests\test_fullscreen.py`

- docstring: Tests for the fullscreen toggle in the settings menu.
- imports:
  - hololive_coliseum.game
  - pytest
- globals:
  - pygame
- classes:
  - (none)
- functions:
  - test_toggle_fullscreen()

### `tests\test_game.py`

- docstring: (none)
- imports:
  - os
  - pytest
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_game_initialization(tmp_path, monkeypatch)
  - test_draw_menu_gradient(tmp_path, monkeypatch)
  - test_game_has_mp_type_menu(tmp_path, monkeypatch)
  - test_game_initializes_objectives(tmp_path, monkeypatch)
  - test_draw_key_bindings_menu(tmp_path, monkeypatch)
  - test_controller_menu_options(tmp_path, monkeypatch)
  - test_character_menu_has_ai_option(tmp_path, monkeypatch)
  - test_vote_menu_has_categories(tmp_path, monkeypatch)
  - test_character_menu_has_difficulty(tmp_path, monkeypatch)
  - test_watson_in_character_list(tmp_path, monkeypatch)
  - test_ina_in_character_list(tmp_path, monkeypatch)
  - test_fubuki_in_character_list(tmp_path, monkeypatch)
  - test_character_list_has_22_entries(tmp_path, monkeypatch)
  - test_game_uses_map_manager(tmp_path, monkeypatch)
  - test_ai_players_spawn(tmp_path, monkeypatch)
  - test_setup_level_resets_timers(tmp_path, monkeypatch)
  - test_setup_level_adds_two_gravity_zones(tmp_path, monkeypatch)
  - test_spawn_manager_schedules_powerup(tmp_path, monkeypatch)
  - test_mana_powerup_refills_mana(tmp_path, monkeypatch)
  - test_stamina_powerup_refills_stamina(tmp_path, monkeypatch)
  - test_speed_powerup_boosts_player(tmp_path, monkeypatch)
  - test_shield_powerup_blocks_damage(tmp_path, monkeypatch)
  - test_life_powerup_adds_life(tmp_path, monkeypatch)
  - test_attack_powerup_boosts_player(tmp_path, monkeypatch)
  - test_defense_powerup_boosts_player(tmp_path, monkeypatch)
  - test_experience_powerup_grants_xp(tmp_path, monkeypatch)
  - test_no_pickup_during_dodge(tmp_path, monkeypatch)
  - test_enemy_ai_moves_toward_player(tmp_path, monkeypatch)
  - test_enemy_collision_hurts_player(tmp_path, monkeypatch)
  - test_chapter_list_has_20_entries(tmp_path, monkeypatch)
  - test_map_menu_has_back_option(tmp_path, monkeypatch)
  - test_character_menu_has_back_option(tmp_path, monkeypatch)
  - test_pause_menu_options(tmp_path, monkeypatch)
  - test_draw_pause_menu(tmp_path, monkeypatch)
  - test_draw_inventory_and_equipment(tmp_path, monkeypatch)
  - test_main_menu_has_info_options(tmp_path, monkeypatch)
  - test_quick_start_launches_playing(tmp_path, monkeypatch)
  - test_first_blood_achievement(tmp_path, monkeypatch)
  - test_draw_how_to_play(tmp_path, monkeypatch)
  - test_draw_credits(tmp_path, monkeypatch)
  - test_draw_scoreboard(tmp_path, monkeypatch)
  - test_draw_goals_menu(tmp_path, monkeypatch)
  - test_draw_achievements(tmp_path, monkeypatch)
  - test_escape_enters_pause(tmp_path, monkeypatch)
  - test_draw_lobby_menu(tmp_path, monkeypatch)
  - test_cycle_volume(tmp_path, monkeypatch)
  - test_node_settings_menu(tmp_path, monkeypatch)
  - test_accounts_menu(tmp_path, monkeypatch)
  - test_settings_menu_has_new_options(tmp_path, monkeypatch)
  - test_start_and_stop_node(tmp_path, monkeypatch)
  - test_game_over_state(tmp_path, monkeypatch)
  - test_best_time_saved(tmp_path, monkeypatch)
  - test_best_score_saved(tmp_path, monkeypatch)
  - test_enemy_kill_increments_score(tmp_path, monkeypatch)
  - test_victory_state(tmp_path, monkeypatch)
  - test_final_time_victory(tmp_path, monkeypatch)
  - test_final_time_game_over(tmp_path, monkeypatch)
  - test_end_menu_options(tmp_path, monkeypatch)
  - test_play_again_returns_to_char(tmp_path, monkeypatch)
  - test_chat_toggle_and_send(tmp_path, monkeypatch)
  - test_f12_captures_screenshot(tmp_path, monkeypatch)
  - test_game_hud_auto_dev_summary(tmp_path, monkeypatch)
  - test_game_hud_world_activity(tmp_path, monkeypatch)

### `tests\test_gathering_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.gathering_manager
  - hololive_coliseum.inventory_manager
  - hololive_coliseum.profession_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_gathering_timing_rewards()

### `tests\test_generators.py`

- docstring: (none)
- imports:
  - hololive_coliseum
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_skill_generator()
  - test_subclass_generator()
  - test_trade_skill_generator()
  - test_trade_skill_generator_handles_new_specialisations() -> None
  - test_trade_skill_generator_includes_gatherers() -> None
  - test_auto_balancer()
  - test_class_generator_unique_and_balance()
  - test_interaction_generator_and_manager()

### `tests\test_goal_analysis_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.goal_analysis_manager
  - pathlib
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_goal_analysis_marks_completed(tmp_path) -> None
  - test_goal_analysis_missing_snapshot(tmp_path) -> None

### `tests\test_gravity_zone.py`

- docstring: (none)
- imports:
  - hololive_coliseum.gravity_zone
  - hololive_coliseum.player
  - os
  - pygame
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_player_gravity_zone()
  - test_high_gravity_zone()

### `tests\test_hazard_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.hazard_manager
  - hololive_coliseum.hazards
  - hololive_coliseum.player
  - os
  - pygame
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_hazard_manager_player_damage(tmp_path, monkeypatch)
  - test_hazard_manager_records_hazards(tmp_path, monkeypatch)

### `tests\test_hazards.py`

- docstring: (none)
- imports:
  - hololive_coliseum.game
  - hololive_coliseum.hazards
  - hololive_coliseum.player
  - os
  - pytest
  - sys
- globals:
  - pygame
- classes:
  - (none)
- functions:
  - test_spike_trap_damages_player(tmp_path, monkeypatch)
  - test_enemy_jumps_over_hazard(tmp_path, monkeypatch)
  - test_lava_zone_damage(tmp_path, monkeypatch)
  - test_acid_pool_slow(tmp_path, monkeypatch)
  - test_quicksand_pulls_and_slows(tmp_path, monkeypatch)
  - test_fire_zone_burns_player(tmp_path, monkeypatch)
  - test_frost_zone_freezes_player(tmp_path, monkeypatch)
  - test_poison_zone_poisons_player(tmp_path, monkeypatch)
  - test_bounce_pad_launches_player(tmp_path, monkeypatch)
  - test_teleport_pad_moves_player(tmp_path, monkeypatch)
  - test_silence_zone_blocks_special(tmp_path, monkeypatch)
  - test_wind_zone_push(tmp_path, monkeypatch)
  - test_lightning_zone_zap(tmp_path, monkeypatch)
  - test_regen_zone_heals(tmp_path, monkeypatch)

### `tests\test_health_regen.py`

- docstring: (none)
- imports:
  - hololive_coliseum.health_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_health_regenerates_after_delay()

### `tests\test_holographic_compression.py`

- docstring: (none)
- imports:
  - cryptography.hazmat.primitives.asymmetric
  - hololive_coliseum.holographic_compression
  - json
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_compress_roundtrip()
  - test_compress_encrypt_roundtrip()
  - test_wrong_key_returns_none()
  - test_compress_custom_level()
  - test_compress_lzma_algorithm()
  - test_compress_bz2_algorithm()
  - test_auto_algorithm_roundtrip()
  - test_anchor_points_present()
  - test_signature_roundtrip()
  - test_signature_verify_failure()
  - test_decompress_invalid_digest_returns_none()
  - test_rle_applied_for_repetition()

### `tests\test_hud_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.hud_manager
  - hololive_coliseum.player
  - os
  - pygame
  - pytest
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_hud_manager_draw()
  - test_hud_manager_draw_combo()
  - test_hud_manager_draw_objectives()
  - test_hud_manager_draw_resource_summary()
  - test_hud_manager_draw_status_effects()
  - test_hud_manager_draw_auto_dev_panel()
  - test_hud_manager_draw_world_ticker()

### `tests\test_inventory_capacity.py`

- docstring: (none)
- imports:
  - hololive_coliseum.inventory_manager
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_inventory_capacity_limit()

### `tests\test_inventory_equipment.py`

- docstring: (none)
- imports:
  - hololive_coliseum.item_manager
  - os
  - pytest
  - sys
- globals:
  - pygame
- classes:
  - (none)
- functions:
  - test_inventory_equip_and_unequip(tmp_path, monkeypatch)
  - test_head_slot(tmp_path, monkeypatch)
  - test_weapon_subclasses_use_weapon_slot()
  - test_offhand_subclasses_use_offhand_slot()

### `tests\test_inventory_persistence.py`

- docstring: (none)
- imports:
  - hololive_coliseum
  - os
  - pytest
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_inventory_roundtrip(tmp_path, monkeypatch)
  - test_level_setup_loads_saved_inventory(tmp_path, monkeypatch)

### `tests\test_item_use.py`

- docstring: (none)
- imports:
  - hololive_coliseum.player
  - os
  - pytest
  - sys
- globals:
  - pygame
- classes:
  - (none)
- functions:
  - test_use_potion_consumes_and_heals()
  - test_use_mana_potion_consumes_and_restores_mana()

### `tests\test_iteration_manager.py`

- docstring: Tests for saving and loading iteration snapshots.
- imports:
  - hololive_coliseum.iteration_manager
  - json
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_save_and_load_iteration(tmp_path)

### `tests\test_level_manager.py`

- docstring: (none)
- imports:
  - pygame
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_level_manager_sets_up_groups(tmp_path, monkeypatch)
  - test_story_boss_and_minions(tmp_path, monkeypatch)
  - test_story_minions_every_chapter(tmp_path, monkeypatch)
  - test_platforms_loaded(tmp_path, monkeypatch)
  - test_auto_dev_tuning_adjusts_spawn_schedule(tmp_path, monkeypatch)

### `tests\test_level_up_stats.py`

- docstring: (none)
- imports:
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_level_up_boosts_stats(monkeypatch, tmp_path)

### `tests\test_leveling_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.leveling_manager
  - hololive_coliseum.world_generation_manager
- globals:
  - (none)
- classes:
  - DummySeedManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - get_seeds(self)
  - DummyContentManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - create(self, kind) -> str
  - DummyRegionManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - add_region(self, region)
      - get_regions(self)
- functions:
  - test_region_grants_experience()

### `tests\test_loot_drops.py`

- docstring: Verify that defeated enemies drop loot items.
- imports:
  - pathlib
  - pytest
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_enemy_drops_loot(tmp_path, monkeypatch)

### `tests\test_low_health_warning.py`

- docstring: (none)
- imports:
  - hololive_coliseum.hud_manager
  - pytest
- globals:
  - pygame
- classes:
  - DummyPlayer (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - draw_status(self, surface) -> None
- functions:
  - test_low_health_warning(monkeypatch)

### `tests\test_menu_state_managers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.game_state_manager
  - hololive_coliseum.menu_manager
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_menu_manager_wraps()
  - test_game_state_manager_change_and_revert()

### `tests\test_meta_managers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.ai_moderation_manager
  - hololive_coliseum.arena_manager
  - hololive_coliseum.bot_manager
  - hololive_coliseum.daily_task_manager
  - hololive_coliseum.device_manager
  - hololive_coliseum.dynamic_content_manager
  - hololive_coliseum.geo_manager
  - hololive_coliseum.onboarding_manager
  - hololive_coliseum.party_manager
  - hololive_coliseum.raid_manager
  - hololive_coliseum.replay_manager
  - hololive_coliseum.season_manager
  - hololive_coliseum.telemetry_manager
  - hololive_coliseum.tournament_manager
  - hololive_coliseum.tutorial_manager
  - hololive_coliseum.war_manager
  - hololive_coliseum.weekly_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_replay_manager()
  - test_bot_and_telemetry()
  - test_ai_moderation_and_dynamic_content()
  - test_geo_and_device()
  - test_season_and_tasks()
  - test_tutorial_and_onboarding()
  - test_competition_managers()

### `tests\test_minigame_autoskill.py`

- docstring: (none)
- imports:
  - hololive_coliseum.auto_skill_manager
  - hololive_coliseum.inventory_manager
  - hololive_coliseum.minigame_manager
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_reaction_minigame_awards_material()
  - test_auto_skill_generation()

### `tests\test_mining_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.mining_manager
  - time
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_mining_manager_runs()
  - test_mining_manager_records_seeds(tmp_path, monkeypatch)
  - test_mining_manager_generates_regions(tmp_path, monkeypatch)

### `tests\test_mmo_builder.py`

- docstring: (none)
- imports:
  - hololive_coliseum
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_builder_creates_managers()

### `tests\test_moving_platform.py`

- docstring: (none)
- imports:
  - hololive_coliseum.platform
  - hololive_coliseum.player
  - pytest
- globals:
  - pygame
- classes:
  - (none)
- functions:
  - test_moving_platform_moves()
  - test_player_moves_with_platform()

### `tests\test_network.py`

- docstring: (none)
- imports:
  - hololive_coliseum
  - hololive_coliseum.ban_manager
  - hololive_coliseum.network
  - hololive_coliseum.node_registry
  - hololive_coliseum.save_manager
  - hololive_coliseum.state_sync
  - os
  - pathlib
  - sys
  - time
- globals:
  - (none)
- classes:
  - MemoryNodeManager (bases: (none))
    doc: In-memory node store for tests.
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - load_nodes(self) -> list[tuple[str, int]]
      - save_nodes(self, nodes) -> None
      - add_node(self, node) -> None
      - prune_nodes(self, ping_func, timeout) -> None
- functions:
  - test_network_send_receive()
  - test_network_discovery()
  - test_network_announce(tmp_path, monkeypatch)
  - test_ping_node()
  - test_select_best_node(monkeypatch)
  - test_register_and_find_games()
  - test_session_token_enforced()
  - test_register_and_find_clients()
  - test_client_join_leave_updates_peers()
  - test_nodes_share_games(tmp_path, monkeypatch)
  - test_nodes_share_clients(tmp_path, monkeypatch)
  - test_request_nodes()
  - test_nodes_update_gossip()
  - test_block_broadcast(tmp_path, monkeypatch)
  - test_chain_request(tmp_path, monkeypatch)
  - test_state_sync_delta()
  - test_reliable_packets()
  - test_records_update(tmp_path, monkeypatch)
  - test_relay_forwarding()
  - test_select_best_node_empty()
  - test_network_chat()
  - test_time_sync()
  - test_state_bridging()
  - test_rate_limit()
  - test_anti_spoofing()
  - test_banned_user_ignored()

### `tests\test_new_managers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.buff_manager
  - hololive_coliseum.combat_manager
  - hololive_coliseum.damage_manager
  - hololive_coliseum.loot_manager
  - hololive_coliseum.status_effects
  - hololive_coliseum.threat_manager
  - os
  - sys
- globals:
  - (none)
- classes:
  - Dummy (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - take_damage(self, amt)
- functions:
  - test_combat_manager_order()
  - test_damage_manager_apply()
  - test_threat_manager_highest()
  - test_loot_manager_roll(monkeypatch)
  - test_buff_manager_update()
  - pygame_time(dummy)

### `tests\test_node_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.node_manager
  - hololive_coliseum.node_registry
  - os
  - pathlib
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_add_node_dedup(tmp_path, monkeypatch)
  - test_prune_nodes(tmp_path, monkeypatch)

### `tests\test_node_registry.py`

- docstring: (none)
- imports:
  - hololive_coliseum.node_registry
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_add_node_dedup(tmp_path, monkeypatch)
  - test_prune_nodes(tmp_path, monkeypatch)
  - test_load_nodes_falls_back_to_defaults(tmp_path, monkeypatch)

### `tests\test_objective_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.objective_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_ensure_region_creates_objectives()
  - test_record_event_rewards_only_once()
  - test_objective_manager_round_trip()
  - test_auto_dev_hazard_objective_creation()

### `tests\test_player.py`

- docstring: (none)
- imports:
  - hololive_coliseum.player
  - os
  - pygame
  - pytest
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_player_gravity()
  - test_player_friction_slows_movement()
  - test_player_loads_image()
  - test_dodge_consumes_stamina()
  - test_blocking_drains_stamina()
  - test_attacks_consume_stamina()
  - test_player_health_mana_usage()
  - test_draw_status_updates_surface()
  - test_melee_attack_and_block()
  - test_parry_prevents_damage()
  - test_gura_special_attack()
  - test_gura_stats()
  - test_watson_special_dash()
  - test_watson_stats()
  - test_ina_grapple_projectile(tmp_path, monkeypatch)
  - test_ina_stats()
  - test_kiara_stats()
  - test_calliope_stats()
  - test_fauna_stats()
  - test_kronii_stats()
  - test_irys_stats()
  - test_mumei_stats()
  - test_fubuki_stats()
  - test_matsuri_stats()
  - test_miko_stats()
  - test_aqua_stats()
  - test_pekora_stats()
  - test_marine_stats()
  - test_suisei_stats()
  - test_ayame_stats()
  - test_noel_stats()
  - test_flare_stats()
  - test_subaru_stats()
  - test_sora_stats()
  - test_player_lives_decrease()
  - test_fubuki_freeze_special()
  - test_mumei_flock_special()
  - test_fauna_healing_zone()
  - test_player_dodge()
  - test_calliope_boomerang_projectile()
  - test_kiara_dive_explosion(tmp_path, monkeypatch)
  - test_irys_shield_blocks_projectile(tmp_path, monkeypatch)
  - test_miko_piercing_beam()
  - test_player_double_jump()
  - test_sora_special_melody()
  - test_aqua_special_projectile()
  - test_pekora_special_projectile()
  - test_marine_special_boomerang()
  - test_suisei_special_piercing()
  - test_ayame_special_dash()
  - test_noel_special_shockwave()
  - test_flare_special_exploding()
  - test_subaru_special_exploding()
  - test_matsuri_firework_projectile()
  - test_aqua_special_slows()
  - test_pekora_carrot_bounces()

### `tests\test_progress_managers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.achievement_manager
  - hololive_coliseum.quest_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_quest_manager_basic()
  - test_achievement_manager_roundtrip()

### `tests\test_projectile.py`

- docstring: (none)
- imports:
  - hololive_coliseum.melee_attack
  - hololive_coliseum.projectile
  - os
  - pygame
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_projectile_moves()
  - test_projectile_aims_toward_target()
  - test_melee_attack_lifetime()
  - test_player_shoot_zero_vector(tmp_path, monkeypatch)
  - test_projectile_hits_enemy(tmp_path, monkeypatch)
  - test_exploding_projectile_expires()
  - test_explosion_projectile_stays_put()
  - test_explosion_projectile_expires()
  - test_poison_projectile_flags_poison()
  - test_burning_projectile_flags_burn()
  - test_stunning_projectile_flags_stun()
  - test_shockwave_projectile_horizontal()
  - test_melody_projectile_oscillates()

### `tests\test_recursive_generator.py`

- docstring: (none)
- imports:
  - hololive_coliseum.recursive_generator
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_recursive_generator_builds_data()

### `tests\test_reputation_rewards.py`

- docstring: (none)
- imports:
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_enemy_kill_grants_reputation(tmp_path, monkeypatch)

### `tests\test_resource_managers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.equipment_manager
  - hololive_coliseum.experience_manager
  - hololive_coliseum.health_manager
  - hololive_coliseum.inventory_manager
  - hololive_coliseum.keybind_manager
  - hololive_coliseum.mana_manager
  - hololive_coliseum.stamina_manager
  - hololive_coliseum.stats_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_health_manager_basic()
  - test_mana_manager_usage()
  - test_stamina_manager_usage()
  - test_equipment_manager()
  - test_inventory_manager_add_remove()
  - test_keybind_manager_basic()
  - test_stats_manager_modifiers()
  - test_experience_manager_levels()

### `tests\test_save_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_save_and_load_settings(tmp_path, monkeypatch)
  - test_load_settings_handles_corrupt_file(tmp_path, monkeypatch)
  - test_save_creates_directory(tmp_path, monkeypatch)
  - test_wipe_saves_missing_dir(tmp_path, monkeypatch)
  - test_wipe_saves_removes_subdirs(tmp_path, monkeypatch)
  - test_merge_records(tmp_path, monkeypatch)
  - test_merge_records_longer_time(tmp_path, monkeypatch)

### `tests\test_score_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.score_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_score_manager()
  - test_score_manager_combo()

### `tests\test_screenshot_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.screenshot_manager
  - os
  - pytest
- globals:
  - pygame
- classes:
  - (none)
- functions:
  - test_capture_saves_file(tmp_path)

### `tests\test_shared_state_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.shared_state_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_shared_state_manager_roundtrip()

### `tests\test_skill_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.skill_manager
  - pygame
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_skill_manager_cooldown()

### `tests\test_social_managers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.currency_manager
  - hololive_coliseum.friend_manager
  - hololive_coliseum.guild_manager
  - hololive_coliseum.mail_manager
  - hololive_coliseum.reputation_manager
  - hololive_coliseum.title_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_currency_manager()
  - test_title_and_reputation()
  - test_friend_and_guild()
  - test_mail_manager()

### `tests\test_sprint.py`

- docstring: (none)
- imports:
  - hololive_coliseum.player
  - os
  - pygame
  - pytest
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_sprint_uses_stamina_and_boosts_speed()

### `tests\test_state_sync.py`

- docstring: Tests for the StateSync helper.
- imports:
  - hololive_coliseum.state_sync
  - os
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_state_sync_tolerance()

### `tests\test_state_verification_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.shared_state_manager
  - hololive_coliseum.state_verification_manager
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_state_verification_roundtrip()
  - test_state_verification_detects_tamper()

### `tests\test_status_effects.py`

- docstring: (none)
- imports:
  - hololive_coliseum.player
  - hololive_coliseum.status_effects
  - os
  - pygame
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_freeze_effect_expires()
  - test_speed_effect_expires()
  - test_shield_effect_blocks_damage()
  - test_poison_effect_ticks_damage()
  - test_burn_effect_ticks_damage()
  - test_stun_effect_prevents_movement()
  - test_status_effect_manager_active_effects_summary()

### `tests\test_story_maps.py`

- docstring: (none)
- imports:
  - hololive_coliseum.story_maps
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_create_story_maps()

### `tests\test_team_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.combat_manager
  - hololive_coliseum.player
  - hololive_coliseum.team_manager
  - os
  - pytest
  - sys
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - setup_pygame()
  - test_team_assignment_allies()
  - test_friendly_fire_ignored()

### `tests\test_trade_skill_crafting_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_trade_skill_crafting_manager_creates_items() -> None
  - test_trade_skill_crafting_manager_summary_matches_items() -> None
  - test_trade_skill_crafting_manager_supports_bows_and_wands() -> None
  - test_gathering_skills_amplify_crafted_items() -> None

### `tests\test_transmission_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.transmission_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_transmission_roundtrip()
  - test_transmission_bz2_roundtrip()

### `tests\test_voting_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum
  - hololive_coliseum.accounts
  - hololive_coliseum.voting_manager
  - json
  - os
  - pytest
  - sys
  - time
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_vote_once_per_week(tmp_path, monkeypatch)
  - test_get_winner_counts_votes(tmp_path, monkeypatch)
  - test_biome_vote_counts(tmp_path, monkeypatch)
  - test_vote_file_backward_compatible(tmp_path, monkeypatch)

### `tests\test_weather_effect.py`

- docstring: (none)
- imports:
  - hololive_coliseum.environment_manager
  - pytest
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_rain_lowers_friction(monkeypatch)
  - test_snow_increases_friction(monkeypatch)
  - test_day_night_adjusts_light_level()
  - test_weather_changes_overlay_tint()

### `tests\test_weather_forecast_manager.py`

- docstring: Tests for the WeatherForecastManager and its environment integration.
- imports:
  - hololive_coliseum.environment_manager
  - hololive_coliseum.weather_forecast_manager
  - random
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_forecast_matches_random_sequence()
  - test_environment_randomize_uses_forecast_sequence()

### `tests\test_world_generation_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.item_manager
  - hololive_coliseum.world_generation_manager
  - math
  - pytest
- globals:
  - (none)
- classes:
  - DummySeedManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - get_seeds(self)
      - __init__(self)
      - sync_with_blockchain(self)
  - DummyContentManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - create(self, kind) -> str
  - DummyRegionManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - add_region(self, region)
      - get_regions(self)
      - sync_with_blockchain(self)
  - DummyVotingManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - get_winner(self)
  - DummyBiomeManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - get_winner(self)
  - DummyItemManager (bases: ItemManager)
    class_vars:
      - (none)
    methods:
      - __init__(self)
  - DummyFeedbackManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - estimate_recommended_level(self, base_level) -> int
      - region_insight(self)
  - DummyTuningManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - support_plan(self)
  - DummyProjectionManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self) -> None
      - projection_summary(self)
- functions:
  - test_generate_region_stores_and_broadcasts(monkeypatch)
  - test_sync_world_calls_managers()
  - test_sync_world_builds_missing_regions(monkeypatch)
  - test_radius_expands_with_each_region(monkeypatch)
  - test_generate_region_uses_max_radius(monkeypatch)
  - test_region_includes_vote_monument(monkeypatch)
  - test_region_includes_biome_and_loot(monkeypatch)
  - test_region_includes_auto_dev_insight(monkeypatch)

### `tests\test_world_managers.py`

- docstring: (none)
- imports:
  - hololive_coliseum.companion_manager
  - hololive_coliseum.dungeon_manager
  - hololive_coliseum.environment_manager
  - hololive_coliseum.event_manager
  - hololive_coliseum.housing_manager
  - hololive_coliseum.map_manager
  - hololive_coliseum.mount_manager
  - hololive_coliseum.pet_manager
  - hololive_coliseum.spawn_manager
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_map_and_environment()
  - test_spawn_and_event_manager()
  - test_dungeon_and_housing()
  - test_mount_pet_companion()
  - test_day_night_cycle()

### `tests\test_world_player_manager.py`

- docstring: (none)
- imports:
  - hololive_coliseum.world_player_manager
  - math
- globals:
  - (none)
- classes:
  - DummyRegionManager (bases: (none))
    class_vars:
      - (none)
    methods:
      - __init__(self)
      - get_regions(self)
- functions:
  - test_move_player_is_clamped_to_radius()
  - test_get_position_defaults_to_origin()
  - test_move_player_relative_uses_yaw()

### `tests\test_world_region_manager.py`

- docstring: Tests for the WorldRegionManager's blockchain sync.
- imports:
  - hololive_coliseum
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - test_sync_skips_regions_with_bad_hash(tmp_path, monkeypatch)

### `tools\analysis_skill.py`

- docstring: Repository analysis helpers for tracking the game's current technical state.
- imports:
  - __future__
  - ast
  - dataclasses
  - datetime
  - pathlib
  - typing
- globals:
  - (none)
- classes:
  - FileSnapshot (bases: (none))
    doc: Summary metadata for a single Python file.
    class_vars:
      - has_docstring
      - line_count
      - path
    methods:
      - (none)
  - ProjectAnalysisSkill (bases: (none))
    doc: Build a lightweight, deterministic snapshot of project health.
    class_vars:
      - (none)
    methods:
      - __init__(self, root) -> None
      - analyze(self) -> dict[str, Any]
      - render_markdown(self, analysis) -> str
      - _python_files(self, relative_dir, pattern) -> list[Path]
      - _snapshot(self, path) -> FileSnapshot
      - _top_files(self, snapshots, limit) -> list[dict[str, Any]]
      - _saved_games_snapshot(self) -> dict[str, Any]
      - _observations(self, module_snapshots, test_snapshots, docstring_ratio, runtime_snapshot) -> list[str]
- functions:
  - (none)

### `tools\analyze_project_state.py`

- docstring: Generate a concise project-state report in the repository root.
- imports:
  - __future__
  - pathlib
  - sys
  - tools.analysis_skill
- globals:
  - OUTPUT
  - ROOT
- classes:
  - (none)
- functions:
  - main() -> None

### `tools\generate_codebase_analysis.py`

- docstring: Generate docs/CODEBASE_ANALYSIS.md from the repository source tree.
- imports:
  - __future__
  - ast
  - json
  - pathlib
- globals:
  - END_MARKER
  - OUTPUT
  - ROOT
  - SKIP_DIRS
  - START_MARKER
- classes:
  - (none)
- functions:
  - _is_skipped_path(path) -> bool
  - walk_py_files(root) -> list[Path]
  - parse_file(path) -> dict[str, object]
  - _function_entry(node, async_flag) -> dict[str, object]
  - _class_entry(node) -> dict[str, object]
  - build_analysis(modules) -> str
  - _build_import_map(modules) -> dict[str, list[str]]
  - _render_module(module, imports) -> list[str]
  - _format_list(items, indent) -> list[str]
  - main() -> None

### `tools\generate_codebase_graphs.py`

- docstring: Generate docs/CODEBASE_GRAPHS.md with module and call interaction graphs.
- imports:
  - __future__
  - ast
  - collections
  - pathlib
- globals:
  - END_MARKER
  - INCLUDE_PACKAGE
  - INCLUDE_ROOT
  - OUTPUT
  - ROOT
  - SKIP_DIRS
  - START_MARKER
- classes:
  - ModuleInfo (bases: (none))
    doc: Container for parsed module details.
    class_vars:
      - (none)
    methods:
      - __init__(self, path, module_name) -> None
- functions:
  - walk_py_files(root) -> list[Path]
  - module_name_from_path(path) -> str
  - parse_module(path) -> ModuleInfo
  - collect_calls(info, tree) -> None
  - build_module_dependency_graph(modules) -> list[str]
  - build_call_graph(modules) -> list[str]
  - resolve_local_import(import_name, modules) -> str | None
  - resolve_call_target(call, info, modules) -> str | None
  - sanitize(label) -> str
  - build_document(modules) -> str
  - main() -> None

### `tools\generate_special_vfx_sprites.py`

- docstring: Generate deterministic special-attack VFX sprites for local use.
- imports:
  - __future__
  - math
  - os
  - pygame
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - _save(surface, path) -> None
  - _draw_circle(surface, color) -> None
  - _draw_vfx() -> dict[str, tuple[tuple[int, int], callable]]
  - _render_frame(size, draw_fn, idx, total) -> pygame.Surface
  - _draw_trident(surface) -> None
  - _draw_dash_ring(surface) -> None
  - _draw_tentacle(surface) -> None
  - _draw_blast(surface) -> None
  - _draw_scythe(surface) -> None
  - _draw_grove(surface) -> None
  - _draw_guard(surface) -> None
  - _draw_shield(surface) -> None
  - _draw_flock(surface) -> None
  - _draw_glitch(surface) -> None
  - _draw_burst(surface) -> None
  - _draw_shard(surface) -> None
  - _draw_firework(surface) -> None
  - _draw_beam(surface) -> None
  - _draw_bubble(surface) -> None
  - _draw_carrot(surface) -> None
  - _draw_anchor(surface) -> None
  - _draw_star(surface) -> None
  - _draw_slash(surface) -> None
  - _draw_shockwave(surface) -> None
  - _draw_fireball(surface) -> None
  - _draw_blast_small(surface) -> None
  - _draw_melody(surface) -> None
  - _draw_enemy_pulse(surface) -> None
  - main() -> None

### `tools\generate_standard_sprites.py`

- docstring: Generate standardized placeholder sprites for local use.
- imports:
  - __future__
  - hololive_coliseum.placeholder_sprites
  - hololive_coliseum.player
  - os
  - pygame
- globals:
  - (none)
- classes:
  - (none)
- functions:
  - main() -> None

<!-- AUTO-GENERATED:codebase-analysis:end -->
