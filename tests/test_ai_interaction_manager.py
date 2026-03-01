"""Tests for AI interaction manager callouts."""

from __future__ import annotations

import pygame

from hololive_coliseum.ai_interaction_manager import AIInteractionManager
from hololive_coliseum.player import PlayerCharacter, Enemy


def test_ai_interaction_manager_emits_callouts():
    pygame.init()
    pygame.display.set_mode((1, 1))
    manager = AIInteractionManager(
        taunt_cooldown_ms=0,
        support_cooldown_ms=0,
        focus_cooldown_ms=0,
    )
    player = PlayerCharacter(0, 0)
    player.max_health = 100
    player.health = 20
    enemy = Enemy(10, 0)
    ally = PlayerCharacter(-10, 0)
    callouts = manager.update(
        player,
        enemies=[enemy],
        allies=[ally],
        now=pygame.time.get_ticks(),
    )
    assert any(callout["source"] == "enemy" for callout in callouts)
    assert any(callout["source"] == "ally" for callout in callouts)
    pygame.quit()


def test_ai_interaction_manager_resource_callouts():
    pygame.init()
    pygame.display.set_mode((1, 1))
    manager = AIInteractionManager(
        taunt_cooldown_ms=0,
        support_cooldown_ms=0,
        focus_cooldown_ms=0,
    )
    player = PlayerCharacter(0, 0)
    player.max_health = 100
    player.health = 80
    player.max_mana = 100
    player.mana = 10
    player.max_stamina = 100
    player.stamina = 10
    ally = PlayerCharacter(-10, 0)
    callouts = manager.update(
        player,
        enemies=[],
        allies=[ally],
        now=pygame.time.get_ticks(),
    )
    texts = {callout["text"] for callout in callouts}
    assert "Mana low!" in texts
    assert "Catch your breath!" in texts
    pygame.quit()
