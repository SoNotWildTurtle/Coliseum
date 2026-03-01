"""Setup helpers for game initialization sequences."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pygame

from .placeholder_sprites import ensure_placeholder_sprites
from .story_maps import create_story_maps

if TYPE_CHECKING:
    from .game import Game


def _create_icon(text: str, size: tuple[int, int]) -> pygame.Surface:
    surf = pygame.Surface(size)
    surf.fill((200, 200, 200))
    font = pygame.font.SysFont(None, 20)
    label = font.render(text, True, (0, 0, 0))
    surf.blit(label, label.get_rect(center=(size[0] // 2, size[1] // 2)))
    return surf


def _load_image(image_dir: str, name: str, size: tuple[int, int]) -> pygame.Surface:
    path = os.path.join(image_dir, name)
    if os.path.exists(path):
        surf = pygame.image.load(path).convert_alpha()
        if size and (surf.get_size() != size):
            surf = pygame.transform.smoothscale(surf, size)
        return surf
    return _create_icon(os.path.splitext(name)[0], size)


def _name_to_file(name: str) -> str:
    base = name.replace(" ", "_").replace("'", "").replace(".", "")
    return f"{base}_right.png"


def _map_name_to_file(name: str) -> str:
    base = name.lower().replace(" ", "_").replace("'", "").replace(".", "")
    return f"map_{base}.png"


def configure_story_and_ui(game: Game, image_dir: str) -> None:
    """Wire story maps, UI defaults, and menu image assets."""
    for name, data in create_story_maps(game.characters).items():
        game.map_manager.add_map(name, data)
    game.map_manager.set_current("Default")
    game.maps = list(game.map_manager.maps.keys())
    game.map_filters = [
        "All",
        "Story",
        "Arena",
        "Low Hazards",
        "High Hazards",
        "Boss",
    ]
    game.map_filter = "All"
    game.map_preview_cache = {}
    game.chapter_preview_cache = {}
    game.chapters = [f"Chapter {i}" for i in range(1, 21)]
    ensure_placeholder_sprites(
        image_dir,
        game.characters,
        chapter_count=len(game.chapters),
        map_names=game.maps,
    )
    game.difficulty_levels = ["Easy", "Normal", "Hard", "Elite", "Adaptive"]
    game.difficulty_index = 1
    game.character_page = 0
    game.map_page = 0
    game.character_page_size = 15
    game.map_page_size = 15
    game.chapter_menu_options = game.chapters + ["Back"]
    game.vote_categories = []
    game.vote_options = []
    game.active_vote_manager = None
    game.lobby_options = ["Start Game", "Back"]
    game.human_players = 1
    game.ai_players = 0
    game.character_selections = [None]
    game.map_selections = [None]
    game.character_select_index = 0
    game.map_select_index = 0
    game.map_select_message = ""
    if game.autoplay and game.autoplay_ai_players > 0:
        game.ai_players = max(0, min(3, game.autoplay_ai_players))
    game.player_names = ["Player 1"]
    game.multiplayer = False
    game.selected_mode = None
    game.selected_character = None
    game.selected_map = None
    game.selected_chapter = None
    if game.autoplay:
        game.selected_character = game.characters[0]
        game.selected_mode = "Story"
        game.selected_chapter = game.chapters[0] if game.chapters else None
        if not game.autoplay_flow:
            game.state = "playing"

    game.character_images = {
        name: _load_image(image_dir, _name_to_file(name), (64, 64))
        for name in game.characters
    }
    game.map_images = {
        name: _load_image(image_dir, _map_name_to_file(name), (64, 64))
        for name in game.map_manager.maps
    }
    game.chapter_images = {
        f"Chapter {i}": _load_image(image_dir, f"chapter{i}.png", (64, 64))
        for i in range(1, 21)
    }

    game._apply_font_scale()
    game.menu_drawers = {
        "splash": game._draw_menu,
        "main_menu": game._draw_main_menu,
        "mode": lambda: game._draw_option_menu("Game Type", game.mode_options),
        "solo_multi": lambda: game._draw_option_menu(
            "Players", game.solo_multi_options
        ),
        "mp_type": lambda: game._draw_option_menu(
            "Multiplayer", game.mp_type_options
        ),
        "char": game._draw_character_menu,
        "map": game._draw_map_menu,
        "chapter": game._draw_chapter_menu,
        "lobby": game._draw_lobby_menu,
        "settings": game._draw_settings_menu,
        "settings_controls": lambda: game._draw_option_menu(
            "Controls", game.settings_controls_options
        ),
        "settings_display": lambda: game._draw_option_menu(
            "Display", game.settings_display_options
        ),
        "settings_audio": lambda: game._draw_option_menu(
            "Audio", game.settings_audio_options
        ),
        "settings_system": lambda: game._draw_option_menu(
            "System", game.settings_system_options
        ),
        "match_options": lambda: game._draw_option_menu(
            "Match Options", game.match_options
        ),
        "key_bindings": game._draw_key_bindings_menu,
        "controller_bindings": game._draw_controller_bindings_menu,
        "rebind": game._draw_rebind_prompt,
        "rebind_controller": game._draw_rebind_controller_prompt,
        "node_settings": game._draw_node_menu,
        "accessibility": game._draw_accessibility_menu,
        "accounts": game._draw_accounts_menu,
        "howto": game._draw_how_to_play,
        "credits": game._draw_credits,
        "scoreboard": game._draw_scoreboard_menu,
        "achievements": game._draw_achievements_menu,
        "vote_category": lambda: game._draw_option_menu(
            "Vote", game.vote_categories
        ),
        "vote": lambda: game._draw_option_menu("Weekly Vote", game.vote_options),
        "goals": game._draw_goals_menu,
        "paused": game._draw_pause_menu,
        "inventory": game._draw_inventory_menu,
        "equipment": game._draw_equipment_menu,
        "victory": game._draw_victory_menu,
        "victory_report": game._draw_victory_report,
        "victory_briefing": game._draw_victory_briefing,
        "victory_actions": game._draw_victory_actions,
        "game_over": game._draw_game_over_menu,
        "mmo": game._draw_mmo_world,
    }
