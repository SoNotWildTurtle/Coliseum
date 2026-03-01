"""NPC creation and behavior orchestration."""

import pygame

class NPCManager:
    """Maintain groups of enemies and allied NPCs."""

    def __init__(self) -> None:
        self.enemies = pygame.sprite.Group()
        self.allies = pygame.sprite.Group()

    def clear(self) -> None:
        self.enemies.empty()
        self.allies.empty()

    def add_enemy(self, sprite: pygame.sprite.Sprite) -> None:
        self.enemies.add(sprite)

    def add_ally(self, sprite: pygame.sprite.Sprite) -> None:
        self.allies.add(sprite)
