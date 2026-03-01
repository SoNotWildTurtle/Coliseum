"""Tests for experience gain."""

import pytest


def test_enemy_kill_awards_experience(tmp_path, monkeypatch):
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
    enemy = Enemy(200, game.ground_y - 60)
    enemy.health = 8
    game.enemies.add(enemy)
    game.all_sprites.add(enemy)
    proj = Projectile(
        enemy.rect.centerx, enemy.rect.centery, pygame.math.Vector2(1, 0)
    )
    game.projectiles.add(proj)
    start = game.player.experience_manager.xp
    game._handle_collisions()
    assert game.player.experience_manager.xp >= start + 10
    pygame.quit()


def test_xp_multiplier_scales_rewards(tmp_path, monkeypatch):
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
    game.xp_multiplier = 2.0
    enemy = Enemy(200, game.ground_y - 60)
    enemy.health = 8
    game.enemies.add(enemy)
    game.all_sprites.add(enemy)
    proj = Projectile(
        enemy.rect.centerx, enemy.rect.centery, pygame.math.Vector2(1, 0)
    )
    game.projectiles.add(proj)
    start = game.player.experience_manager.xp
    game._handle_collisions()
    assert game.player.experience_manager.xp >= start + 20
    pygame.quit()
