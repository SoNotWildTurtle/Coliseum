"""Autoplay coordination helpers for menu flow and MMO navigation."""

from __future__ import annotations

from typing import Iterable

import os
import pygame


def autoplay_mmo(game, now: int) -> None:
    """Drive the MMO hub automatically when autoplay is enabled."""
    if not game.autoplay:
        return
    if game.state == "mmo":
        autoplay_mmo_overlays(game, now)
        return
    if not game.autoplay_mmo_fast and game.state != "main_menu":
        return
    if game.state == "main_menu":
        options = game._menu_options_for_state("main_menu") or []
        if "MMO" in options:
            game.menu_index = options.index("MMO")
            game.menu_manager.index = game.menu_index
            game._autoplay_trace("Menu main_menu: MMO", now=now)
            game._handle_menu_selection(options)


def autoplay_mmo_overlays(game, now: int) -> None:
    """Cycle MMO overlay screens and toggles during autoplay."""
    if game.autoplay_mmo_state != "mmo":
        game.autoplay_mmo_state = "mmo"
        game.autoplay_mmo_overlay_index = 0
        game.autoplay_mmo_overlay_seen.clear()
        game.autoplay_mmo_last_step = now
        game.autoplay_mmo_toggle_index = 0
        game.autoplay_mmo_layer_index = 0
    if now - game.autoplay_mmo_last_step < game.autoplay_menu_delay:
        return
    game.autoplay_mmo_last_step = now
    overlay = game.mmo_overlays[
        game.autoplay_mmo_overlay_index % len(game.mmo_overlays)
    ]
    game.autoplay_mmo_overlay_index += 1
    game.autoplay_mmo_overlay_seen.add(overlay)
    game.mmo_overlay_mode = overlay
    game._clear_mmo_toggles()
    toggle_note, layer_note, help_note = autoplay_mmo_cycle_aux(game, overlay)
    notes = [note for note in (overlay, toggle_note, layer_note, help_note) if note]
    game._autoplay_trace("MMO " + " ".join(notes), now=now)
    target = len(game.mmo_overlays)
    if game.autoplay_menu_quick:
        target = max(1, min(game.autoplay_mmo_overlay_limit, target))
    if len(game.autoplay_mmo_overlay_seen) >= target:
        game.autoplay_menu_resume_state = "main_menu"
        game.autoplay_menu_resume_time = now + game.autoplay_menu_delay


def autoplay_mmo_cycle_aux(game, overlay: str) -> tuple[str | None, ...]:
    """Flip auxiliary MMO toggles during autoplay."""
    toggle_note = None
    layer_note = None
    help_note = None
    toggles = [
        "mmo_show_minimap",
        "mmo_show_event_log",
        "mmo_ui_show_panel",
    ]
    if toggles:
        attr = toggles[game.autoplay_mmo_toggle_index % len(toggles)]
        game.autoplay_mmo_toggle_index += 1
        current = bool(getattr(game, attr, False))
        setattr(game, attr, not current)
        toggle_note = attr.replace("mmo_", "").replace("_", "-")
    layer_keys = list(game.mmo_layers.keys())
    if layer_keys:
        key = layer_keys[game.autoplay_mmo_layer_index % len(layer_keys)]
        game.autoplay_mmo_layer_index += 1
        game.mmo_layers[key] = not bool(game.mmo_layers.get(key, True))
        layer_note = f"layer:{key}"
    if overlay == "help" and not game.mmo_show_help:
        game.mmo_show_help = True
        help_note = "help"
    return toggle_note, layer_note, help_note


def autoplay_generation(game, now: int) -> None:
    """Generate MMO regions and extend playtime during autoplay."""
    if not game.autoplay:
        return
    if game.autoplay_mmo_fast:
        return
    if game.autoplay_generation_interval <= 0:
        return
    if now < game.autoplay_next_generation:
        return
    game.autoplay_next_generation = now + game.autoplay_generation_interval
    regions = game.world_generation_manager.region_manager.get_regions()
    if len(regions) < 6:
        game.world_generation_manager.generate_regions(2)
        game._autoplay_trace("Auto-dev: expanded regions", now=now)
    if game.autoplay_level_limit <= 0:
        return
    extension = max(0, game.autoplay_level_extension)
    if extension:
        game.level_limit += extension
        game._autoplay_trace(f"Level extended +{extension}s", now=now)


