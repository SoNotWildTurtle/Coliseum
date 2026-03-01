"""Tests for enemy ai."""

import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

pygame = pytest.importorskip("pygame")
from hololive_coliseum.player import PlayerCharacter, Enemy, BossEnemy
from hololive_coliseum.projectile import Projectile
from hololive_coliseum.game import Game


def test_enemy_difficulty_reaction(monkeypatch):
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(100, 100)
    monkeypatch.setattr('random.random', lambda: 0.0)
    easy = Enemy(0, 100, difficulty="Easy")
    hard = Enemy(0, 100, difficulty="Hard")
    now = pygame.time.get_ticks()
    assert easy.handle_ai(player, now + 150, [], []) == (None, None)
    proj, melee = hard.handle_ai(player, now + 150, [], [])
    assert proj or melee
    proj2, melee2 = easy.handle_ai(player, now + 650, [], [])
    assert proj2 or melee2
    pygame.quit()


def test_enemy_projectile_hits_player(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    monkeypatch.setattr('random.random', lambda: 0.0)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.selected_character = "Gawr Gura"
    game.ai_players = 1
    game.difficulty_index = 2  # Hard
    game._setup_level()
    enemy = next(iter(game.enemies))
    enemy.last_ai_action = -1000
    now = pygame.time.get_ticks()
    proj, _ = enemy.handle_ai(game.player, now + 200, [], [])
    assert proj is not None
    proj.rect.center = game.player.rect.center
    game.projectiles.add(proj)
    game.all_sprites.add(proj)
    game._handle_collisions()
    assert game.player.health < game.player.max_health
    pygame.quit()


def test_enemy_dodges_projectile(monkeypatch):
    monkeypatch.setattr('random.random', lambda: 0.0)
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(100, 100)
    enemy = Enemy(50, 100, difficulty="Hard")
    proj = Projectile(55, 100, pygame.math.Vector2(-1, 0))
    projectiles = [proj]
    now = pygame.time.get_ticks() + 1000
    enemy.handle_ai(player, now, [], projectiles)
    assert enemy.dodging
    pygame.quit()


def test_enemy_dodges_close_player(monkeypatch):
    monkeypatch.setattr('random.random', lambda: 0.0)
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(100, 100)
    enemy = Enemy(130, 100, difficulty="Hard")
    now = pygame.time.get_ticks() + 1000
    enemy.handle_ai(player, now, [], [])
    assert enemy.dodging
    pygame.quit()


def test_enemy_blocks_projectile(monkeypatch):
    monkeypatch.setattr('random.random', lambda: 0.5)
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(100, 100)
    monkeypatch.setitem(
        Enemy.AI_LEVELS,
        'BlockTest',
        {
            'react_ms': 0,
            'speed': 1.0,
            'shoot_prob': 0.0,
            'melee_prob': 0.0,
            'jump_prob': 0.0,
            'dodge_prob': 0.0,
            'block_prob': 1.0,
            'lead_frames': 0,
        },
    )
    enemy = Enemy(90, 100, difficulty='BlockTest')
    proj = Projectile(95, 100, pygame.math.Vector2(-1, 0))
    projectiles = [proj]
    now = pygame.time.get_ticks() + 1000
    enemy.handle_ai(player, now, [], projectiles)
    assert enemy.blocking
    pygame.quit()


def test_enemy_retreats_when_low_health(monkeypatch):
    monkeypatch.setattr('random.random', lambda: 0.0)
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(100, 100)
    enemy = Enemy(50, 100, difficulty="Normal")
    enemy.health_manager.health = enemy.health = enemy.max_health // 5
    now = pygame.time.get_ticks() + 1000
    proj, melee = enemy.handle_ai(player, now, [], [])
    assert proj is None and melee is None
    assert enemy.velocity.x < 0
    assert enemy.direction == -1
    pygame.quit()


def test_hard_ai_leads_moving_target(monkeypatch):
    monkeypatch.setattr('random.random', lambda: 0.0)
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(100, 0)
    player.velocity.y = -5
    enemy = Enemy(0, 0, difficulty="Hard")
    enemy.last_ai_action = -1000
    now = pygame.time.get_ticks() + 1000
    proj, _ = enemy.handle_ai(player, now, [], [])
    assert proj is not None
    assert proj.velocity.y < 0
    pygame.quit()


def test_boss_enemy_special_attack(monkeypatch):
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(100, 100)
    boss = BossEnemy(50, 100, difficulty="Hard")
    boss.last_ai_action = -1000
    now = pygame.time.get_ticks() + 2500
    proj, melee = boss.handle_ai(player, now, [], [])
    assert proj is not None and proj.from_enemy
    pygame.quit()


def test_enemy_patrols_when_far(monkeypatch):
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(1000, 100)
    enemy = Enemy(0, 100, difficulty="Normal")
    enemy.last_ai_action = -1000
    now = pygame.time.get_ticks() + 1000
    proj, melee = enemy.handle_ai(player, now, [], [])
    assert proj is None and melee is None
    assert enemy.velocity.x != 0
    pygame.quit()
