"""Tests for arena fun balancing."""

from hololive_coliseum import (
    ArenaAIPlayer,
    ArenaFunDirective,
    ArenaFunForecast,
    ArenaFunReport,
    ArenaFunSnapshot,
    ArenaFunTuningPlan,
    ArenaFunSeasonSummary,
    ArenaManager,
    AutoBalancer,
)


def test_arena_ai_player_rating_stays_in_range() -> None:
    agent = ArenaAIPlayer(
        name="Aggressive",
        aggression=1.2,
        creativity=-0.2,
        teamwork=0.8,
    )
    rating = agent.evaluate_arena(
        {
            "pace": 0.9,
            "variety": 0.7,
            "fairness": 0.6,
            "support": 0.5,
            "risk": 0.3,
        }
    )
    assert 0.0 <= rating <= 1.0


def test_arena_ai_player_playtest_projection() -> None:
    agent = ArenaAIPlayer(
        name="Strategist",
        aggression=0.25,
        creativity=0.85,
        teamwork=0.9,
        preferred_archetypes=("Support", "Control"),
        adaptability=0.8,
    )
    feedback = agent.playtest_arena(
        {
            "pace": 0.65,
            "variety": 0.75,
            "fairness": 0.7,
            "support": 0.85,
            "risk": 0.55,
            "volatility": 0.45,
        },
        rounds=4,
    )
    assert feedback["player"] == "Strategist"
    assert 0.0 <= feedback["projected_rating"] <= 1.0
    assert feedback["preferred_archetypes"] == ("Support", "Control")


def test_arena_manager_updates_fun_with_feedback() -> None:
    manager = ArenaManager(baseline_fun=0.4)
    updated = manager.record_match_feedback(
        "Player",
        0.9,
        intensity=0.8,
        duration=6.0,
    )
    assert updated > 0.4
    assert manager.fun_history[-1] == updated
    assert manager.scores["Player"] == 1


def test_auto_balancer_uses_background_ai_feedback() -> None:
    classes = {
        "A": {"attack": 10.0, "defense": 5.0, "health": 90.0},
        "B": {"attack": 20.0, "defense": 12.0, "health": 110.0},
    }
    agents = (
        ArenaAIPlayer("A", aggression=0.9, creativity=0.7, teamwork=0.4),
        ArenaAIPlayer("B", aggression=0.2, creativity=0.3, teamwork=0.8),
    )
    manager = ArenaManager(
        ai_players=agents,
        baseline_fun=0.6,
        fun_smoothing=0.3,
    )
    manager.record_match_feedback(
        "Pilot",
        0.85,
        intensity=0.9,
        duration=8.0,
    )
    manager.simulate_background_balancing(
        {
            "pace": 0.9,
            "variety": 0.55,
            "fairness": 0.65,
            "support": 0.35,
            "risk": 0.85,
        }
    )
    ai_feedback = manager.get_ai_feedback()
    balancer = AutoBalancer(fun_target=0.5, feedback_strength=2.0)
    baseline = balancer.balance(classes)
    tuned = balancer.balance(
        classes,
        fun_level=manager.fun_level,
        ai_feedback=ai_feedback,
    )
    assert tuned["A"]["attack"] > baseline["A"]["attack"]
    assert tuned["B"]["attack"] < baseline["B"]["attack"]


def test_arena_manager_calibrates_baseline_with_ai() -> None:
    agent = ArenaAIPlayer("Strategist", aggression=0.3, creativity=0.7, teamwork=0.8)
    manager = ArenaManager(
        baseline_fun=0.42,
        fun_smoothing=0.4,
        ai_players=(agent,),
        baseline_adaptation=0.25,
    )
    manager.record_match_feedback("Pilot", 0.78, intensity=0.9, duration=10.0)
    manager.simulate_background_balancing(
        {
            "pace": 0.85,
            "variety": 0.8,
            "fairness": 0.7,
            "support": 0.65,
            "risk": 0.45,
        }
    )
    before_calibration = manager.base_fun_level
    manager.calibrate_fun_baseline()
    snapshot = manager.capture_fun_snapshot()
    assert isinstance(snapshot, ArenaFunSnapshot)
    assert snapshot.baseline_fun >= before_calibration
    assert snapshot.fun_momentum == round(snapshot.fun_level - snapshot.baseline_fun, 3)
    assert snapshot.ai_projection == manager.ai_fun_projection


