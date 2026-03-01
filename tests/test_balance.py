"""Combat balance tests for attack and defense scaling."""

import pytest

pygame = pytest.importorskip("pygame")

from hololive_coliseum.player import PlayerCharacter, Enemy
from hololive_coliseum.combat_manager import CombatManager


def test_stats_affect_damage():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    enemy = Enemy(0, 0)
    player.stats.base["attack"] = 20
    enemy.stats.base["defense"] = 5
    proj = player.shoot(pygame.time.get_ticks(), target=enemy.rect.center)
    proj.rect.center = enemy.rect.center
    cm = CombatManager()
    cm.handle_collisions(
        player,
        pygame.sprite.Group(enemy),
        pygame.sprite.Group(proj),
        pygame.sprite.Group(),
        pygame.time.get_ticks(),
    )
    assert enemy.health == enemy.max_health - 15
    pygame.quit()
