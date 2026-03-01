"""Tests for auto dev pipeline helpers."""

from __future__ import annotations

from hololive_coliseum.auto_dev_pipeline_helpers import (
    copy_dict,
    intensity_entries,
    normalise_trade_skills,
    projection_focus,
    roadmap_focus,
)


def test_normalise_trade_skills_removes_empty_values() -> None:
    assert normalise_trade_skills(["Smithing", "", "Alchemy"]) == [
        "Smithing",
        "Alchemy",
    ]
    assert normalise_trade_skills(None) == []


def test_roadmap_focus_prefers_top_focus() -> None:
    assert roadmap_focus({"top_focus": "Lava"}) == {"focus": "lava"}
    assert roadmap_focus({"hazard": "Ice"}) == {"focus": "ice"}
    assert roadmap_focus({}) == {}


def test_projection_focus_uses_spawn_danger_and_synergy() -> None:
    monsters = [
        {"hazard": "lava", "weakness": "frost", "spawn_synergy": "reinforcement"},
        {"hazard": "ice", "spawn_synergy": "overwhelming"},
    ]
    projection = projection_focus(
        monsters,
        spawn_plan={"danger": 1.2},
        trade_skills=["Smithing", "Alchemy"],
    )
    focus = projection["focus"]
    assert focus[0]["spawn_multiplier"] == 1.32
    assert focus[1]["spawn_multiplier"] == 1.5


def test_intensity_entries_and_copy_dict_normalise_inputs() -> None:
    entries = list(
        intensity_entries(
            [{"value": 0.25, "source": "probe"}, (0.5, "manual")]
        )
    )
    assert entries == [(0.25, "probe"), (0.5, "manual")]
    source = {"x": 1, "y": 2}
    copied = copy_dict(source)
    assert copied == {"x": 1, "y": 2}
    assert copied is not source