def test_arena_manager_run_ai_playtests_generates_report() -> None:
    agents = (
        ArenaAIPlayer(
            "Blitzer",
            aggression=0.9,
            creativity=0.5,
            teamwork=0.4,
            preferred_archetypes=("Assault",),
            adaptability=0.3,
        ),
        ArenaAIPlayer(
            "Coordinator",
            aggression=0.2,
            creativity=0.8,
            teamwork=0.95,
            preferred_archetypes=("Support", "Hybrid"),
            adaptability=0.7,
        ),
    )
    manager = ArenaManager(
        baseline_fun=0.48,
        fun_smoothing=0.35,
        ai_players=agents,
        baseline_adaptation=0.22,
    )
    manager.record_match_feedback("Pilot", 0.82, intensity=0.85, duration=9.0)
    report = manager.run_ai_playtests(
        (
            {
                "pace": 0.75,
                "variety": 0.7,
                "fairness": 0.62,
                "support": 0.6,
                "risk": 0.55,
                "volatility": 0.5,
            },
            {
                "pace": 0.68,
                "variety": 0.8,
                "fairness": 0.7,
                "support": 0.72,
                "risk": 0.48,
                "volatility": 0.42,
            },
        ),
        rounds=3,
    )
    assert isinstance(report, ArenaFunReport)
    assert report.rounds_tested == 2
    assert 0.0 <= report.ai_consensus <= 1.0
    assert report.volatility >= 0.0
    assert manager.base_fun_level == report.baseline_fun


def test_arena_manager_simulate_ai_matches_returns_summary() -> None:
    agents = (
        ArenaAIPlayer("Aggro", aggression=0.9, creativity=0.6, teamwork=0.4),
        ArenaAIPlayer("Support", aggression=0.3, creativity=0.7, teamwork=0.9),
    )
    manager = ArenaManager(
        baseline_fun=0.5,
        fun_smoothing=0.35,
        ai_players=agents,
        baseline_adaptation=0.18,
    )
    snapshots = (
        {
            "pace": 0.72,
            "variety": 0.68,
            "fairness": 0.66,
            "support": 0.62,
            "risk": 0.52,
            "volatility": 0.44,
        },
        {
            "pace": 0.65,
            "variety": 0.74,
            "fairness": 0.7,
            "support": 0.78,
            "risk": 0.48,
            "volatility": 0.39,
        },
    )
    summary = manager.simulate_ai_matches(snapshots, rounds=4)
    assert isinstance(summary, ArenaFunSeasonSummary)
    assert summary.rounds_played >= 2
    wins = manager.get_ai_season_wins()
    assert set(wins).issubset({"Aggro", "Support"})
    assert summary.ai_participation > 0.0


def test_auto_balancer_considers_fun_baseline() -> None:
    classes = {
        "A": {"attack": 14.0, "defense": 9.0, "health": 100.0},
        "B": {"attack": 16.0, "defense": 11.0, "health": 105.0},
    }
    balancer = AutoBalancer(fun_target=0.6, feedback_strength=3.5)
    low_baseline = balancer.balance(classes, fun_level=0.55, base_fun_level=0.4)
    high_baseline = balancer.balance(classes, fun_level=0.55, base_fun_level=0.7)
    assert low_baseline["A"]["health"] > high_baseline["A"]["health"]


def test_auto_balancer_uses_fun_season_summary() -> None:
    classes = {
        "Warrior": {"attack": 18.0, "defense": 11.0, "health": 120.0},
        "Cleric": {"attack": 12.0, "defense": 14.0, "health": 115.0},
    }
    balancer = AutoBalancer(fun_target=0.58, feedback_strength=3.0)
    baseline = balancer.balance(classes)
    season = ArenaFunSeasonSummary(
        season_fun=0.62,
        baseline_fun=0.55,
        ai_projection=0.6,
        fun_momentum=0.07,
        ai_participation=0.9,
        highlighted_archetypes=("Support", "Control"),
        win_leaders=(("Aggro", 2),),
        rounds_played=4,
    )
    tuned = balancer.balance(classes, fun_season=season)
    assert tuned["Warrior"]["defense"] >= baseline["Warrior"]["defense"]
    assert tuned["Cleric"]["health"] >= baseline["Cleric"]["health"]


