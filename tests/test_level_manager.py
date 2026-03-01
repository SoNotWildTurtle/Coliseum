"""Tests for level manager."""

import pytest

pygame = pytest.importorskip("pygame")


def test_level_manager_sets_up_groups(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.ai_players = 1
    game.selected_character = "Gawr Gura"
    game.level_manager.setup_level()
    assert isinstance(game.player, game.player.__class__)
    assert len(game.enemies) == 1
    assert game.spawn_manager.spawns
    pygame.quit()


def test_story_boss_and_minions(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.selected_character = "Gawr Gura"
    game.selected_chapter = "Chapter 3"
    game.ai_players = 0
    game.level_manager.setup_level()
    data = game.map_manager.get_current()
    minions = data.get("minions", 0)
    boss_present = 1 if data.get("boss") else 0
    assert len(game.enemies) == minions + boss_present
    pygame.quit()


def test_story_minions_every_chapter(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.selected_character = "Gawr Gura"
    game.selected_chapter = "Chapter 1"
    game.level_manager.setup_level()
    data = game.map_manager.get_current()
    assert data["minions"] == len(game.enemies)
    pygame.quit()


def test_platforms_loaded(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.selected_character = "Gawr Gura"
    game.selected_chapter = "Chapter 8"
    game.level_manager.setup_level()
    data = game.map_manager.get_current()
    base = len(data.get("platforms", []))
    moving = len(data.get("moving_platforms", []))
    crumbling = len(data.get("crumbling_platforms", []))
    assert len(game.platforms) == base + moving + crumbling
    plat = next(iter(game.platforms))
    game.player.rect.midbottom = plat.rect.midtop
    game.player.pos = pygame.math.Vector2(game.player.rect.topleft)
    game.player.velocity.y = 5
    game.player.update(game.ground_y)
    assert game.player.rect.bottom == plat.rect.top
    pygame.quit()


def test_auto_dev_tuning_adjusts_spawn_schedule(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    monkeypatch.setattr("pygame.time.get_ticks", lambda: 1000)
    from hololive_coliseum.game import Game
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.auto_dev_manager.start_match("Gawr Gura", "Arena")
    for _ in range(6):
        game.auto_dev_manager.record_hazard("lava")
    game.auto_dev_manager.finalize("loss", 1200, 90)
    game.selected_character = "Gawr Gura"
    game.level_manager.setup_level()
    spawn_times = {obj: t for t, obj in game.spawn_manager.spawns}
    assert spawn_times["shield"] < 1000 + 9000
    assert spawn_times["defense"] < 1000 + 10500
    assert game.auto_dev_support_plan["hazard"] == "lava"
    assert game.auto_dev_projection_summary["focus"][0]["hazard"] == "lava"
    pygame.quit()