def autoplay_menu_flow(game, now: int) -> None:
    """Automatically step through menus before starting a match."""
    if not game.autoplay_flow or game.state == "playing":
        return
    if game.autoplay_menu_state != game.state:
        game.autoplay_menu_state = game.state
        game.autoplay_menu_stage = 0
        game.autoplay_preview_index = 0
        game.autoplay_preview_count = 0
        game.autoplay_preview_wait_start = now
        game.autoplay_preview_pause_logged = False
        game.autoplay_last_menu_step = now
        return
    if now - game.autoplay_last_menu_step < game.autoplay_menu_delay:
        return
    game.autoplay_last_menu_step = now
    if (
        game.autoplay_menu_budget > 0
        and now - game.autoplay_flow_start >= game.autoplay_menu_budget
    ):
        options = game._menu_options_for_state("main_menu") or []
        if game.state != "main_menu":
            game._set_state("main_menu")
            return
        if "Quick Start" in options:
            game.menu_index = options.index("Quick Start")
            game.menu_manager.index = game.menu_index
            game._autoplay_trace("Menu budget hit -> Quick Start", now=now)
            game._handle_menu_selection(options)
            return
        if "New Game" in options:
            game.menu_index = options.index("New Game")
            game.menu_manager.index = game.menu_index
            game._autoplay_trace("Menu budget hit -> New Game", now=now)
            game._handle_menu_selection(options)
            return
    if game.state == "splash":
        game._set_state("main_menu")
        return
    if game.state in {"rebind", "rebind_controller"}:
        autoplay_complete_rebind(game)
        return
    if (
        game.state == "mmo"
        and game.autoplay_menu_resume_state == "main_menu"
        and now >= game.autoplay_menu_resume_time
    ):
        game.autoplay_menu_resume_state = None
        game._set_state("main_menu")
        return
    if game.state in {"victory", "game_over"} and not game.show_end_options:
        game.show_end_options = True
    if game.state == "main_menu" and game.autoplay_pending_results:
        seen = game.autoplay_menu_seen.get("main_menu", set())
        options = game._menu_options_for_state("main_menu") or []
        required = [opt for opt in options if opt != "Exit"]
        if all(opt in seen for opt in required) and autoplay_vote_complete(game):
            next_state = game.autoplay_pending_results.pop(0)
            game.show_end_options = True
            game._set_state(next_state)
            return
    options = game._menu_options_for_state()
    if not options:
        return
    seen = game.autoplay_menu_seen.setdefault(game.state, set())
    if game.state == "settings_system" and not game.autoplay_allow_system_actions:
        seen.update({"Reset Records", "Wipe Saves"})
    preview_items = autoplay_preview_items(game)
    if preview_items and game.autoplay_menu_stage == 0:
        if now - game.autoplay_preview_wait_start < game.autoplay_preview_delay:
            if not game.autoplay_preview_pause_logged:
                game.autoplay_preview_pause_logged = True
                game._autoplay_trace(f"Preview pause {game.state}", now=now)
            return
        if game.autoplay_preview_count >= len(preview_items):
            game.autoplay_menu_stage = 1
        else:
            idx = game.autoplay_preview_index % len(preview_items)
            game.menu_index = idx
            game.menu_manager.index = idx
            game.autoplay_preview_index += 1
            game.autoplay_preview_count += 1
            game._autoplay_trace(
                f"Preview {game.state}: {preview_items[idx]}", now=now
            )
            return
    ordered = autoplay_menu_choice_order(game, options)
    choice = None
    page_options = game._page_option_labels()
    char_filter_label = game._character_filter_label()
    map_filter_label = game._map_filter_label()
    for opt in ordered:
        if (
            game.state == "settings_system"
            and not game.autoplay_allow_system_actions
            and opt in {"Reset Records", "Wipe Saves"}
        ):
            continue
        if game.state == "char" and opt == "Continue":
            if not autoplay_collection_complete(
                game,
                "char",
                exclude={
                    "Add AI Player",
                    "Difficulty",
                    "Continue",
                    "Back",
                    char_filter_label,
                    *page_options,
                },
                required=list(game.characters),
            ):
                continue
        if game.state == "char" and opt == "Back":
            if not autoplay_collection_complete(
                game,
                "char",
                exclude={
                    "Add AI Player",
                    "Difficulty",
                    "Continue",
                    "Back",
                    char_filter_label,
                    *page_options,
                },
                required=list(game.characters),
            ):
                continue
        if game.state == "char" and opt in page_options:
            if autoplay_collection_complete(
                game,
                "char",
                exclude={
                    "Add AI Player",
                    "Difficulty",
                    "Continue",
                    "Back",
                    char_filter_label,
                    *page_options,
                },
                required=list(game.characters),
            ):
                continue
        if game.state == "map" and opt == "Back":
            if not autoplay_collection_complete(
                game,
                "map",
                exclude={"Back", map_filter_label, *page_options},
                required=list(game.map_manager.maps.keys()),
            ):
                continue
        if game.state == "map" and opt in page_options:
            if autoplay_collection_complete(
                game,
                "map",
                exclude={"Back", map_filter_label, *page_options},
                required=list(game.map_manager.maps.keys()),
            ):
                continue
        if game.state == "chapter" and opt == "Back":
            if not autoplay_collection_complete(
                game,
                "chapter",
                exclude={"Back"},
                required=list(game.chapters),
            ):
                continue
        if game.state == "main_menu" and opt == "Vote":
            if not autoplay_vote_complete(game):
                choice = opt
                break
        if game.state == "main_menu" and opt == "Exit":
            if game.autoplay_pending_results:
                continue
        if game.state == "vote_category" and opt in {"Character", "Biome"}:
            if not autoplay_vote_category_complete(game, opt):
                choice = opt
                break
        if game.state == "vote_category" and opt == "Back":
            if not autoplay_vote_complete(game):
                continue
        if opt not in seen:
            choice = opt
            break
    if choice is None:
        return
    current_state = game.state
    game.menu_index = options.index(choice)
    game.menu_manager.index = game.menu_index
    if choice not in page_options:
        seen.add(choice)
    game._autoplay_trace(f"Menu {current_state}: {choice}", now=now)
    if game.state == "vote" and game.autoplay_vote_category:
        category_seen = game.autoplay_vote_seen.setdefault(
            game.autoplay_vote_category, set()
        )
        category_seen.add(choice)
    game._handle_menu_selection(options)
    if current_state == "main_menu" and choice == "MMO":
        game.autoplay_menu_resume_state = None
        game.autoplay_menu_resume_time = 0
        game.autoplay_mmo_state = None
    if current_state == "map" and choice != "Back":
        game.autoplay_menu_resume_state = "map"
        game.autoplay_menu_resume_time = now + game.autoplay_menu_delay
    if current_state == "chapter" and choice != "Back":
        game.autoplay_menu_resume_state = "chapter"
        game.autoplay_menu_resume_time = now + game.autoplay_menu_delay


