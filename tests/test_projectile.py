"""Tests for projectile."""

import os
import sys
import pytest

# Unit tests covering projectile and melee behavior.

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

pygame = pytest.importorskip("pygame")
from hololive_coliseum.projectile import (
    Projectile,
    PROJECTILE_SPEED,
    ExplodingProjectile,
    ExplosionProjectile,
    EXPLODE_TIME,
    PoisonProjectile,
    BurningProjectile,
    StunningProjectile,
    ShockwaveProjectile,
    MelodyProjectile,
)
from hololive_coliseum.melee_attack import MeleeAttack, MELEE_LIFETIME


def test_projectile_moves():
    direction = pygame.math.Vector2(1, 0)
    proj = Projectile(0, 0, direction)
    orig_x = proj.rect.x
    proj.update()
    assert proj.rect.x == orig_x + PROJECTILE_SPEED


def test_projectile_aims_toward_target():
    direction = pygame.math.Vector2(10, 0)
    proj = Projectile(0, 0, direction)
    assert proj.velocity.x > 0 and proj.velocity.y == 0


def test_melee_attack_lifetime():
    attack = MeleeAttack(0, 0, 1)
    for _ in range(MELEE_LIFETIME):
        attack.update()
    # Should be killed after lifetime expires
    assert not attack.alive()


def test_player_shoot_zero_vector(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.player import PlayerCharacter

    player = PlayerCharacter(0, 0)
    player.last_shot = -1000
    now = pygame.time.get_ticks()
    proj = player.shoot(now, player.rect.center)
    assert proj is not None
    assert proj.velocity.x == PROJECTILE_SPEED
    assert proj.velocity.y == 0
    pygame.quit()


def test_projectile_hits_enemy(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.ai_players = 1
    game._setup_level()
    enemy = next(iter(game.enemies))
    proj = Projectile(enemy.rect.centerx, enemy.rect.centery, pygame.math.Vector2(0, 0))
    game.projectiles.add(proj)
    game.all_sprites.add(proj)
    game._handle_collisions()
    assert enemy.health < enemy.max_health
    pygame.quit()


def test_exploding_projectile_expires():
    proj = ExplodingProjectile(0, 0, pygame.math.Vector2(1, 0))
    for _ in range(EXPLODE_TIME):
        proj.update()
    assert not proj.alive()


def test_explosion_projectile_stays_put():
    proj = ExplosionProjectile(5, 5)
    assert proj.velocity.x == 0 and proj.velocity.y == 0


def test_explosion_projectile_expires():
    proj = ExplosionProjectile(5, 5)
    for _ in range(5):
        proj.update()
    assert not proj.alive()


def test_poison_projectile_flags_poison():
    proj = PoisonProjectile(0, 0, pygame.math.Vector2(1, 0))
    assert getattr(proj, "poison", False)


def test_burning_projectile_flags_burn():
    proj = BurningProjectile(0, 0, pygame.math.Vector2(1, 0))
    assert getattr(proj, "burn", False)


def test_stunning_projectile_flags_stun():
    proj = StunningProjectile(0, 0, pygame.math.Vector2(1, 0))
    assert getattr(proj, "stun", False)


def test_shockwave_projectile_horizontal():
    proj = ShockwaveProjectile(0, 0, pygame.math.Vector2(1, 0))
    assert proj.velocity.y == 0


def test_melody_projectile_oscillates():
    proj = MelodyProjectile(0, 0, pygame.math.Vector2(1, 0))
    start_y = proj.rect.y
    proj.update()
    assert proj.rect.y != start_y
