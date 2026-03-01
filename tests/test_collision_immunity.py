"""Ensure invincibility prevents all damage types."""

import pytest


def test_invincible_blocks_all_damage(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.player import Enemy
    from hololive_coliseum.projectile import Projectile
    from hololive_coliseum.melee_attack import MeleeAttack

    game = Game()
    game.ai_players = 0
    game._setup_level()
    player = game.player
    player.invincible = True

    enemy = Enemy(player.rect.centerx, player.rect.centery)
    game.enemies.add(enemy)

    proj = Projectile(
        player.rect.centerx,
        player.rect.centery,
        pygame.math.Vector2(),
        from_enemy=True,
    )
    game.projectiles.add(proj)

    melee = MeleeAttack(
        player.rect.centerx,
        player.rect.centery,
        1,
        from_enemy=True,
    )
    game.melee_attacks.add(melee)

    now = pygame.time.get_ticks()
    game.combat_manager.handle_collisions(
        player, game.enemies, game.projectiles, game.melee_attacks, now
    )

    assert player.health == player.max_health


def test_dodge_avoids_damage(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.player import Enemy
    from hololive_coliseum.projectile import Projectile
    from hololive_coliseum.melee_attack import MeleeAttack

    game = Game()
    game.ai_players = 0
    game._setup_level()
    player = game.player

    now = pygame.time.get_ticks()
    player.dodge(now, 1)

    enemy = Enemy(player.rect.centerx, player.rect.centery)
    game.enemies.add(enemy)

    proj = Projectile(
        player.rect.centerx,
        player.rect.centery,
        pygame.math.Vector2(),
        from_enemy=True,
    )
    game.projectiles.add(proj)

    melee = MeleeAttack(
        player.rect.centerx,
        player.rect.centery,
        1,
        from_enemy=True,
    )
    game.melee_attacks.add(melee)

    game.combat_manager.handle_collisions(
        player, game.enemies, game.projectiles, game.melee_attacks, now
    )

    assert player.health == player.max_health