def autoplay_complete_rebind(game) -> None:
    """Complete a rebind step during autoplay."""
    action = getattr(game, "rebind_action", "")
    if not action:
        return
    key = pygame.K_SPACE if action in {"jump", "pause"} else pygame.K_z
    game.key_bindings[action] = key
    game.rebind_action = None
    game._set_state("key_bindings")


def autoplay_menu_choice_order(game, options: list[str]) -> list[str]:
    """Determine autoplay ordering for menu options."""
    if not options:
        return []
    ordered = list(options)
    rng = getattr(game, "autoplay_rng", None)
    if rng:
        rng.shuffle(ordered)
    return ordered


def autoplay_preview_items(game) -> list[str]:
    if game.state == "char":
        return list(game._paged_characters())
    if game.state == "map":
        return list(game._paged_maps())
    if game.state == "chapter":
        return list(game.chapters)
    return []


def autoplay_state_complete(game, state: str) -> bool:
    """Return True when autoplay has selected every option for a state."""
    options = game._menu_options_for_state(state) or []
    if not options:
        return True
    seen = game.autoplay_menu_seen.get(state, set())
    return all(option in seen for option in options)


def autoplay_collection_complete(
    game,
    state: str,
    *,
    exclude: Iterable[str],
    required: Iterable[str],
) -> bool:
    seen = game.autoplay_menu_seen.get(state, set())
    for item in exclude:
        if item in seen:
            continue
    return all(item in seen for item in required)


def autoplay_vote_category_complete(game, category: str) -> bool:
    options = game.vote_options if game.autoplay_vote_category == category else []
    if not options:
        return True
    seen = game.autoplay_vote_seen.get(category, set())
    seen_count = len(seen)
    if game.autoplay_menu_quick and game.autoplay_vote_limit > 0:
        return seen_count >= min(game.autoplay_vote_limit, len(options))
    return seen_count >= len(options)


def autoplay_vote_complete(game) -> bool:
    return all(
        autoplay_vote_category_complete(game, category)
        for category in ("Character", "Biome")
    )


def autoplay_menu_playing(game, now: int) -> bool:
    if game.autoplay_menu_resume_state and now >= game.autoplay_menu_resume_time:
        game._set_state(game.autoplay_menu_resume_state)
        game.autoplay_menu_resume_state = None
        return True
    if not game.autoplay_pause_tested and now - game.level_start_time >= 600:
        game._set_state("paused")
        game.autoplay_pause_tested = True
        return True
    return False


