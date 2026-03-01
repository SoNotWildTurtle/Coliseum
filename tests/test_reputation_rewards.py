"""Tests for reputation rewards."""

import pytest


def test_enemy_kill_grants_reputation(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game
    from hololive_coliseum.player import Enemy
    from hololive_coliseum.projectile import Projectile

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    enemy = Enemy(
        200,
        game.ground_y - 60,
        faction="Crimson Legion",
        reputation_reward=7,
    )
    enemy.health = 1
    game.enemies.add(enemy)
    game.all_sprites.add(enemy)
    proj = Projectile(
        enemy.rect.centerx,
        enemy.rect.centery,
        pygame.math.Vector2(1, 0),
    )
    game.projectiles.add(proj)
    start = game.reputation_manager.get("Crimson Legion")
    game._handle_collisions()
    assert game.reputation_manager.get("Crimson Legion") == start + 7
    pygame.quit()
