"""Track AI combat experiences and propose smarter next actions."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentExperience:
    """Stateful combat record for a single AI agent."""

    actions: dict[str, int] = field(default_factory=dict)
    last_health: float = 0.0
    last_damage_time: int = 0
    time_alive_ms: int = 0
    engagements: int = 0
    next_action: str = "patrol"
    bias: dict[str, float] = field(default_factory=dict)
    last_action: str = ""
    repeat_count: int = 0


class AIExperienceManager:
    """Monitor AI agent outcomes and compute next-action hints."""

    def __init__(self, experience_level: int = 1) -> None:
        self.experience_level = max(1, int(experience_level))
        self._agents: dict[int, AgentExperience] = {}

    def set_experience_level(self, level: int) -> None:
        """Update the global experience multiplier."""
        self.experience_level = max(1, int(level))

    def record_action(self, agent: Any, action: str) -> None:
        """Record an action performed by an agent."""
        state = self._state(agent)
        state.actions[action] = state.actions.get(action, 0) + 1
        if state.last_action == action:
            state.repeat_count += 1
        else:
            state.last_action = action
            state.repeat_count = 0

    def snapshot(self, agents: list[Any]) -> list[dict[str, Any]]:
        """Return a serializable snapshot for the supplied agents."""
        snapshot: list[dict[str, Any]] = []
        for agent in agents:
            state = self._state(agent)
            snapshot.append(
                {
                    "agent_id": id(agent),
                    "label": getattr(agent, "name", agent.__class__.__name__),
                    "next_action": state.next_action,
                    "bias": dict(state.bias),
                    "actions": dict(state.actions),
                    "time_alive_ms": state.time_alive_ms,
                    "engagements": state.engagements,
                    "health": float(getattr(agent, "health", 0.0)),
                    "max_health": float(getattr(agent, "max_health", 0.0)),
                }
            )
        return snapshot

    def update_context(
        self,
        player: Any,
        enemies: list[Any],
        now: int,
        hazards: list[Any] | None = None,
        threat_level: float | None = None,
    ) -> None:
        """Update agent contexts and compute next-action bias."""
        hazards = hazards or []
        for enemy in enemies:
            state = self._state(enemy)
            state.time_alive_ms += 1
            if state.last_health <= 0.0:
                state.last_health = float(getattr(enemy, "health", 0.0))
            health = float(getattr(enemy, "health", 0.0))
            if health < state.last_health:
                state.last_damage_time = now
            state.last_health = health
            state.engagements += 1
            state.next_action, state.bias = self._plan_next_action(
                enemy, player, now, hazards, state, threat_level
            )
            setattr(enemy, "ai_next_action", state.next_action)
            setattr(enemy, "ai_bias", state.bias)

    def _state(self, agent: Any) -> AgentExperience:
        key = id(agent)
        if key not in self._agents:
            self._agents[key] = AgentExperience()
        return self._agents[key]

    def _plan_next_action(
        self,
        enemy: Any,
        player: Any,
        now: int,
        hazards: list[Any],
        state: AgentExperience,
        threat_level: float | None,
    ) -> tuple[str, dict[str, float]]:
        dist_x = abs(player.rect.centerx - enemy.rect.centerx)
        dist_y = abs(player.rect.centery - enemy.rect.centery)
        health_ratio = 0.0
        if getattr(enemy, "max_health", 0):
            health_ratio = enemy.health / enemy.max_health
        recent_damage = now - state.last_damage_time
        experience_boost = min(0.35, state.engagements / 4200)
        hazard_near = any(
            getattr(hz, "avoid", False)
            and hz.rect.colliderect(enemy.rect.inflate(40, 20))
            for hz in hazards
        )
        threat = max(0.0, float(threat_level or 0.0))
        threat_ratio = min(1.0, threat / 10.0)
        threat_bias = {
            "speed": 0.05 * threat_ratio,
            "react_ms": -35 * threat_ratio,
            "melee_prob": 0.1 * threat_ratio,
            "shoot_prob": 0.08 * threat_ratio,
            "dodge_prob": 0.05 * threat_ratio,
            "special_prob": 0.08 * threat_ratio,
            "dash_prob": 0.06 * threat_ratio,
        }

        def _apply_threat_bias(bias: dict[str, float]) -> dict[str, float]:
            for key, delta in threat_bias.items():
                if delta == 0:
                    continue
                if key == "react_ms":
                    base = float(bias.get(key, 0))
                    bias[key] = max(50.0, base + delta)
                else:
                    bias[key] = float(bias.get(key, 0)) + delta
            return bias

        bias: dict[str, float] = {}
        if hazard_near:
            return "avoid", _apply_threat_bias(
                {
                    "jump_prob": 0.55,
                    "dodge_prob": 0.6 + experience_boost,
                    "block_prob": 0.4 + experience_boost * 0.6,
                    "speed": 1.1 + experience_boost * 0.2,
                }
            )
        if health_ratio < 0.35 or recent_damage < 1200:
            bias["retreat_threshold"] = 0.45
            bias["dodge_prob"] = 0.6 + 0.04 * self.experience_level
            bias["dodge_prob"] += experience_boost * 0.4
            bias["block_prob"] = 0.4 + 0.02 * self.experience_level
            bias["block_prob"] += experience_boost * 0.3
            bias["speed"] = 1.0 + 0.04 * self.experience_level
            bias["speed"] += experience_boost * 0.3
            return "retreat", _apply_threat_bias(bias)
        if state.repeat_count >= 4 and dist_x < 120:
            bias["melee_prob"] = 1.0
            bias["shoot_prob"] = 0.4
            bias["react_ms"] = max(60, 200 - self.experience_level * 10)        
            return "melee", _apply_threat_bias(bias)
        if dist_x < 60 and dist_y < 70:
            bias["melee_prob"] = 1.0
            bias["shoot_prob"] = 0.3
            bias["react_ms"] = max(
                60,
                220 - self.experience_level * 12 - int(experience_boost * 80),  
            )
            return "melee", _apply_threat_bias(bias)
        if dist_x < 240:
            bias["shoot_prob"] = 1.0
            bias["melee_prob"] = 0.35
            bias["lead_frames"] = min(
                18,
                4 + self.experience_level + int(experience_boost * 10),
            )
            return "shoot", _apply_threat_bias(bias)
        bias["jump_prob"] = 0.25 + 0.02 * self.experience_level
        bias["jump_prob"] += experience_boost * 0.2
        bias["speed"] = 0.9 + 0.04 * self.experience_level
        bias["speed"] += experience_boost * 0.2
        return "approach", _apply_threat_bias(bias)
