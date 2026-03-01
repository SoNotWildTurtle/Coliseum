"""Coordinate lightweight AI-to-player interaction callouts."""

from __future__ import annotations

from typing import Iterable


class AIInteractionManager:
    """Emit taunts and support callouts based on arena state."""

    def __init__(
        self,
        *,
        taunt_cooldown_ms: int = 4500,
        support_cooldown_ms: int = 5000,
        focus_cooldown_ms: int = 7000,
    ) -> None:
        self.taunt_cooldown_ms = taunt_cooldown_ms
        self.support_cooldown_ms = support_cooldown_ms
        self.focus_cooldown_ms = focus_cooldown_ms
        self._last_emit: dict[str, int] = {}

    def update(
        self,
        player,
        enemies: Iterable[object],
        allies: Iterable[object],
        now: int,
    ) -> list[dict[str, object]]:
        """Return callouts triggered by the current arena state."""
        messages: list[dict[str, object]] = []
        enemies = list(enemies)
        allies = list(allies)
        if player is None:
            return messages
        player_ratio = _health_ratio(player)
        if enemies:
            if player_ratio <= 0.35:
                enemy = _closest_entity(enemies, player)
                if enemy and self._ready("enemy_taunt", now, self.taunt_cooldown_ms):
                    messages.append(
                        _message(
                            "Finish them!",
                            enemy,
                            color=(255, 120, 120),
                            source_label="enemy",
                        )
                    )
            if player_ratio >= 0.8 and self._ready(
                "enemy_push", now, self.taunt_cooldown_ms
            ):
                enemy = _closest_entity(enemies, player)
                if enemy:
                    messages.append(
                        _message(
                            "Hold the line!",
                            enemy,
                            color=(255, 160, 120),
                            source_label="enemy",
                        )
                    )
            if len(enemies) >= 3 and self._ready(
                "enemy_focus", now, self.focus_cooldown_ms
            ):
                enemy = _closest_entity(enemies, player)
                if enemy:
                    messages.append(
                        _message(
                            "Focus fire!",
                            enemy,
                            color=(255, 150, 120),
                            source_label="enemy",
                        )
                    )
            boss = _boss_entity(enemies)
            if boss and self._ready("enemy_boss", now, self.taunt_cooldown_ms + 1500):
                messages.append(
                    _message(
                        "Boss engaged!",
                        boss,
                        color=(255, 140, 90),
                        source_label="enemy",
                    )
                )
        if allies:
            if player_ratio <= 0.45 and self._ready(
                "ally_support", now, self.support_cooldown_ms
            ):
                ally = _closest_entity(allies, player)
                if ally:
                    messages.append(
                        _message(
                            "On your back!",
                            ally,
                            color=(170, 220, 255),
                            source_label="ally",
                        )
                    )
            if len(enemies) >= 3 and self._ready(
                "ally_focus", now, self.focus_cooldown_ms
            ):
                ally = _closest_entity(allies, player)
                if ally:
                    messages.append(
                        _message(
                            "Focus fire!",
                            ally,
                            color=(200, 255, 200),
                            source_label="ally",
                        )
                    )
            low_ally = _lowest_health(allies)
            if low_ally and self._ready(
                "ally_cover", now, self.support_cooldown_ms + 1500
            ):
                if _health_ratio(low_ally) <= 0.35:
                    messages.append(
                        _message(
                            "Cover me!",
                            low_ally,
                            color=(160, 200, 255),
                            source_label="ally",
                        )
                    )
            stamina_ratio = _resource_ratio(player, "stamina", "max_stamina")
            if stamina_ratio <= 0.25 and self._ready(
                "ally_stamina", now, self.support_cooldown_ms
            ):
                ally = _closest_entity(allies, player)
                if ally:
                    messages.append(
                        _message(
                            "Catch your breath!",
                            ally,
                            color=(190, 220, 255),
                            source_label="ally",
                        )
                    )
            mana_ratio = _resource_ratio(player, "mana", "max_mana")
            if mana_ratio <= 0.25 and self._ready(
                "ally_mana", now, self.support_cooldown_ms
            ):
                ally = _closest_entity(allies, player)
                if ally:
                    messages.append(
                        _message(
                            "Mana low!",
                            ally,
                            color=(180, 200, 255),
                            source_label="ally",
                        )
                    )
        return messages

    def _ready(self, key: str, now: int, cooldown: int) -> bool:
        last = self._last_emit.get(key, -cooldown)
        if now - last < cooldown:
            return False
        self._last_emit[key] = now
        return True


def _health_ratio(entity: object) -> float:
    max_health = float(getattr(entity, "max_health", 0) or 0)
    health = float(getattr(entity, "health", 0) or 0)
    if max_health <= 0:
        return 0.0
    return max(0.0, min(1.0, health / max_health))


def _resource_ratio(entity: object, value_attr: str, max_attr: str) -> float:
    maximum = float(getattr(entity, max_attr, 0) or 0)
    value = float(getattr(entity, value_attr, 0) or 0)
    if maximum <= 0:
        return 1.0
    return max(0.0, min(1.0, value / maximum))


def _closest_entity(entities: list[object], target: object) -> object | None:
    if not entities:
        return None
    target_rect = getattr(target, "rect", None)
    if target_rect is None:
        return entities[0]
    return min(
        entities,
        key=lambda entity: abs(
            getattr(getattr(entity, "rect", None), "centerx", 0)
            - target_rect.centerx
        ),
    )


def _lowest_health(entities: list[object]) -> object | None:
    if not entities:
        return None
    return min(entities, key=_health_ratio)


def _boss_entity(entities: list[object]) -> object | None:
    for entity in entities:
        if getattr(entity, "max_health", 0) >= 160:
            return entity
    return None


def _message(
    text: str,
    source: object,
    *,
    color: tuple[int, int, int],
    source_label: str,
) -> dict[str, object]:
    rect = getattr(source, "rect", None)
    if rect is None:
        pos = (0, 0)
    else:
        pos = (rect.centerx, rect.top - 24)
    return {"text": text, "pos": pos, "color": color, "source": source_label}
