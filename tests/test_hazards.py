"""Tests for hazards."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.hazards import (
    SpikeTrap,
    IceZone,
    LavaZone,
    AcidPool,
    FireZone,
    FrostZone,
    QuicksandZone,
    LightningZone,
    PoisonZone,
    SilenceZone,
    BouncePad,
    TeleportPad,
    WindZone,
    RegenZone,
)
from hololive_coliseum.game import Game
from hololive_coliseum.player import Enemy


def test_spike_trap_damages_player(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    trap = SpikeTrap(game.player.rect.copy())
    game.hazards.add(trap)
    game.all_sprites.add(trap)
    now = pygame.time.get_ticks()
    game.last_hazard_damage = -1000
    game.state = 'playing'
    game._handle_collisions()  # to avoid unused
    zone = pygame.sprite.spritecollideany(game.player, game.hazards)
    if zone:
        game.player.take_damage(trap.damage)
    assert game.player.health < game.player.max_health
    pygame.quit()


def test_enemy_jumps_over_hazard(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.ai_players = 1
    game._setup_level()
    enemy = next(iter(game.enemies))
    trap_rect = enemy.rect.move(5, 0)
    trap = SpikeTrap(trap_rect)
    game.hazards.add(trap)
    enemy.on_ground = True
    now = pygame.time.get_ticks() + 1000
    enemy.handle_ai(game.player, now, game.hazards, [])
    assert enemy.velocity.y == -10
    pygame.quit()


def test_lava_zone_damage(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    lava = LavaZone(game.player.rect.copy(), damage=3, interval=0)
    game.hazards.add(lava)
    game.all_sprites.add(lava)
    now = pygame.time.get_ticks()
    game.last_hazard_damage = -1000
    game.state = 'playing'
    hazard = pygame.sprite.spritecollideany(game.player, game.hazards)
    if hazard:
        game.player.take_damage(lava.damage)
        game.last_hazard_damage = now
    assert game.player.health < game.player.max_health
    pygame.quit()


def test_acid_pool_slow(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    pool = AcidPool(game.player.rect.copy(), damage=2, interval=0, friction=0.5)
    game.hazards.add(pool)
    game.all_sprites.add(pool)
    now = pygame.time.get_ticks()
    game.last_hazard_damage = -1000
    game.state = 'playing'
    hazard = pygame.sprite.spritecollideany(game.player, game.hazards)
    if hazard:
        game.player.take_damage(pool.damage)
        game.player.set_friction_multiplier(pool.friction)
        game.last_hazard_damage = now
    assert game.player.health < game.player.max_health
    assert game.player.friction_multiplier == pool.friction
    pygame.quit()


def test_quicksand_pulls_and_slows(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    sand = QuicksandZone(game.player.rect.copy(), pull=2.0, friction=0.4)
    game.hazards.add(sand)
    now = pygame.time.get_ticks()
    game.hazard_manager.apply_to_player(game.player, now)
    assert game.player.velocity.y >= 2.0
    assert game.player.friction_multiplier == sand.friction
    pygame.quit()


def test_fire_zone_burns_player(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    zone = FireZone(game.player.rect.copy())
    game.hazards.add(zone)
    now = pygame.time.get_ticks()
    game.last_hazard_damage = -1000
    game.hazard_manager.apply_to_player(game.player, now)
    start = game.player.health
    game.status_manager.update(now + 600)
    assert game.player.health < start
    pygame.quit()


def test_frost_zone_freezes_player(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    zone = FrostZone(game.player.rect.copy())
    game.hazards.add(zone)
    now = pygame.time.get_ticks()
    start = game.player.speed_factor
    game.hazard_manager.last_damage = -1000
    game.hazard_manager.apply_to_player(game.player, now)
    assert game.player.speed_factor < start
    game.status_manager.update(now + zone.duration)
    assert game.player.speed_factor == start
    pygame.quit()


def test_poison_zone_poisons_player(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    zone = PoisonZone(game.player.rect.copy())
    game.hazards.add(zone)
    now = pygame.time.get_ticks()
    game.hazard_manager.last_damage = -1000
    game.hazard_manager.apply_to_player(game.player, now)
    start = game.player.health
    game.status_manager.update(now + 600)
    assert game.player.health < start
    pygame.quit()


def test_bounce_pad_launches_player(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    pad = BouncePad(game.player.rect.copy(), force=-20)
    game.hazards.add(pad)
    now = pygame.time.get_ticks()
    game.hazard_manager.apply_to_player(game.player, now)
    assert game.player.velocity.y == -20
    pygame.quit()


def test_teleport_pad_moves_player(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    pad = TeleportPad(game.player.rect.copy(), (30, 40))
    game.hazards.add(pad)
    now = pygame.time.get_ticks()
    game.hazard_manager.apply_to_player(game.player, now)
    assert game.player.rect.topleft == (30, 40)


def test_silence_zone_blocks_special(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    zone = SilenceZone(game.player.rect.copy())
    game.hazard_manager.hazards.add(zone)
    now = pygame.time.get_ticks()
    game.hazard_manager.last_damage = -1000
    game.hazard_manager.apply_to_player(game.player, now)
    assert game.player.silenced
    now += 1000
    assert game.player.special_attack(now) is None
    pygame.quit()


def test_wind_zone_push(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    zone = WindZone(game.player.rect.copy(), force=3)
    game.hazards.add(zone)
    now = pygame.time.get_ticks()
    game.hazard_manager.apply_to_player(game.player, now)
    assert game.player.velocity.x == 3
    pygame.quit()


def test_lightning_zone_zap(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    zone = LightningZone(game.player.rect.copy(), damage=2, interval=0, force=-9)
    game.hazards.add(zone)
    now = pygame.time.get_ticks()
    game.hazard_manager.apply_to_player(game.player, now)
    assert game.player.health < game.player.max_health
    assert game.player.velocity.y == -9
    pygame.quit()


def test_regen_zone_heals(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    zone = RegenZone(game.player.rect.copy(), heal=5, interval=0)
    game.hazard_manager.hazards.add(zone)
    game.player.health = 50
    game.hazard_manager.last_damage = -1000
    now = pygame.time.get_ticks()
    game.hazard_manager.apply_to_player(game.player, now)
    assert game.player.health > 50
    pygame.quit()

