"""Regression tests for multi-entity combat ticks."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.ally_fighter import AllyFighter
from hololive_coliseum.combat_manager import CombatManager
from hololive_coliseum.melee_attack import MeleeAttack
from hololive_coliseum.player import Enemy, PlayerCharacter
from hololive_coliseum.projectile import FreezingProjectile, Projectile
from hololive_coliseum.status_effects import StatusEffectManager
from hololive_coliseum.team_manager import TeamManager


def test_multi_entity_combat_tick():
    pygame.init()
    pygame.display.set_mode((1, 1))
    status_manager = StatusEffectManager()
    team_manager = TeamManager()
    combat = CombatManager(status_manager=status_manager, team_manager=team_manager)

    player = PlayerCharacter(0, 0)
    ally = AllyFighter(200, 0)
    enemy_a = Enemy(160, 0)
    enemy_b = Enemy(230, 0)
    enemy_b.health = 3
    enemy_b.stats.apply_modifier("defense", -enemy_b.stats.get("defense"))

    team_manager.set_team(player, 0)
    team_manager.set_team(ally, 0)
    team_manager.set_team(enemy_a, 1)
    team_manager.set_team(enemy_b, 1)

    projectiles = pygame.sprite.Group()
    melees = pygame.sprite.Group()
    damage_numbers = pygame.sprite.Group()
    enemies = pygame.sprite.Group(enemy_a, enemy_b)
    allies = pygame.sprite.Group(ally)

    ally_proj = FreezingProjectile(
        enemy_b.rect.centerx,
        enemy_b.rect.centery,
        pygame.math.Vector2(1, 0),
    )
    ally_proj.owner = ally
    ally_proj.attack = 8
    projectiles.add(ally_proj)

    enemy_proj = Projectile(
        ally.rect.centerx,
        ally.rect.centery,
        pygame.math.Vector2(1, 0),
        from_enemy=True,
        owner=enemy_a,
    )
    enemy_proj.attack = 6
    projectiles.add(enemy_proj)

    enemy_melee = MeleeAttack(
        player.rect.centerx,
        player.rect.centery,
        1,
        owner=enemy_a,
        from_enemy=True,
    )
    enemy_melee.attack = 10
    melees.add(enemy_melee)

    start_player = player.health
    start_ally = ally.health

    now = pygame.time.get_ticks()
    killed = combat.handle_collisions(
        player,
        enemies,
        projectiles,
        melees,
        now,
        allies=allies,
        damage_numbers=damage_numbers,
    )

    assert player.health < start_player
    assert ally.health < start_ally
    assert any(entry["name"] == "Freeze" for entry in status_manager.active_effects(enemy_b))
    assert enemy_b in killed
    assert len(damage_numbers) >= 2
    pygame.quit()