def autoplay_update_learning(game, now: int) -> None:
    """Feed recent combat outcomes back into autoplay tuning."""
    if not game.autoplay or not game.autoplayer:
        return
    player = getattr(game, "player", None)
    if player is None:
        return
    if game.autoplay_last_health is None:
        game.autoplay_last_health = float(player.health)
        game.autoplay_last_kills = game.kills
        game.autoplay_last_feedback = now
        return
    if now - game.autoplay_last_feedback < game.autoplay_learning_interval:
        return
    damage_taken = max(0.0, game.autoplay_last_health - float(player.health))
    kills = max(0, game.kills - game.autoplay_last_kills)
    game.autoplayer.update_feedback(
        damage_taken,
        kills,
        now - game.autoplay_last_feedback,
    )
    game.autoplay_last_health = float(player.health)
    game.autoplay_last_kills = game.kills
    game.autoplay_last_feedback = now
    snapshot = game.autoplayer.tuning_snapshot()
    game._autoplay_trace(
        f"Learn dmg={damage_taken:.1f} kills={kills} {snapshot}", now=now
    )


def autoplay_monitor(game, now: int) -> None:
    """Emit periodic autoplay telemetry for monitoring."""
    if not game.autoplay_monitor or not game.autoplay or not game.autoplayer:
        return
    if now - game.autoplay_monitor_last < game.autoplay_monitor_interval:
        return
    game.autoplay_monitor_last = now
    goal = getattr(game.autoplayer, "last_goal", "idle")
    target = getattr(game.autoplayer, "last_target_name", "None")
    dist = getattr(game.autoplayer, "last_target_distance", 0)
    game._autoplay_trace(
        f"MON goal={goal} target={target} dist={int(dist)}", now=now
    )
    player = getattr(game, "player", None)
    if player is not None:
        game._autoplay_trace(
            f"MON hp={player.health} mana={player.mana} stam={player.stamina}",
            now=now,
        )
    snapshot = game.autoplayer.tuning_snapshot()
    game._autoplay_trace(f"MON tuning {snapshot}", now=now)
    if game.autoplay_feature_counts:
        summary = sorted(
            game.autoplay_feature_counts.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:4]
        packed = " ".join(f"{name}={count}" for name, count in summary)
        game._autoplay_trace(f"MON features {packed}", now=now)


def autoplay_trace(game, message: str, *, now: int | None = None) -> None:
    """Record autoplay actions to the HUD and console."""
    if now is None:
        now = pygame.time.get_ticks()
    stamp = f"{now / 1000:6.1f}s"
    line = f"{stamp} {message}"
    if game.autoplay_trace:
        game.autoplay_trace_lines.append(line)
        if len(game.autoplay_trace_lines) > max(1, game.autoplay_trace_limit):
            game.autoplay_trace_lines = game.autoplay_trace_lines[
                -game.autoplay_trace_limit :
            ]
        if game.autoplay_trace_console:
            print(line)
    autoplay_log(game, line)


def autoplay_log(game, line: str) -> None:
    if not game.autoplay_log_enabled:
        return
    try:
        os.makedirs(os.path.dirname(game.autoplay_log_path), exist_ok=True)
        with open(game.autoplay_log_path, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except OSError:
        return


def autoplay_record_feature(game, name: str) -> None:
    if not game.autoplay:
        return
    current = game.autoplay_feature_counts.get(name, 0)
    game.autoplay_feature_counts[name] = current + 1


def autoplay_trace_inputs(
    game,
    pressed_keys: set[int],
    actions: set[str],
    now: int,
) -> None:
    """Log input decisions made during autoplay."""
    for action in actions:
        autoplay_record_feature(game, f"action:{action}")
    if not game.autoplay_trace:
        return
    if now - game.autoplay_input_trace_last < game.autoplay_trace_interval:
        return
    game.autoplay_input_trace_last = now
    key_names = [pygame.key.name(key) for key in sorted(pressed_keys)]
    action_names = sorted(actions)
    keys_text = ", ".join(key_names) if key_names else "-"
    actions_text = ", ".join(action_names) if action_names else "-"
    autoplay_trace(game, f"Input keys=[{keys_text}] actions=[{actions_text}]", now=now)


def draw_autoplay_trace(game) -> None:
    """Draw recent autoplay decisions on screen."""
    if not game.autoplay_trace_overlay:
        return
    if not game.autoplay_trace_lines:
        return
    font = game.autoplay_trace_font
    lines = game.autoplay_trace_lines[-game.autoplay_trace_limit :]
    line_h = font.get_linesize()
    width = max(font.size(line)[0] for line in lines) + 12
    height = line_h * len(lines) + 10
    panel = pygame.Surface((width, height), pygame.SRCALPHA)
    panel.fill((10, 12, 16, 170))
    game.screen.blit(panel, (10, 10))
    for i, line in enumerate(lines):
        label = font.render(line, True, (230, 240, 250))
        game.screen.blit(label, (16, 14 + i * line_h))