def test_arena_manager_generates_fun_forecast() -> None:
    agents = (
        ArenaAIPlayer(
            "Aggro",
            aggression=0.85,
            creativity=0.55,
            teamwork=0.35,
            preferred_archetypes=("Assault", "Skirmisher"),
            adaptability=0.4,
        ),
        ArenaAIPlayer(
            "Strategist",
            aggression=0.3,
            creativity=0.8,
            teamwork=0.9,
            preferred_archetypes=("Support", "Control"),
            adaptability=0.75,
        ),
    )
    manager = ArenaManager(
        baseline_fun=0.5,
        fun_smoothing=0.35,
        ai_players=agents,
        baseline_adaptation=0.2,
    )
    manager.record_match_feedback("Pilot", 0.76, intensity=0.8, duration=9.5)
    manager.run_ai_playtests(
        (
            {
                "pace": 0.78,
                "variety": 0.72,
                "fairness": 0.64,
                "support": 0.58,
                "risk": 0.52,
                "volatility": 0.48,
            },
            {
                "pace": 0.7,
                "variety": 0.82,
                "fairness": 0.7,
                "support": 0.76,
                "risk": 0.46,
                "volatility": 0.4,
            },
        ),
        rounds=3,
    )
    forecast = manager.generate_fun_forecast()
    assert isinstance(forecast, ArenaFunForecast)
    assert 0.0 <= forecast.expected_fun <= 1.0
    assert forecast.recommended_focus in {"elevate", "stabilize", "align_ai", "experiment"}
    archetypes = manager.get_ai_archetype_focus()
    assert forecast.archetype_focus == archetypes
    if archetypes:
        assert archetypes[0] in {"Assault", "Skirmisher", "Support", "Control"}


def test_auto_balancer_uses_fun_forecast_focus() -> None:
    classes = {
        "A": {"attack": 18.0, "defense": 9.0, "health": 98.0},
        "B": {"attack": 16.0, "defense": 11.0, "health": 110.0},
    }
    balancer = AutoBalancer(fun_target=0.58, feedback_strength=3.2)
    baseline = balancer.balance(classes, fun_level=0.55)
    forecast = ArenaFunForecast(
        expected_fun=0.57,
        risk_band=0.65,
        volatility_band=0.22,
        recommended_focus="stabilize",
        ai_alignment=0.72,
        archetype_focus=("Support",),
    )
    tuned = balancer.balance(
        classes,
        fun_level=0.55,
        fun_forecast=forecast,
    )
    assert tuned["A"]["defense"] > baseline["A"]["defense"]
    assert tuned["A"]["health"] > baseline["A"]["health"]


def test_auto_balancer_fun_forecast_scales_ai_feedback() -> None:
    classes = {
        "A": {"attack": 12.0, "defense": 8.0, "health": 95.0},
        "B": {"attack": 14.0, "defense": 10.0, "health": 105.0},
    }
    ai_feedback = {"A": 0.82, "B": 0.42}
    balancer = AutoBalancer(fun_target=0.6, feedback_strength=3.8)
    base = balancer.balance(classes, fun_level=0.58, ai_feedback=ai_feedback)
    forecast = ArenaFunForecast(
        expected_fun=0.62,
        risk_band=0.18,
        volatility_band=0.3,
        recommended_focus="align_ai",
        ai_alignment=0.4,
        archetype_focus=("Assault",),
    )
    directed = balancer.balance(
        classes,
        fun_level=0.58,
        ai_feedback=ai_feedback,
        fun_forecast=forecast,
    )
    assert directed["A"]["attack"] > base["A"]["attack"]
    assert directed["B"]["attack"] < base["B"]["attack"]


def test_auto_balancer_uses_fun_report_trends() -> None:
    classes = {
        "Assault": {"attack": 18.0, "defense": 8.0, "health": 95.0},
        "Support": {"attack": 11.0, "defense": 12.0, "health": 110.0},
    }
    agents = (
        ArenaAIPlayer(
            "Aggro",
            aggression=0.85,
            creativity=0.45,
            teamwork=0.35,
            preferred_archetypes=("Assault",),
        ),
        ArenaAIPlayer(
            "Analyst",
            aggression=0.35,
            creativity=0.75,
            teamwork=0.85,
            preferred_archetypes=("Support", "Hybrid"),
            adaptability=0.9,
        ),
    )
    manager = ArenaManager(
        baseline_fun=0.4,
        fun_smoothing=0.4,
        ai_players=agents,
        baseline_adaptation=0.3,
    )
    manager.record_match_feedback("Pilot", 0.88, intensity=0.9, duration=10.0)
    report = manager.run_ai_playtests(
        (
            {
                "pace": 0.82,
                "variety": 0.68,
                "fairness": 0.64,
                "support": 0.58,
                "risk": 0.6,
                "volatility": 0.52,
            },
        ),
        rounds=2,
    )
    ai_feedback = manager.get_ai_feedback()
    balancer = AutoBalancer(fun_target=0.58, feedback_strength=2.8)
    baseline = balancer.balance(
        classes,
        fun_level=manager.fun_level,
        ai_feedback=ai_feedback,
        base_fun_level=manager.base_fun_level,
    )
    tuned = balancer.balance(
        classes,
        fun_level=manager.fun_level,
        ai_feedback=ai_feedback,
        base_fun_level=manager.base_fun_level,
        fun_report=report,
    )
    assert tuned["Support"]["defense"] != baseline["Support"]["defense"]
    if report.fun_momentum > 0:
        assert tuned["Support"]["health"] >= baseline["Support"]["health"]


