"""Tests for game."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pytest


def test_game_initialization(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert game.width == 1280
    assert game.height == 720
    assert hasattr(game, "camera_manager")


def test_draw_menu_gradient(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=100, height=100)
    game._draw_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR
    assert game.screen.get_at((0, 99))[:3] == (255, 255, 255)


def test_game_has_mp_type_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert game.mp_type_options == ["Offline", "Online", "Back"]


def test_game_initializes_objectives(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert game.objective_manager.objectives
    summary = game.objective_manager.summary()
    assert summary and isinstance(summary[0], str)


def test_draw_key_bindings_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)    
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=120, height=90)
    game._draw_key_bindings_menu()
    pixel = game.screen.get_at((0, 0))[:3]
    assert pixel[1:] == MENU_BG_COLOR[1:]


def test_controller_menu_options(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)    
    from hololive_coliseum.game import Game

    game = Game()
    assert "Controller Bindings" in game.settings_controls_options
    assert "Input Method" in game.settings_controls_options


def test_character_menu_has_ai_option(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)    
    from hololive_coliseum.game import Game

    game = Game()
    assert "Add AI Player" in game._character_menu_options()


def test_vote_menu_has_categories(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.open_vote_menu()
    assert "Biome" in game.vote_categories


def test_character_menu_has_difficulty(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)    
    from hololive_coliseum.game import Game

    game = Game()
    assert "Difficulty" in game._character_menu_options()
    assert game.difficulty_levels == [
        "Easy",
        "Normal",
        "Hard",
        "Elite",
        "Adaptive",
    ]


def test_watson_in_character_list(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Watson Amelia" in game.characters


def test_ina_in_character_list(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Ninomae Ina'nis" in game.characters


def test_fubuki_in_character_list(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Shirakami Fubuki" in game.characters


def test_character_list_has_22_entries(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert len(game.characters) == 22
    assert "Natsuiro Matsuri" in game.characters


def test_game_uses_map_manager(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.map_manager import MapManager

    game = Game()
    assert isinstance(game.map_manager, MapManager)
    assert game.map_manager.get_current() is not None


def test_ai_players_spawn(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game.ai_players = 2
    game._setup_level()
    assert len(game.enemies) == 2


def test_setup_level_resets_timers(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.spawn_manager.schedule("heal", 123)
    game.last_enemy_damage = 456
    game.ai_players = 0
    game._setup_level()
    assert len(game.spawn_manager.spawns) == 9
    assert game.last_enemy_damage == 0


def test_setup_level_adds_two_gravity_zones(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.ai_players = 0
    game.selected_character = "Gawr Gura"
    game._setup_level()
    assert len(game.gravity_zones) == 2
    multipliers = sorted(zone.multiplier for zone in game.gravity_zones)
    assert multipliers == [0.2, 2.0]


def test_spawn_manager_schedules_powerup(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    import pygame

    game = Game()
    game.ai_players = 0
    game._setup_level()
    assert game.spawn_manager.spawns


def test_mana_powerup_refills_mana(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.powerup import PowerUp

    game = Game()
    game.ai_players = 0
    game._setup_level()
    game.player.mana = 0
    p = PowerUp(game.player.rect.centerx, game.player.rect.centery, "mana")
    game.powerups.add(p)
    game._handle_powerup_collision()
    assert game.player.mana == game.player.max_mana


def test_stamina_powerup_refills_stamina(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.powerup import PowerUp

    game = Game()
    game.ai_players = 0
    game._setup_level()
    game.player.stamina_manager.stamina = 0
    p = PowerUp(game.player.rect.centerx, game.player.rect.centery, "stamina")
    game.powerups.add(p)
    game._handle_powerup_collision()
    assert (
        game.player.stamina_manager.stamina
        == game.player.stamina_manager.max_stamina
    )


def test_speed_powerup_boosts_player(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.powerup import PowerUp

    game = Game()
    game.ai_players = 0
    game._setup_level()
    p = PowerUp(game.player.rect.centerx, game.player.rect.centery, "speed")
    game.powerups.add(p)
    game._handle_powerup_collision()
    assert game.player.speed_factor > 1.0
    now = pygame.time.get_ticks() + 3000
    game.status_manager.update(now)
    assert game.player.speed_factor == 1.0


def test_shield_powerup_blocks_damage(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.powerup import PowerUp

    game = Game()
    game.ai_players = 0
    game._setup_level()
    p = PowerUp(game.player.rect.centerx, game.player.rect.centery, "shield")
    game.powerups.add(p)
    game._handle_powerup_collision()
    assert game.player.invincible
    game.player.take_damage(20)
    assert game.player.health == game.player.max_health
    now = pygame.time.get_ticks() + 1500
    game.status_manager.update(now)
    assert not game.player.invincible
    game.player.take_damage(20)
    assert game.player.health < game.player.max_health


def test_life_powerup_adds_life(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.powerup import PowerUp

    game = Game()
    game.ai_players = 0
    game._setup_level()
    initial = game.player.lives
    p = PowerUp(game.player.rect.centerx, game.player.rect.centery, "life")
    game.powerups.add(p)
    game._handle_powerup_collision()
    assert game.player.lives == initial + 1


def test_attack_powerup_boosts_player(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.powerup import PowerUp

    game = Game()
    game.ai_players = 0
    game._setup_level()
    base = game.player.stats.get("attack")
    p = PowerUp(game.player.rect.centerx, game.player.rect.centery, "attack")
    game.powerups.add(p)
    game._handle_powerup_collision()
    assert game.player.stats.get("attack") > base
    now = pygame.time.get_ticks() + 1500
    game.status_manager.update(now)
    assert game.player.stats.get("attack") == base


def test_defense_powerup_boosts_player(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.powerup import PowerUp

    game = Game()
    game.ai_players = 0
    game._setup_level()
    base = game.player.stats.get("defense")
    p = PowerUp(game.player.rect.centerx, game.player.rect.centery, "defense")
    game.powerups.add(p)
    game._handle_powerup_collision()
    assert game.player.stats.get("defense") > base
    now = pygame.time.get_ticks() + 1500
    game.status_manager.update(now)
    assert game.player.stats.get("defense") == base


def test_experience_powerup_grants_xp(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.powerup import PowerUp

    game = Game()
    game.ai_players = 0
    game._setup_level()
    base_xp = game.player.experience_manager.xp
    p = PowerUp(game.player.rect.centerx, game.player.rect.centery, "xp")
    game.powerups.add(p)
    game._handle_powerup_collision()
    assert game.player.experience_manager.xp > base_xp


def test_no_pickup_during_dodge(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.powerup import PowerUp

    game = Game()
    game.ai_players = 0
    game._setup_level()
    p = PowerUp(game.player.rect.x + 50, game.player.rect.y, "heal")
    game.powerups.add(p)
    now = pygame.time.get_ticks()
    game.player.dodging = True
    game.player.velocity.x = 100
    game.player.update(game.ground_y, now + 16)
    game._handle_powerup_collision()
    assert game.powerups


def test_enemy_ai_moves_toward_player(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    import pygame

    game = Game()
    game.ai_players = 1
    game._setup_level()
    game.last_enemy_damage = -1000
    enemy = next(iter(game.enemies))
    start_x = enemy.rect.x
    now = pygame.time.get_ticks()
    enemy.handle_ai(game.player, now, [], [])
    enemy.update(game.ground_y, now)
    assert enemy.rect.x != start_x


def test_enemy_collision_hurts_player(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.ai_players = 1
    game._setup_level()
    game.last_enemy_damage = -1000
    enemy = next(iter(game.enemies))
    enemy.rect.center = game.player.rect.center
    enemy.pos = pygame.math.Vector2(enemy.rect.topleft)
    game._handle_collisions()
    assert game.player.health < game.player.max_health
    pygame.quit()


def test_chapter_list_has_20_entries(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert len(game.chapters) == 20
    assert len(game.chapter_images) == 20


def test_map_menu_has_back_option(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)    
    from hololive_coliseum.game import Game

    game = Game()
    assert game._map_menu_options()[-1] == "Back"


def test_character_menu_has_back_option(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)    
    from hololive_coliseum.game import Game

    game = Game()
    assert game._character_menu_options()[-1] == "Back"


def test_pause_menu_options(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert game.pause_options == [
        "Resume",
        "Inventory",
        "Equipment",
        "Achievements",
        "Main Menu",
    ]


def test_draw_pause_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=90, height=90)
    game._draw_pause_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_draw_inventory_and_equipment(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR
    from hololive_coliseum.item_manager import Weapon

    game = Game(width=80, height=80)
    game.player.inventory.add("Sword")
    game.item_manager.add_item(Weapon("Sword", {}))
    game._draw_inventory_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR
    game.player.equipment.equip("weapon", "Sword")
    game._draw_equipment_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_main_menu_has_info_options(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Quick Start" in game.main_menu_options
    assert "How to Play" in game.main_menu_options
    assert "Credits" in game.main_menu_options
    assert "Achievements" in game.main_menu_options
    assert "Records" in game.main_menu_options
    assert "Goals" in game.main_menu_options
    assert "Vote" in game.main_menu_options


def test_quick_start_launches_playing(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game._quick_start()
    assert game.state == "playing"
    assert game.selected_chapter == game.chapters[0]
    assert game.player is not None


def test_first_blood_achievement(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game
    from hololive_coliseum.projectile import Projectile

    game = Game()
    game.ai_players = 1
    game._setup_level()
    enemy = next(iter(game.enemies))
    enemy.health = 1
    proj = Projectile(enemy.rect.centerx, enemy.rect.centery, pygame.math.Vector2())
    game.projectiles.add(proj)
    game.all_sprites.add(proj)
    game._handle_collisions()
    assert game.achievement_manager.is_unlocked("First Blood")
    pygame.quit()


def test_draw_how_to_play(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=80, height=80)
    game._draw_how_to_play()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_draw_credits(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=80, height=80)
    game._draw_credits()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_draw_scoreboard(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=80, height=80)
    game._draw_scoreboard_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_draw_goals_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=80, height=80)
    game._draw_goals_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_draw_achievements(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=80, height=80)
    game._draw_achievements_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_escape_enters_pause(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame
    from hololive_coliseum.game import Game

    game = Game()
    game.state = "playing"
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.state == "paused"


def test_draw_lobby_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=100, height=100)
    game.player_names = ["P1", "P2"]
    game._draw_lobby_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_cycle_volume(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.volume = 0.0
    game.sound_manager.volume = 0.0
    game.sound_manager.cycle_volume()
    assert game.sound_manager.volume == 0.5
    game.sound_manager.cycle_volume()
    assert game.sound_manager.volume == 1.0
    game.sound_manager.cycle_volume()
    assert game.sound_manager.volume == 0.0


def test_node_settings_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)    
    from hololive_coliseum.game import Game

    game = Game()
    assert "Node Settings" in game.settings_system_options
    assert game.node_options == [
        "Start Node",
        "Stop Node",
        "Latency Helper",
        "Background Mining",
        "Back",
    ]


def test_accounts_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)    
    from hololive_coliseum.game import Game

    game = Game()
    assert "Accounts" in game.settings_system_options
    assert game.account_options == [
        "Register Account",
        "Delete Account",
        "Renew Key",
        "Back",
    ]


def test_settings_menu_has_new_options(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)    
    from hololive_coliseum.game import Game

    game = Game()
    assert "Show FPS" in game.settings_display_options
    assert "Accessibility" in game.settings_system_options
    assert "Reset Records" in game.settings_system_options


def test_start_and_stop_node(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.start_node()
    assert game.network_manager is not None
    assert game.node_hosting
    game.stop_node()
    assert game.network_manager is None
    assert not game.node_hosting


def test_game_over_state(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.player.lives = 0
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.state == "game_over"
    pygame.quit()


def test_best_time_saved(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game, load_settings

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.level_start_time = pygame.time.get_ticks() - 3000
    game.player.lives = 0
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    settings = load_settings()
    assert settings.get("best_time", 0) >= 3
    pygame.quit()


def test_best_score_saved(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game, load_settings

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.score = 5
    game.player.lives = 0
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    settings = load_settings()
    assert settings.get("best_score", 0) >= 5
    pygame.quit()


def test_enemy_kill_increments_score(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)    
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game
    from hololive_coliseum.projectile import Projectile

    game = Game()
    game.selected_character = "Gawr Gura"
    game.ai_players = 1
    game._setup_level()
    enemy = next(iter(game.enemies))
    enemy.health = 5
    proj = Projectile(enemy.rect.centerx, enemy.rect.centery, pygame.math.Vector2(1, 0))
    game.projectiles.add(proj)
    game._handle_collisions()
    assert game.score >= 1
    assert len(game.enemies) == 0
    pygame.quit()


def test_victory_state(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.level_start_time = pygame.time.get_ticks() - game.level_limit * 1000 - 100
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.state == "victory"
    pygame.quit()


def test_final_time_victory(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.level_start_time = pygame.time.get_ticks() - game.level_limit * 1000 - 100
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.final_time >= game.level_limit
    pygame.quit()


def test_final_time_game_over(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.level_start_time = pygame.time.get_ticks() - 2000
    game.player.lives = 0
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.final_time >= 2
    pygame.quit()


def test_end_menu_options(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert game.game_over_options == ["Play Again", "Main Menu"]
    assert game.victory_options == ["Play Again", "Main Menu"]


def test_play_again_returns_to_char(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.state = "victory"
    game.show_end_options = True
    options = game._victory_menu_options()
    game.menu_index = options.index("Play Again")
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.state == "char"
    pygame.quit()


def test_chat_toggle_and_send(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": "\r"}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_h, "unicode": "h"}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_i, "unicode": "i"}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": "\r"}))
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert not game.chat_manager.open
    assert game.chat_manager.history() == [("Player 1", "hi")]
    pygame.quit()


def test_f12_captures_screenshot(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    monkeypatch.setattr("hololive_coliseum.screenshot_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    shots_dir = tmp_path / "screenshots"
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_F12}))
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert len(list(shots_dir.iterdir())) == 1
    pygame.quit()


def test_game_hud_auto_dev_summary(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    class DummyFeedback:
        def region_insight(self):
            return {
                "trending_hazard": "lava",
                "favorite_character": "Calli",
                "average_score": 1234.6,
                "average_time": 182,
                "hazard_challenge": {"hazard": "spike", "target": 4},
            }

        def estimate_recommended_level(self, base_level: int = 1) -> int:
            return base_level + 4

    game = Game(width=80, height=80)
    game.auto_dev_manager = DummyFeedback()
    game.auto_dev_support_plan = {"hazard": "storm"}
    game.auto_dev_projection_summary = {"focus": [{"hazard": "poison"}]}
    summary = game._hud_auto_dev_summary()
    assert ("Trend", "lava") in summary
    assert ("Favorite", "Calli") in summary
    assert ("Avg Score", 1235) in summary
    assert ("Avg Time", "182s") in summary
    assert ("Rec Lv", 5) in summary
    assert ("Support", "storm") in summary
    assert any(label == "Focus" and value == "poison" for label, value in summary)
    pygame.quit()


def test_game_hud_world_activity(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    class DummyRegionManager:
        def get_regions(self):
            return [
                {
                    "name": "region_7",
                    "recommended_level": 4,
                    "quest": {"name": "Rescue"},
                    "auto_dev": {
                        "support_plan": {"hazard": "aurora"},
                        "network_upgrade_backlog": ["relay", "firmware"],
                    },
                }
            ]

    class DummyWorldGeneration:
        def __init__(self):
            self.region_manager = DummyRegionManager()

    game = Game(width=80, height=80)
    game.world_generation_manager = DummyWorldGeneration()
    lines = game._hud_world_activity()
    assert "Regions: 1" in lines
    assert any(line == "Latest: region_7" for line in lines)
    assert any(line == "Upgrades: 2" for line in lines)
    assert any(line.startswith("Quest:") for line in lines)
    pygame.quit()
