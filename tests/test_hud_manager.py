"""Tests for hud manager."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

pytest.importorskip("pygame")
import pygame
from hololive_coliseum.hud_manager import HUDManager
from hololive_coliseum.player import PlayerCharacter


def test_hud_manager_draw():
    pygame.init()
    screen = pygame.display.set_mode((120, 60))
    hud = HUDManager()
    player = PlayerCharacter(0, 0)
    hud.draw(screen, player, score=5, elapsed=10, cooldowns=[])
    # pixel inside the health bar should be green
    assert screen.get_at((15, 10))[:3] == (0, 255, 0)
    pygame.quit()


def test_hud_manager_draw_combo():
    pygame.init()
    screen = pygame.display.set_mode((200, 120))
    hud = HUDManager()
    player = PlayerCharacter(0, 0)
    hud.draw(screen, player, score=0, elapsed=0, combo=2)
    pixels = [screen.get_at((15, y))[:3] for y in range(85, 100)]
    assert any(color != (0, 0, 0) for color in pixels)
    pygame.quit()


def test_hud_manager_draw_objectives():
    pygame.init()
    screen = pygame.display.set_mode((240, 140))
    hud = HUDManager()
    player = PlayerCharacter(0, 0)
    hud.draw(
        screen,
        player,
        score=0,
        elapsed=0,
        objectives=["• Defeat 5 foes: 1/5", "• Gather coins: 0/10"],
    )
    objective_pixels = [screen.get_at((15, y))[:3] for y in range(110, 140, 10)]
    assert any(color != (0, 0, 0) for color in objective_pixels)
    pygame.quit()


def test_hud_manager_draw_resource_summary():
    pygame.init()
    screen = pygame.display.set_mode((320, 180))
    hud = HUDManager()
    player = PlayerCharacter(0, 0)
    hud.draw(
        screen,
        player,
        score=0,
        elapsed=0,
        resource_summary=[("Coins", 12), ("Inventory", "3/30")],
    )
    pixel = screen.get_at((screen.get_width() - 15, 50))[:3]
    assert pixel != (0, 0, 0)
    pygame.quit()


def test_hud_manager_draw_status_effects():
    pygame.init()
    screen = pygame.display.set_mode((320, 180))
    hud = HUDManager()
    player = PlayerCharacter(0, 0)
    hud.draw(
        screen,
        player,
        score=0,
        elapsed=0,
        status_effects=[{"name": "Speed", "remaining_ms": 2000}],
    )
    pixel = screen.get_at((screen.get_width() - 15, screen.get_height() - 15))[:3]
    assert pixel != (0, 0, 0)
    pygame.quit()


def test_hud_manager_draw_auto_dev_panel():
    pygame.init()
    screen = pygame.display.set_mode((360, 200))
    hud = HUDManager()
    player = PlayerCharacter(0, 0)
    hud.draw(
        screen,
        player,
        score=0,
        elapsed=0,
        auto_dev_summary=[("Trend", "Lava"), ("Rec Lv", 5)],
    )
    pixel = screen.get_at((screen.get_width() - 15, 70))[:3]
    assert pixel != (0, 0, 0)
    pygame.quit()


def test_hud_manager_draw_world_ticker():
    pygame.init()
    screen = pygame.display.set_mode((360, 220))
    hud = HUDManager()
    player = PlayerCharacter(0, 0)
    hud.draw(
        screen,
        player,
        score=0,
        elapsed=0,
        world_activity=["Regions: 3", "Latest: region_1"],
    )
    pixel = screen.get_at((screen.get_width() // 2, screen.get_height() - 80))[:3]
    assert pixel != (0, 0, 0)
    pygame.quit()
