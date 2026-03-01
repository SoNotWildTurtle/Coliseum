"""Tests for auto dev codebase analyzer."""

from __future__ import annotations

from hololive_coliseum.auto_dev_codebase_analyzer import AutoDevCodebaseAnalyzer


def test_analyzer_highlights_missing_tests_and_complexity() -> None:
    analyzer = AutoDevCodebaseAnalyzer(complexity_threshold=10.0, warning_threshold=15.0)
    analysis = analyzer.evaluate(
        modules=[
            {
                "name": "auto_dev_monster_manager",
                "complexity": 9.5,
                "has_tests": True,
                "docstring": True,
                "recent_incidents": [],
            },
            {
                "name": "auto_dev_network_manager",
                "complexity": 20.0,
                "has_tests": False,
                "docstring": True,
                "recent_incidents": [True],
            },
            {
                "name": "auto_dev_pipeline",
                "complexity": 13.0,
                "has_tests": False,
                "docstring": True,
                "recent_incidents": [],
            },
        ],
        tests=[{"name": "test_auto_dev_pipeline"}],
    )

    assert analysis["status"] == "analysed"
    assert analysis["coverage_ratio"] < 1.0
    assert analysis["average_complexity"] > 10.0
    assert any("Tests missing" in signal for signal in analysis["weakness_signals"])
    assert any("complexity" in signal.lower() for signal in analysis["weakness_signals"])
    assert analysis["mitigation_plan"]
    profile = analysis["debt_profile"]
    assert profile["missing_tests"]
    assert profile["high_complexity"]
    assert analysis["stability_outlook"] in {"refactor-critical", "stabilise", "improve", "steady"}
    assert 0.0 <= analysis["debt_risk_score"] <= 1.0
    assert analysis["module_scorecards"]
    network_card = next(
        card for card in analysis["module_scorecards"] if card["name"] == "auto_dev_network_manager"
    )
    assert network_card["risk_level"] in {"elevated", "high", "critical"}
    assert network_card["recommended_actions"]
    modernization = analysis["modernization_targets"]
    assert modernization
    assert modernization[0]["modernization_steps"]
    assert analysis["functionality_gap_index"] >= 0.0
    assert analysis["functionality_gaps"]
    assert 0.0 <= analysis["mechanics_alignment_score"] <= 100.0
    assert analysis["design_fragility_index"] >= 0.0
    assert analysis["design_focus_modules"]
    assert analysis["design_recommendations"]
    assert analysis["systems_fragility_index"] >= 0.0
    assert analysis["systems_focus_modules"]
    assert analysis["systems_recommendations"]
    assert 0.0 <= analysis["systems_alignment_index"] <= 100.0
    assert analysis["creation_gap_index"] >= 0.0
    assert analysis["creation_focus_modules"]
    assert analysis["creation_recommendations"]
    assert 0.0 <= analysis["creation_alignment_score"] <= 100.0
    assert analysis["blueprint_gap_index"] >= 0.0
    assert 0.0 <= analysis["blueprint_alignment_score"] <= 100.0
    assert analysis["blueprint_focus_modules"]
    assert analysis["blueprint_recommendations"]
    assert analysis["iteration_gap_index"] >= 0.0
    assert 0.0 <= analysis["iteration_alignment_score"] <= 100.0
    assert analysis["iteration_focus_modules"]
    assert analysis["iteration_recommendations"]
    assert analysis["convergence_gap_index"] >= 0.0
    assert 0.0 <= analysis["convergence_alignment_score"] <= 100.0
    assert analysis["convergence_focus_modules"]
    assert analysis["implementation_gap_index"] >= 0.0
    assert 0.0 <= analysis["implementation_alignment_score"] <= 100.0
    assert analysis["implementation_focus_modules"]
    assert analysis["implementation_recommendations"]
