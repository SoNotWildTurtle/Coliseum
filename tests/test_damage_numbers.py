"""Tests for damage numbers."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

pygame = pytest.importorskip("pygame")

from hololive_coliseum.projectile import Projectile


def test_damage_number_spawns(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.ai_players = 1
    game._setup_level()
    enemy = next(iter(game.enemies))
    proj = Projectile(enemy.rect.centerx, enemy.rect.centery, pygame.math.Vector2())
    game.projectiles.add(proj)
    game.all_sprites.add(proj)
    game._handle_collisions()
    assert len(game.damage_numbers) == 1
    now = pygame.time.get_ticks() + 1000
    game.damage_numbers.update(now)
    assert len(game.damage_numbers) == 0
    pygame.quit()


def test_critical_damage_number_color(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.ai_players = 1
    game._setup_level()
    enemy = next(iter(game.enemies))

    def fake_calc(
        self,
        base,
        defense=0,
        multiplier=1.0,
        crit_chance=0,
        crit_multiplier=2.0,
        return_crit=False,
    ):
        return (1, True) if return_crit else 1

    monkeypatch.setattr(
        "hololive_coliseum.combat_manager.DamageManager.calculate", fake_calc
    )

    proj = Projectile(enemy.rect.centerx, enemy.rect.centery, pygame.math.Vector2())
    game.projectiles.add(proj)
    game.all_sprites.add(proj)
    game._handle_collisions()
    color = game.damage_numbers.sprites()[0].image.get_at((0, 0))[:3]
    assert color == (255, 255, 0)
    pygame.quit()
