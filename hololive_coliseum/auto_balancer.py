"""Automatically balance class statistics."""

from __future__ import annotations

from typing import Mapping


def _clamp(value: float, *, lower: float = 0.0, upper: float = 1.0) -> float:
    """Return *value* limited to the inclusive ``[lower, upper]`` range."""

    return max(lower, min(upper, value))


class AutoBalancer:
    """Adjust class stat dictionaries toward the average."""

    def __init__(self, *, fun_target: float = 0.6, feedback_strength: float = 4.0) -> None:
        self.fun_target = _clamp(fun_target)
        self.feedback_strength = max(0.0, feedback_strength)

    def balance(
        self,
        classes: Mapping[str, Mapping[str, float]],
        *,
        fun_level: float | None = None,
        ai_feedback: Mapping[str, float] | None = None,
        base_fun_level: float | None = None,
        fun_report: object | None = None,
        fun_forecast: object | None = None,
        fun_plan: object | None = None,
        fun_season: object | None = None,
    ) -> dict[str, dict[str, float]]:
        """Return new stats closer to the average values.

        When ``ai_feedback`` is provided the values should be within ``[0.0, 1.0]``.
        The balancer compares those ratings with ``fun_level`` (or ``fun_target`` if
        not supplied) to nudge stats toward combinations that the background AI
        players found more engaging. ``base_fun_level`` represents the long-term
        arena fun baseline. When supplied, the balancer first shifts all class
        stats so the current fun level trends toward that baseline before
        applying the per-class AI adjustments. ``fun_forecast`` can be either an
        :class:`~hololive_coliseum.arena_manager.ArenaFunForecast` instance or a
        mapping. When provided, the balancer incorporates the forecast's expected
        fun level, risk band, and recommended focus when adjusting stats. ``fun_plan``
        can be an :class:`~hololive_coliseum.arena_manager.ArenaFunTuningPlan`
        instance or mapping. When supplied, the balancer honours the plan's target
        fun level, baseline shift, volatility hints, and class directives before
        applying the normal AI feedback adjustments. ``fun_season`` accepts an
        :class:`~hololive_coliseum.arena_manager.ArenaFunSeasonSummary` (or mapping)
        so the balancer can follow the fun momentum, participation rate, and
        archetype focus surfaced by AI-only background matches.
        """

        if not classes:
            return {}

        keys = ("attack", "defense", "health")
        averages = {
            key: sum(stats.get(key, 0.0) for stats in classes.values()) / len(classes)
            for key in keys
        }
        balanced: dict[str, dict[str, float]] = {}
        for name, stats in classes.items():
            balanced[name] = {
                key: stats.get(key, 0.0) - (stats.get(key, 0.0) - averages[key]) / 2.0
                for key in keys
            }

        target_fun = _clamp(fun_level if fun_level is not None else self.fun_target)
        momentum = None
        volatility = None
        expected_fun = None
        risk_band = None
        ai_alignment = 1.0
        feedback_scale = 1.0
        focus = None
        volatility_band = None
        plan_target_fun = None
        plan_focus = None
        plan_alignment = 1.0
        plan_baseline_shift = 0.0
        plan_volatility = None
        plan_momentum = None
        plan_directives: tuple | list | None = None
        season_fun = None
        season_momentum = None
        season_participation = None
        season_archetypes: tuple[str, ...] | list[str] | None = None
        if fun_forecast is not None:
            if hasattr(fun_forecast, "expected_fun"):
                expected_fun = getattr(fun_forecast, "expected_fun")
                risk_band = getattr(fun_forecast, "risk_band", None)
                focus = getattr(fun_forecast, "recommended_focus", None)
                ai_alignment = getattr(fun_forecast, "ai_alignment", ai_alignment)
                volatility_band = getattr(fun_forecast, "volatility_band", None)
            elif isinstance(fun_forecast, Mapping):
                expected_fun = fun_forecast.get("expected_fun")
                risk_band = fun_forecast.get("risk_band")
                focus = fun_forecast.get("recommended_focus")
                ai_alignment = fun_forecast.get("ai_alignment", ai_alignment)
                volatility_band = fun_forecast.get("volatility_band")
            if expected_fun is not None:
                expected_fun = _clamp(expected_fun)
            if risk_band is not None:
                risk_band = _clamp(risk_band, upper=1.0)
            ai_alignment = _clamp(ai_alignment)
            if focus:
                focus = str(focus).lower()
            if volatility_band is not None:
                volatility_band = _clamp(volatility_band, upper=1.0)
                feedback_scale *= max(0.4, 1.0 - volatility_band * 0.5)

        if fun_report is not None:
            momentum = getattr(fun_report, "fun_momentum", None)
            if momentum is None and isinstance(fun_report, Mapping):
                momentum = fun_report.get("fun_momentum")
            volatility = getattr(fun_report, "volatility", None)
            if volatility is None and isinstance(fun_report, Mapping):
                volatility = fun_report.get("volatility")
        if fun_plan is not None:
            if hasattr(fun_plan, "target_fun"):
                plan_target_fun = getattr(fun_plan, "target_fun")
                plan_focus = getattr(fun_plan, "focus", None)
                plan_alignment = getattr(fun_plan, "ai_alignment", plan_alignment)
                plan_baseline_shift = getattr(
                    fun_plan, "baseline_shift", plan_baseline_shift
                )
                plan_volatility = getattr(fun_plan, "volatility", None)
                plan_momentum = getattr(fun_plan, "fun_momentum", None)
                plan_directives = getattr(fun_plan, "directives", None)
            elif isinstance(fun_plan, Mapping):
                plan_target_fun = fun_plan.get("target_fun")
                plan_focus = fun_plan.get("focus", None)
                plan_alignment = fun_plan.get("ai_alignment", plan_alignment)
                plan_baseline_shift = fun_plan.get(
                    "baseline_shift", plan_baseline_shift
                )
                plan_volatility = fun_plan.get("volatility", None)
                plan_momentum = fun_plan.get("fun_momentum", None)
                plan_directives = fun_plan.get("directives", None)
        if fun_season is not None:
            if hasattr(fun_season, "season_fun"):
                season_fun = getattr(fun_season, "season_fun", None)
                season_momentum = getattr(fun_season, "fun_momentum", None)
                season_participation = getattr(
                    fun_season, "ai_participation", season_participation
                )
                season_archetypes = getattr(
                    fun_season, "highlighted_archetypes", season_archetypes
                )
            elif isinstance(fun_season, Mapping):
                season_fun = fun_season.get("season_fun")
                season_momentum = fun_season.get("fun_momentum")
                season_participation = fun_season.get("ai_participation")
                season_archetypes = fun_season.get("highlighted_archetypes")
        if expected_fun is not None:
            target_fun = _clamp(target_fun * 0.6 + expected_fun * 0.4)
        if plan_target_fun is not None:
            plan_target_fun = _clamp(plan_target_fun)
            target_fun = _clamp(target_fun * 0.5 + plan_target_fun * 0.5)
        if season_fun is not None:
            season_fun = _clamp(float(season_fun))
            target_fun = _clamp(target_fun * 0.6 + season_fun * 0.4)
        baseline = _clamp(base_fun_level) if base_fun_level is not None else target_fun
        baseline_delta = target_fun - baseline
        if baseline_delta:
            baseline_factor = baseline_delta * (self.feedback_strength / 2.0)
            for stats in balanced.values():
                stats["attack"] = max(0.0, stats["attack"] + baseline_factor * 0.25)
                stats["defense"] = max(0.0, stats["defense"] + baseline_factor * 0.6)
                stats["health"] = max(0.0, stats["health"] + baseline_factor * 2.5)
        if plan_baseline_shift:
            shift = _clamp(plan_baseline_shift, lower=-1.0, upper=1.0)
            shift_factor = shift * (self.feedback_strength / 3.2)
            for stats in balanced.values():
                stats["attack"] = max(0.0, stats["attack"] + shift_factor * 0.2)
                stats["defense"] = max(0.0, stats["defense"] + shift_factor * 0.35)
                stats["health"] = max(0.0, stats["health"] + shift_factor * 1.1)

        if momentum:
            momentum_factor = momentum * (self.feedback_strength / 3.0)
            for stats in balanced.values():
                stats["attack"] = max(0.0, stats["attack"] + momentum_factor * 0.4)
                stats["defense"] = max(0.0, stats["defense"] + momentum_factor * 0.3)
                stats["health"] = max(0.0, stats["health"] + momentum_factor * 1.2)
        if season_momentum is not None:
            season_momentum_value = float(season_momentum)
            momentum_factor = season_momentum_value * (self.feedback_strength / 3.5)
            for stats in balanced.values():
                stats["attack"] = max(0.0, stats["attack"] + momentum_factor * 0.25)
                stats["defense"] = max(0.0, stats["defense"] + momentum_factor * 0.35)
                stats["health"] = max(0.0, stats["health"] + momentum_factor * 1.0)
            if plan_momentum is not None:
                plan_momentum = float(plan_momentum) + season_momentum_value * 0.5
            else:
                plan_momentum = season_momentum_value

        if volatility is not None:
            stability_delta = 0.18 - _clamp(volatility, upper=1.0)
            if stability_delta:
                stability_factor = stability_delta * (self.feedback_strength / 4.0)
                for stats in balanced.values():
                    stats["defense"] = max(0.0, stats["defense"] + stability_factor * 0.5)
                    stats["health"] = max(0.0, stats["health"] + stability_factor * 1.8)
        if plan_volatility is not None:
            volatility_value = _clamp(float(plan_volatility), upper=1.0)
            stability_delta = 0.2 - volatility_value
            if stability_delta:
                stability_factor = stability_delta * (self.feedback_strength / 4.5)
                for stats in balanced.values():
                    stats["defense"] = max(0.0, stats["defense"] + stability_factor * 0.45)
                    stats["health"] = max(0.0, stats["health"] + stability_factor * 1.1)

        if risk_band:
            risk_factor = risk_band * (self.feedback_strength / 4.5)
            for stats in balanced.values():
                stats["defense"] = max(0.0, stats["defense"] + risk_factor * 0.2)
                stats["health"] = max(0.0, stats["health"] + risk_factor * 0.7)
        if season_participation is not None:
            feedback_scale *= 0.85 + _clamp(float(season_participation)) * 0.5
        season_archetype_set = {
            str(value).lower() for value in (season_archetypes or ()) if value
        }
        if season_archetype_set:
            support_focus = {"support", "healer", "guardian"}
            assault_focus = {"assault", "brawler", "aggressor"}
            control_focus = {"control", "tactician", "controller"}
            for stats in balanced.values():
                if season_archetype_set & support_focus:
                    stats["defense"] = max(0.0, stats["defense"] * 1.02)
                    stats["health"] = max(0.0, stats["health"] * 1.025)
                if season_archetype_set & assault_focus:
                    stats["attack"] = max(0.0, stats["attack"] * 1.03)
                if season_archetype_set & control_focus:
                    stats["defense"] = max(0.0, stats["defense"] * 1.01)
                    stats["attack"] = max(0.0, stats["attack"] * 1.008)

        if focus == "stabilize":
            focus_factor = ai_alignment * (self.feedback_strength / 3.0)
            for stats in balanced.values():
                stats["defense"] = max(0.0, stats["defense"] + focus_factor * 0.3)
                stats["health"] = max(0.0, stats["health"] + focus_factor * 1.0)
        elif focus == "experiment":
            focus_factor = ai_alignment * (self.feedback_strength / 3.5)
            for stats in balanced.values():
                stats["attack"] = max(0.0, stats["attack"] + focus_factor * 0.5)
        elif focus == "elevate":
            focus_factor = ai_alignment * (self.feedback_strength / 3.2)
            for stats in balanced.values():
                stats["attack"] = max(0.0, stats["attack"] + focus_factor * 0.25)
                stats["health"] = max(0.0, stats["health"] + focus_factor * 0.8)
        elif focus == "align_ai":
            feedback_scale += (1.0 - ai_alignment) * 0.8

        if plan_directives:
            directives_iter = plan_directives
            if not isinstance(plan_directives, (tuple, list)):
                directives_iter = tuple(plan_directives)
            plan_alignment = _clamp(float(plan_alignment), upper=1.0)
            plan_focus = (plan_focus or "").lower()
            for directive in directives_iter:
                if hasattr(directive, "class_name"):
                    name = getattr(directive, "class_name")
                    action = getattr(directive, "action", "")
                    weight = getattr(directive, "weight", 0.0)
                    stat_bias = getattr(directive, "stat_bias", ())
                elif isinstance(directive, Mapping):
                    name = directive.get("class_name") or directive.get("target")
                    action = directive.get("action", "")
                    weight = directive.get("weight", 0.0)
                    stat_bias = directive.get("stat_bias", ())
                else:
                    continue
                if name not in balanced:
                    continue
                weight = max(0.0, float(weight))
                if not weight:
                    continue
                if isinstance(stat_bias, Mapping):
                    items = stat_bias.items()
                else:
                    items = stat_bias
                bias = [(str(stat), float(value)) for stat, value in items]
                total_bias = sum(abs(value) for _, value in bias)
                if not total_bias:
                    continue
                bias = [(stat, value / total_bias) for stat, value in bias]
                action = str(action or "").lower()
                direction = 0.0
                if action == "boost":
                    direction = 1.0
                elif action == "trim":
                    direction = -1.0
                elif action == "stabilize":
                    if plan_momentum is not None:
                        direction = -1.0 if float(plan_momentum) > 0.0 else 1.0
                    else:
                        direction = 0.5 if plan_alignment >= 0.5 else 0.0
                adjustment = (
                    direction
                    * weight
                    * self.feedback_strength
                    * max(0.3, plan_alignment)
                )
                if plan_focus == "experiment" and action == "boost":
                    adjustment *= 1.15
                elif plan_focus == "stabilize" and action != "trim":
                    adjustment *= 0.85
                if not adjustment:
                    continue
                for stat, ratio in bias:
                    if stat not in balanced[name]:
                        continue
                    balanced[name][stat] = max(
                        0.0, balanced[name][stat] + adjustment * ratio
                    )

        if ai_feedback:
            for name, stats in balanced.items():
                rating = ai_feedback.get(name)
                if rating is None:
                    continue
                rating = _clamp(rating)
                delta = (rating - target_fun) * self.feedback_strength * feedback_scale
                if not delta:
                    continue
                stats["attack"] = max(0.0, stats["attack"] + delta)
                stats["defense"] = max(0.0, stats["defense"] + delta * 0.6)
                stats["health"] = max(0.0, stats["health"] + delta * 4.0)

        return balanced
