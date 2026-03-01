"""Integration tests for combat scenarios."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.game import Game
from hololive_coliseum.hazards import LavaZone
from hololive_coliseum.melee_attack import MeleeAttack
from hololive_coliseum.player import Enemy
from hololive_coliseum.projectile import FreezingProjectile
from hololive_coliseum.status_effects import ShieldEffect


def _build_game(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    return game


def test_projectile_melee_and_status_effects(tmp_path, monkeypatch):
    game = _build_game(tmp_path, monkeypatch)
    enemy = Enemy(game.player.rect.centerx + 10, game.ground_y - 60)
    enemy.health = 40
    enemy.stats.apply_modifier("defense", -enemy.stats.get("defense"))
    game.enemies.add(enemy)
    game.all_sprites.add(enemy)

    proj = FreezingProjectile(
        enemy.rect.centerx,
        enemy.rect.centery,
        pygame.math.Vector2(1, 0),
    )
    proj.owner = game.player
    proj.attack = 10
    game.projectiles.add(proj)

    melee = MeleeAttack(
        game.player.rect.centerx,
        game.player.rect.centery,
        1,
        owner=game.player,
    )
    game.melee_attacks.add(melee)

    start_health = enemy.health
    game._handle_collisions()

    assert enemy.health < start_health
    effects = game.status_manager.active_effects(enemy)
    assert any(entry["name"] == "Freeze" for entry in effects)
    assert len(game.damage_numbers) >= 1
    pygame.quit()


def test_enemy_melee_respects_shield(tmp_path, monkeypatch):
    game = _build_game(tmp_path, monkeypatch)
    enemy = Enemy(game.player.rect.centerx + 10, game.ground_y - 60)
    game.enemies.add(enemy)
    game.all_sprites.add(enemy)

    game.status_manager.add_effect(game.player, ShieldEffect(duration_ms=1000))
    melee = MeleeAttack(
        game.player.rect.centerx,
        game.player.rect.centery,
        1,
        owner=enemy,
        from_enemy=True,
    )
    game.melee_attacks.add(melee)

    start_health = game.player.health
    game._handle_collisions()

    assert game.player.health == start_health
    pygame.quit()


def test_hazard_damage_and_combat_stack(tmp_path, monkeypatch):
    game = _build_game(tmp_path, monkeypatch)
    enemy = Enemy(game.player.rect.centerx + 10, game.ground_y - 60)
    enemy.health = 20
    enemy.stats.apply_modifier("defense", -enemy.stats.get("defense"))
    game.enemies.add(enemy)
    game.all_sprites.add(enemy)

    lava = LavaZone(game.player.rect.copy(), damage=3, interval=0)
    game.hazard_manager.hazards.add(lava)
    game.hazard_manager.last_damage = -1000

    proj = FreezingProjectile(
        enemy.rect.centerx,
        enemy.rect.centery,
        pygame.math.Vector2(1, 0),
    )
    proj.owner = game.player
    proj.attack = 8
    game.projectiles.add(proj)

    player_start = game.player.health
    enemy_start = enemy.health
    now = pygame.time.get_ticks()
    game.hazard_manager.apply_to_player(game.player, now)
    game._handle_collisions()

    assert game.player.health < player_start
    assert enemy.health < enemy_start
    pygame.quit()
