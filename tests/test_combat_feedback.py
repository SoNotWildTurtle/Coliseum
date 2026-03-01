"""Tests for combat feedback hooks (SFX and knockback)."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.combat_manager import CombatManager
from hololive_coliseum.player import PlayerCharacter, Enemy
from hololive_coliseum.projectile import Projectile
from hololive_coliseum.melee_attack import MeleeAttack


class DummySound:
    def __init__(self) -> None:
        self.last_played = None

    def play(self, name: str) -> None:
        self.last_played = name

    def play_event(self, name: str) -> None:
        self.last_played = name


def test_hit_sfx_plays_on_projectile_damage():
    pygame.init()
    pygame.display.set_mode((1, 1))
    sound = DummySound()
    combat = CombatManager(sound_manager=sound)
    player = PlayerCharacter(0, 0)
    enemy = Enemy(40, 0)
    proj = Projectile(enemy.rect.centerx, enemy.rect.centery, pygame.math.Vector2(1, 0))
    proj.owner = player
    projectiles = pygame.sprite.Group(proj)
    melee = pygame.sprite.Group()
    enemies = pygame.sprite.Group(enemy)

    combat.handle_collisions(
        player,
        enemies,
        projectiles,
        melee,
        pygame.time.get_ticks(),
    )

    assert sound.last_played in {"hit_light", "hit_heavy", "hit_crit"}
    pygame.quit()


def test_melee_knockback_pushes_enemy():
    pygame.init()
    pygame.display.set_mode((1, 1))
    combat = CombatManager()
    player = PlayerCharacter(0, 0)
    enemy = Enemy(30, 0)
    attack = MeleeAttack(player.rect.centerx + 20, player.rect.centery, 1, owner=player)
    attack.rect.center = enemy.rect.center
    melee = pygame.sprite.Group(attack)
    enemies = pygame.sprite.Group(enemy)

    combat.handle_collisions(
        player,
        enemies,
        pygame.sprite.Group(),
        melee,
        pygame.time.get_ticks(),
    )

    assert enemy.velocity.x != 0
    pygame.quit()


def test_melee_swing_plays_sfx():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    sound = DummySound()
    player.sound_manager = sound
    player.melee_attack(pygame.time.get_ticks())
    assert sound.last_played == "melee_swing"
    pygame.quit()


def test_special_cast_plays_sfx_even_without_projectile():
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.player import KiaraPlayer

    player = KiaraPlayer(0, 0)
    sound = DummySound()
    player.sound_manager = sound
    player.special_attack(pygame.time.get_ticks())
    assert sound.last_played.startswith("special_cast")
    pygame.quit()
