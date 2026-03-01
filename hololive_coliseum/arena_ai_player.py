"""Background arena AI players used for fun balancing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


def _clamp(value: float, *, lower: float = 0.0, upper: float = 1.0) -> float:
    """Return *value* constrained to the inclusive ``[lower, upper]`` range."""

    return max(lower, min(upper, value))


@dataclass(frozen=True)
class ArenaAIPlayer:
    """Simple agent that scores arena states for fun balancing.

    ``aggression`` favours faster paced matches, ``creativity`` rewards varied
    encounters, and ``teamwork`` values supportive play. ``preferred_archetypes``
    highlights the playstyles this agent represents, while ``adaptability``
    controls how much future projections drift from an initial evaluation. All
    numeric attributes are expected on ``[0.0, 1.0]`` and are automatically
    clamped at runtime.
    """

    name: str
    aggression: float = 0.5
    creativity: float = 0.5
    teamwork: float = 0.5
    preferred_archetypes: tuple[str, ...] = ()
    adaptability: float = 0.5

    def evaluate_arena(self, snapshot: Mapping[str, float]) -> float:
        """Return a fun rating for ``snapshot`` on ``[0.0, 1.0]``."""

        aggression = _clamp(self.aggression)
        creativity = _clamp(self.creativity)
        teamwork = _clamp(self.teamwork)
        pace = _clamp(snapshot.get("pace", 0.6))
        variety = _clamp(snapshot.get("variety", 0.5))
        fairness = _clamp(snapshot.get("fairness", 0.65))
        support = _clamp(snapshot.get("support", 0.5))
        risk = _clamp(snapshot.get("risk", 0.5))
        excitement = (
            pace * (0.4 + aggression * 0.25)
            + variety * (0.25 + creativity * 0.25)
            + fairness * (0.2 + (1.0 - abs(aggression - 0.5)) * 0.15)
            + support * (0.15 + teamwork * 0.2)
        )
        penalty = abs(risk - 0.6) * (0.15 + teamwork * 0.1)
        return _clamp(excitement - penalty)

    def playtest_arena(
        self, snapshot: Mapping[str, float], *, rounds: int = 3
    ) -> Mapping[str, object]:
        """Return structured feedback for iterative background playtests.

        The function simulates ``rounds`` background matches by starting with the
        base :meth:`evaluate_arena` rating and gently projecting how the fun
        level might drift when volatility and pacing change. The resulting
        dictionary contains the base rating, an averaged projection, the
        volatility penalty observed across the simulated rounds, and the agent's
        preferred archetypes to aid downstream balancing heuristics.
        """

        rounds = max(1, rounds)
        rating = self.evaluate_arena(snapshot)
        aggression = _clamp(self.aggression)
        adaptability = _clamp(self.adaptability)
        pace = _clamp(snapshot.get("pace", 0.6))
        volatility = _clamp(snapshot.get("volatility", snapshot.get("risk", 0.5)))
        projections: list[float] = []
        for index in range(rounds):
            influence = (index + 1) / rounds
            projection = _clamp(
                rating
                + (pace - 0.6) * (0.12 + aggression * 0.06) * influence
                - (volatility - 0.45) * (0.1 + (1.0 - adaptability) * 0.05) * influence
            )
            projections.append(projection)
        average_projection = sum(projections) / len(projections)
        consensus = sum(abs(proj - rating) for proj in projections) / len(projections)
        return {
            "player": self.name,
            "rating": rating,
            "projected_rating": round(average_projection, 3),
            "volatility_penalty": round(consensus, 3),
            "preferred_archetypes": self.preferred_archetypes[:3],
        }