def test_arena_manager_generates_fun_tuning_plan() -> None:
    classes = {
        "Blitzer": {"attack": 20.0, "defense": 9.0, "health": 94.0},
        "Anchor": {"attack": 14.0, "defense": 13.0, "health": 112.0},
    }
    agents = (
        ArenaAIPlayer(
            "Blitzer",
            aggression=0.9,
            creativity=0.6,
            teamwork=0.35,
            preferred_archetypes=("Aggressor",),
        ),
        ArenaAIPlayer(
            "Anchor",
            aggression=0.25,
            creativity=0.55,
            teamwork=0.92,
            preferred_archetypes=("Support", "Control"),
            adaptability=0.8,
        ),
    )
    manager = ArenaManager(
        baseline_fun=0.52,
        fun_smoothing=0.32,
        ai_players=agents,
        baseline_adaptation=0.18,
    )
    manager.record_match_feedback("Pilot", 0.78, intensity=0.85, duration=9.0)
    manager.simulate_background_balancing(
        {
            "pace": 0.86,
            "variety": 0.68,
            "fairness": 0.64,
            "support": 0.52,
            "risk": 0.62,
        }
    )
    manager.run_ai_playtests(
        (
            {
                "pace": 0.82,
                "variety": 0.74,
                "fairness": 0.66,
                "support": 0.55,
                "risk": 0.57,
                "volatility": 0.46,
            },
        ),
        rounds=3,
    )
    plan = manager.generate_fun_tuning_plan(classes)
    assert isinstance(plan, ArenaFunTuningPlan)
    assert 0.0 <= plan.target_fun <= 1.0
    assert plan.focus in {"elevate", "stabilize", "align_ai", "experiment", "balance"}
    assert plan.directives
    directive_targets = {directive.class_name for directive in plan.directives}
    assert {"Blitzer", "Anchor"}.issuperset(directive_targets)
    assert plan.archetype_focus == manager.get_ai_archetype_focus()


def test_auto_balancer_honours_fun_plan_directives() -> None:
    classes = {
        "Blitzer": {"attack": 18.0, "defense": 9.0, "health": 96.0},
        "Anchor": {"attack": 13.0, "defense": 12.0, "health": 110.0},
    }
    agents = (
        ArenaAIPlayer(
            "Blitzer",
            aggression=0.88,
            creativity=0.6,
            teamwork=0.4,
            preferred_archetypes=("Aggressor",),
        ),
        ArenaAIPlayer(
            "Anchor",
            aggression=0.2,
            creativity=0.5,
            teamwork=0.9,
            preferred_archetypes=("Support",),
            adaptability=0.85,
        ),
    )
    manager = ArenaManager(
        baseline_fun=0.5,
        fun_smoothing=0.3,
        ai_players=agents,
        baseline_adaptation=0.2,
    )
    manager.record_match_feedback("Pilot", 0.82, intensity=0.9, duration=10.0)
    manager.simulate_background_balancing(
        {
            "pace": 0.88,
            "variety": 0.66,
            "fairness": 0.58,
            "support": 0.48,
            "risk": 0.63,
        }
    )
    fun_report = manager.generate_fun_report()
    fun_forecast = manager.generate_fun_forecast()
    plan = manager.generate_fun_tuning_plan(
        classes,
        fun_report=fun_report,
        fun_forecast=fun_forecast,
    )
    ai_feedback = manager.get_ai_feedback()
    balancer = AutoBalancer(fun_target=0.58, feedback_strength=3.2)
    base = balancer.balance(
        classes,
        fun_level=manager.fun_level,
        ai_feedback=ai_feedback,
        base_fun_level=manager.base_fun_level,
    )
    tuned = balancer.balance(
        classes,
        fun_level=manager.fun_level,
        ai_feedback=ai_feedback,
        base_fun_level=manager.base_fun_level,
        fun_plan=plan,
        fun_report=fun_report,
        fun_forecast=fun_forecast,
    )
    boosted = [
        directive.class_name
        for directive in plan.directives
        if isinstance(directive, ArenaFunDirective) and directive.action == "boost"
    ]
    trimmed = [
        directive.class_name
        for directive in plan.directives
        if isinstance(directive, ArenaFunDirective) and directive.action == "trim"
    ]
    if boosted:
        target = boosted[0]
        assert tuned[target]["attack"] >= base[target]["attack"]
    if trimmed:
        target = trimmed[0]
        assert tuned[target]["attack"] <= base[target]["attack"]
