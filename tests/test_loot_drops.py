"""Verify that defeated enemies drop loot items."""

import pytest
import pathlib
import sys


def test_enemy_drops_loot(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    import hololive_coliseum.save_manager as save_manager
    monkeypatch.setattr(save_manager, "SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game
    from hololive_coliseum.player import Enemy
    from hololive_coliseum.projectile import Projectile

    game = Game()
    game.loot_manager.add_table("Enemy", ["potion"])
    game.selected_character = "Gawr Gura"
    game._setup_level()
    enemy = Enemy(200, game.ground_y - 60)
    enemy.health = 8
    game.enemies.add(enemy)
    game.all_sprites.add(enemy)
    proj = Projectile(enemy.rect.centerx, enemy.rect.centery, pygame.math.Vector2(1, 0))
    game.projectiles.add(proj)
    game._handle_collisions()
    assert game.player.inventory.count("potion") == 1
    pygame.quit()
