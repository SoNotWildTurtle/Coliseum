"""Helper utilities shared by the auto-dev pipeline orchestration module."""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence


def normalise_trade_skills(skills: Sequence[str] | None) -> list[str]:
    """Return trade skills without empty values."""
    return [skill for skill in (skills or ()) if skill]


def roadmap_focus(focus: Mapping[str, Any] | None) -> dict[str, Any]:
    """Build a compact roadmap focus payload."""
    if not focus:
        return {}
    hazard = focus.get("top_focus") or focus.get("hazard")
    if not hazard:
        return {}
    return {"focus": str(hazard).lower()}


def projection_focus(
    monsters: Sequence[dict[str, Any]],
    spawn_plan: Mapping[str, Any] | None,
    trade_skills: Sequence[str] | None,
) -> dict[str, Any]:
    """Build a projection bundle that mob AI and bosses can consume."""
    danger = float((spawn_plan or {}).get("danger", 1.0))
    skills = normalise_trade_skills(trade_skills) or ["Generalist"]
    focus_entries = []
    for index, monster in enumerate(monsters, start=1):
        hazard = str(monster.get("hazard", "general"))
        weakness = str(monster.get("weakness", skills[index % len(skills)]))
        spawn_synergy = str(monster.get("spawn_synergy", "skirmish"))
        multiplier = 1.0
        if spawn_synergy == "reinforcement":
            multiplier = 1.1
        elif spawn_synergy == "overwhelming":
            multiplier = 1.25
        multiplier *= max(0.8, danger)
        focus_entries.append(
            {
                "hazard": hazard,
                "recommended_powerups": (
                    f"{weakness.lower()} shield",
                    f"{hazard} resistance",
                ),
                "spawn_multiplier": round(multiplier, 2),
            }
        )
    return {"focus": tuple(focus_entries)}


def intensity_entries(
    intensities: Sequence[dict[str, Any]] | Sequence[tuple[float, str]] | None,
) -> Iterable[tuple[float, str]]:
    """Yield normalized `(value, source)` pairs from mixed intensity inputs."""
    for entry in intensities or ():
        if isinstance(entry, dict):
            value = float(entry.get("value") or entry.get("intensity") or 0.0)
            source = str(entry.get("source") or "intensity")
            yield value, source
        else:
            value, source = entry  # type: ignore[misc]
            yield float(value), str(source)


def copy_dict(data: Mapping[str, Any]) -> dict[str, Any]:
    """Return a shallow dict copy from mapping inputs."""
    return {key: value for key, value in data.items()}
