"""Arena orchestration utilities."""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Mapping

from .arena_ai_player import ArenaAIPlayer


def _clamp(value: float, *, lower: float = 0.0, upper: float = 1.0) -> float:
    """Return *value* limited to the inclusive ``[lower, upper]`` range."""

    return max(lower, min(upper, value))


@dataclass(frozen=True)
class ArenaFunSnapshot:
    """Immutable snapshot of the arena fun telemetry."""

    fun_level: float
    baseline_fun: float
    ai_projection: float
    fun_momentum: float

    def as_dict(self) -> dict[str, float]:
        """Return the snapshot as a plain dictionary."""

        return {
            "fun_level": self.fun_level,
            "baseline_fun": self.baseline_fun,
            "ai_projection": self.ai_projection,
            "fun_momentum": self.fun_momentum,
        }


@dataclass(frozen=True)
class ArenaFunReport:
    """Detailed fun telemetry emitted after background AI playtests."""

    fun_level: float
    baseline_fun: float
    ai_projection: float
    fun_momentum: float
    volatility: float
    ai_consensus: float
    rounds_tested: int = 0

    def as_dict(self) -> dict[str, float]:
        """Return the report as a serialisable dictionary."""

        return {
            "fun_level": self.fun_level,
            "baseline_fun": self.baseline_fun,
            "ai_projection": self.ai_projection,
            "fun_momentum": self.fun_momentum,
            "volatility": self.volatility,
            "ai_consensus": self.ai_consensus,
            "rounds_tested": float(self.rounds_tested),
        }


@dataclass(frozen=True)
class ArenaFunForecast:
    """Forward-looking fun outlook based on background AI telemetry."""

    expected_fun: float
    risk_band: float
    volatility_band: float
    recommended_focus: str
    ai_alignment: float
    archetype_focus: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        """Return the forecast as a serialisable dictionary."""

        return {
            "expected_fun": self.expected_fun,
            "risk_band": self.risk_band,
            "volatility_band": self.volatility_band,
            "recommended_focus": self.recommended_focus,
            "ai_alignment": self.ai_alignment,
            "archetype_focus": self.archetype_focus,
        }


@dataclass(frozen=True)
class ArenaFunDirective:
    """Recommendation describing how to tweak a specific class for fun gains."""

    class_name: str
    action: str
    weight: float
    stat_bias: tuple[tuple[str, float], ...]
    rationale: str = ""

    def as_dict(self) -> dict[str, object]:
        """Return the directive as a serialisable dictionary."""

        return {
            "class_name": self.class_name,
            "action": self.action,
            "weight": self.weight,
            "stat_bias": {key: value for key, value in self.stat_bias},
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class ArenaFunTuningPlan:
    """Holistic fun plan derived from background AI telemetry."""

    target_fun: float
    baseline_fun: float
    fun_momentum: float
    ai_alignment: float
    focus: str
    volatility: float
    baseline_shift: float
    directives: tuple[ArenaFunDirective, ...] = ()
    archetype_focus: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        """Return the tuning plan as a serialisable dictionary."""

        return {
            "target_fun": self.target_fun,
            "baseline_fun": self.baseline_fun,
            "fun_momentum": self.fun_momentum,
            "ai_alignment": self.ai_alignment,
            "focus": self.focus,
            "volatility": self.volatility,
            "baseline_shift": self.baseline_shift,
            "directives": tuple(directive.as_dict() for directive in self.directives),
            "archetype_focus": self.archetype_focus,
        }


@dataclass(frozen=True)
class ArenaFunSeasonSummary:
    """Summary describing how background AI matches influenced fun."""

    season_fun: float
    baseline_fun: float
    ai_projection: float
    fun_momentum: float
    ai_participation: float
    highlighted_archetypes: tuple[str, ...]
    win_leaders: tuple[tuple[str, int], ...]
    rounds_played: int

    def as_dict(self) -> dict[str, object]:
        """Return the summary as a serialisable dictionary."""

        return {
            "season_fun": self.season_fun,
            "baseline_fun": self.baseline_fun,
            "ai_projection": self.ai_projection,
            "fun_momentum": self.fun_momentum,
            "ai_participation": self.ai_participation,
            "highlighted_archetypes": self.highlighted_archetypes,
            "win_leaders": self.win_leaders,
            "rounds_played": float(self.rounds_played),
        }


class ArenaManager:
    """Handle PvP arena rankings, fun tracking, and AI-driven balancing."""

    def __init__(
        self,
        *,
        baseline_fun: float = 0.55,
        fun_smoothing: float = 0.35,
        ai_players: Iterable[ArenaAIPlayer] | None = None,
        baseline_adaptation: float = 0.12,
    ) -> None:
        self.scores: dict[str, int] = {}
        self.fun_level = round(_clamp(baseline_fun), 3)
        self.fun_smoothing = _clamp(fun_smoothing)
        self.fun_history: deque[float] = deque((self.fun_level,), maxlen=50)
        self.ai_players = tuple(ai_players or ())
        self._ai_feedback: dict[str, float] = {}
        self.base_fun_level = self.fun_level
        self.baseline_adaptation = _clamp(baseline_adaptation)
        self.ai_fun_projection = self.fun_level
        self.fun_momentum = 0.0
        self._ai_consensus_history: deque[float] = deque(maxlen=50)
        self._archetype_history: deque[str] = deque(maxlen=60)
        self._ai_season_wins: Counter[str] = Counter()
        self._ai_season_rounds = 0

    def record_win(self, player: str) -> None:
        """Increment ``player``'s win count."""

        self.scores[player] = self.scores.get(player, 0) + 1

    def record_match_feedback(
        self,
        player: str,
        fun_rating: float,
        *,
        intensity: float = 0.5,
        duration: float = 1.0,
    ) -> float:
        """Blend player feedback into the arena fun level.

        ``fun_rating`` is expected to be on ``[0.0, 1.0]`` and represents how fun the
        match felt. ``intensity`` denotes the pace of the match, while ``duration``
        is measured in minutes and feeds into the weighting so short matches do not
        over-correct the global fun score. The resulting fun level is returned.
        """

        self.record_win(player)
        rating = _clamp(fun_rating)
        pace = _clamp(intensity)
        length_factor = _clamp(duration / 12.0)
        weight = _clamp(0.25 + pace * 0.4 + length_factor * 0.35)
        self.fun_level = round(
            (1.0 - weight) * self.fun_level + weight * rating,
            3,
        )
        self.fun_history.append(self.fun_level)
        self._update_baseline(weight * self.baseline_adaptation)
        return self.fun_level

    def simulate_background_balancing(
        self, arena_snapshot: Mapping[str, float]
    ) -> float:
        """Use AI players to evaluate ``arena_snapshot`` and update fun metrics."""

        if not self.ai_players:
            self.fun_history.append(self.fun_level)
            self._ai_feedback = {}
            self.ai_fun_projection = self.fun_level
            self._refresh_momentum()
            return self.fun_level

        evaluations = []
        feedback: dict[str, float] = {}
        for ai_player in self.ai_players:
            rating = ai_player.evaluate_arena(arena_snapshot)
            feedback[ai_player.name] = rating
            evaluations.append(rating)

        self._ai_feedback = feedback
        average_rating = sum(evaluations) / len(evaluations)
        self.ai_fun_projection = round(_clamp(average_rating), 3)
        smoothing = self.fun_smoothing
        blended = (1.0 - smoothing) * self.fun_level + smoothing * average_rating
        self.fun_level = round(_clamp(blended), 3)
        self.fun_history.append(self.fun_level)
        self._record_consensus(abs(self.ai_fun_projection - self.fun_level))
        self._update_baseline(
            0.5 * self.fun_smoothing * self.baseline_adaptation,
            target=self.ai_fun_projection,
        )
        return self.fun_level

    def get_ai_feedback(self) -> dict[str, float]:
        """Return the most recent background AI fun feedback mapping."""

        return dict(self._ai_feedback)

    def calibrate_fun_baseline(self) -> float:
        """Slowly align the baseline fun level with recent trends."""

        if not self.fun_history:
            return self.base_fun_level

        trend = sum(self.fun_history) / len(self.fun_history)
        target = (trend * 0.6) + (self.ai_fun_projection * 0.4)
        self._update_baseline(self.baseline_adaptation * 0.8, target=target)
        return self.base_fun_level

    def capture_fun_snapshot(self) -> ArenaFunSnapshot:
        """Return a structured snapshot of the current fun telemetry."""

        self._refresh_momentum()
        return ArenaFunSnapshot(
            fun_level=self.fun_level,
            baseline_fun=self.base_fun_level,
            ai_projection=self.ai_fun_projection,
            fun_momentum=self.fun_momentum,
        )

    def get_fun_momentum(self) -> float:
        """Return the current difference between fun and the baseline."""

        self._refresh_momentum()
        return self.fun_momentum

    def run_ai_playtests(
        self, snapshots: Iterable[Mapping[str, float]], *, rounds: int = 3
    ) -> ArenaFunReport:
        """Iterate through ``snapshots`` to refine the arena fun outlook.

        Each snapshot represents an alternative arena state. The manager
        simulates balancing for every snapshot, requests richer playtest feedback
        from all registered AI players, and blends the aggregated projections
        into the long-term fun baseline. The resulting :class:`ArenaFunReport`
        captures the updated telemetry.
        """

        snapshots = tuple(snapshots)
        if not snapshots:
            return self.generate_fun_report()

        aggregated_projections: list[float] = []
        for snapshot in snapshots:
            self.simulate_background_balancing(snapshot)
            if not self.ai_players:
                continue
            session_feedback = [
                ai.playtest_arena(snapshot, rounds=rounds) for ai in self.ai_players
            ]
            average_projection = sum(
                feedback["projected_rating"] for feedback in session_feedback
            ) / len(session_feedback)
            consensus = sum(
                feedback["volatility_penalty"] for feedback in session_feedback
            ) / len(session_feedback)
            for feedback in session_feedback:
                self._record_archetypes(feedback.get("preferred_archetypes", ()))
            aggregated_projections.append(average_projection)
            self._record_consensus(consensus)

        if aggregated_projections:
            projection_target = sum(aggregated_projections) / len(aggregated_projections)
            self._update_baseline(
                self.baseline_adaptation * 0.5,
                target=_clamp(projection_target),
            )

        return self.generate_fun_report(rounds_tested=len(snapshots))

    def generate_fun_report(self, rounds_tested: int = 0) -> ArenaFunReport:
        """Return the current fun telemetry wrapped in a report."""

        self._refresh_momentum()
        volatility = self._calculate_volatility()
        if self._ai_consensus_history:
            ai_consensus = sum(self._ai_consensus_history) / len(self._ai_consensus_history)
        else:
            ai_consensus = 0.0
        return ArenaFunReport(
            fun_level=self.fun_level,
            baseline_fun=self.base_fun_level,
            ai_projection=self.ai_fun_projection,
            fun_momentum=self.fun_momentum,
            volatility=round(volatility, 3),
            ai_consensus=round(ai_consensus, 3),
            rounds_tested=rounds_tested,
        )

    def generate_fun_forecast(self) -> ArenaFunForecast:
        """Return a forecast describing likely fun trajectory and focus areas."""

        self._refresh_momentum()
        volatility = _clamp(self._calculate_volatility(), upper=1.0)
        if self._ai_consensus_history:
            consensus = sum(self._ai_consensus_history) / len(self._ai_consensus_history)
        else:
            consensus = 0.0
        ai_alignment = round(_clamp(1.0 - consensus), 3)
        expected_fun = round(
            _clamp(
                self.fun_level * 0.45
                + self.ai_fun_projection * 0.35
                + self.base_fun_level * 0.2
            ),
            3,
        )
        risk_band = round(
            _clamp(abs(self.fun_momentum) * 0.5 + volatility * 0.5, upper=1.0),
            3,
        )
        if expected_fun + 0.03 < self.base_fun_level:
            focus = "elevate"
        elif volatility > 0.24:
            focus = "stabilize"
        elif ai_alignment < 0.55:
            focus = "align_ai"
        else:
            focus = "experiment"
        archetype_focus = self.get_ai_archetype_focus()
        return ArenaFunForecast(
            expected_fun=expected_fun,
            risk_band=risk_band,
            volatility_band=round(volatility, 3),
            recommended_focus=focus,
            ai_alignment=ai_alignment,
            archetype_focus=archetype_focus,
        )

    def generate_fun_tuning_plan(
        self,
        classes: Mapping[str, Mapping[str, float]] | None = None,
        *,
        fun_report: ArenaFunReport | Mapping[str, float] | None = None,
        fun_forecast: ArenaFunForecast | Mapping[str, float] | None = None,
    ) -> ArenaFunTuningPlan:
        """Return a fun tuning plan blending AI directives with arena telemetry."""

        self._refresh_momentum()
        report = fun_report if fun_report is not None else self.generate_fun_report()
        forecast = (
            fun_forecast
            if fun_forecast is not None
            else self.generate_fun_forecast()
        )
        volatility = float(self._extract_scalar(report, "volatility", 0.0) or 0.0)
        ai_alignment = float(
            self._extract_scalar(forecast, "ai_alignment", 1.0) or 0.0
        )
        focus = str(self._extract_scalar(forecast, "recommended_focus", "balance")).lower()
        target_fun = self._extract_scalar(forecast, "expected_fun")
        if target_fun is not None:
            target_fun = _clamp(float(target_fun))
        else:
            target_fun = _clamp(
                self.fun_level * 0.6
                + self.ai_fun_projection * 0.25
                + self.base_fun_level * 0.15
            )
        directives = self._build_fun_directives(
            self.get_ai_feedback(),
            target_fun=target_fun,
            focus=focus,
            classes=classes or {},
        )
        plan = ArenaFunTuningPlan(
            target_fun=round(target_fun, 3),
            baseline_fun=self.base_fun_level,
            fun_momentum=self.fun_momentum,
            ai_alignment=round(_clamp(ai_alignment), 3),
            focus=focus,
            volatility=round(_clamp(volatility, upper=1.0), 3),
            baseline_shift=round(target_fun - self.base_fun_level, 3),
            directives=tuple(directives),
            archetype_focus=self.get_ai_archetype_focus(),
        )
        return plan

    def get_ai_archetype_focus(self, limit: int = 3) -> tuple[str, ...]:
        """Return the most common archetypes observed in recent playtests."""

        if not self._archetype_history:
            return ()
        limit = max(1, limit)
        counts = Counter(self._archetype_history)
        return tuple(name for name, _ in counts.most_common(limit))

    def _build_season_summary(
        self, matches: int, participation_rate: float
    ) -> ArenaFunSeasonSummary:
        """Return a structured season summary using the current telemetry."""

        return ArenaFunSeasonSummary(
            season_fun=self.fun_level,
            baseline_fun=self.base_fun_level,
            ai_projection=self.ai_fun_projection,
            fun_momentum=self.fun_momentum,
            ai_participation=round(_clamp(participation_rate), 3),
            highlighted_archetypes=self.get_ai_archetype_focus(),
            win_leaders=self._top_ai_wins(),
            rounds_played=self._ai_season_rounds,
        )

    def _top_ai_wins(self, limit: int = 3) -> tuple[tuple[str, int], ...]:
        """Return the top ``limit`` AI win leaders for the background season."""

        if not self._ai_season_wins:
            return ()
        limit = max(1, limit)
        return tuple(self._ai_season_wins.most_common(limit))

    def simulate_ai_matches(
        self,
        snapshots: Iterable[Mapping[str, float]],
        *,
        rounds: int = 3,
    ) -> ArenaFunSeasonSummary:
        """Run AI-only matches and return a season-level fun summary."""

        snapshots = tuple(snapshots)
        if not snapshots:
            self._refresh_momentum()
            return self._build_season_summary(0, 0.0)

        total_participation = 0
        matches = 0
        for snapshot in snapshots:
            self.simulate_background_balancing(snapshot)
            if not self.ai_players:
                continue
            session_results: list[tuple[str, float]] = []
            for ai_player in self.ai_players:
                feedback = ai_player.playtest_arena(snapshot, rounds=rounds)
                projected = _clamp(float(feedback.get("projected_rating", 0.0)))
                session_results.append((ai_player.name, projected))
                total_participation += 1
                self._record_archetypes(feedback.get("preferred_archetypes", ()))
            if not session_results:
                continue
            matches += 1
            session_results.sort(key=lambda item: item[1], reverse=True)
            winner, top_projection = session_results[0]
            self._ai_season_wins[winner] += 1
            average_projection = sum(value for _, value in session_results) / len(
                session_results
            )
            self.ai_fun_projection = round(_clamp(average_projection), 3)
            blend = _clamp(0.45 + min(0.25, rounds * 0.05))
            self.fun_level = round(
                (1.0 - blend) * self.fun_level + blend * self.ai_fun_projection,
                3,
            )
            self.fun_history.append(self.fun_level)
            self._update_baseline(
                self.baseline_adaptation * 0.6,
                target=self.ai_fun_projection,
            )
            self._record_consensus(abs(top_projection - self.fun_level))

        if matches:
            self._ai_season_rounds += matches
        participation_rate = 0.0
        if self.ai_players and matches:
            participation_rate = _clamp(
                total_participation / (len(self.ai_players) * matches)
            )
        self._refresh_momentum()
        return self._build_season_summary(matches, participation_rate)

    def reset_ai_season(self) -> None:
        """Clear accumulated AI season results."""

        self._ai_season_wins.clear()
        self._ai_season_rounds = 0

    def get_ai_season_wins(self) -> dict[str, int]:
        """Return background AI win counts from simulated matches."""

        return dict(self._ai_season_wins)

    @staticmethod
    def _extract_scalar(
        source: ArenaFunReport | ArenaFunForecast | Mapping[str, object] | None,
        key: str,
        default: object | None = None,
    ) -> object | None:
        """Return ``key`` from ``source`` whether it is an object or mapping."""

        if source is None:
            return default
        if hasattr(source, key):
            return getattr(source, key)
        if isinstance(source, Mapping):
            return source.get(key, default)
        return default

    def _build_fun_directives(
        self,
        ai_feedback: Mapping[str, float],
        *,
        target_fun: float,
        focus: str,
        classes: Mapping[str, Mapping[str, float]],
    ) -> list[ArenaFunDirective]:
        """Return directives describing how to adjust each class."""

        if not ai_feedback:
            return []
        directives: list[ArenaFunDirective] = []
        focus = focus.lower()
        for name, rating in sorted(
            ((key, _clamp(value)) for key, value in ai_feedback.items()),
            key=lambda item: item[1],
            reverse=True,
        ):
            delta = rating - target_fun
            weight = round(abs(delta), 3)
            if weight < 0.02:
                continue
            if delta > 0.04:
                action = "boost"
            elif delta < -0.04:
                action = "trim"
            else:
                action = "stabilize"
            stat_bias = self._derive_stat_bias(
                action,
                focus,
                classes.get(name),
            )
            rationale = (
                f"AI rating delta {delta:+.3f} vs target {target_fun:.2f}; "
                f"focus {focus or 'balance'}."
            )
            directives.append(
                ArenaFunDirective(
                    class_name=name,
                    action=action,
                    weight=weight,
                    stat_bias=stat_bias,
                    rationale=rationale,
                )
            )
        return directives

    @staticmethod
    def _derive_stat_bias(
        action: str,
        focus: str,
        stats: Mapping[str, float] | None,
    ) -> tuple[tuple[str, float], ...]:
        """Return stat weightings for a directive based on focus and class stats."""

        focus = focus.lower()
        if focus == "stabilize":
            base = {"attack": 0.18, "defense": 0.36, "health": 0.46}
        elif focus == "experiment":
            base = {"attack": 0.56, "defense": 0.24, "health": 0.2}
        elif focus == "elevate":
            base = {"attack": 0.32, "defense": 0.26, "health": 0.42}
        elif focus == "align_ai":
            base = {"attack": 0.38, "defense": 0.32, "health": 0.3}
        else:
            base = {"attack": 0.34, "defense": 0.32, "health": 0.34}

        action = action.lower()
        if action == "trim":
            base = {
                "attack": base["attack"] * 0.4,
                "defense": base["defense"] * 0.3,
                "health": base["health"] * 0.3,
            }
        elif action == "stabilize":
            base = {"attack": 0.22, "defense": 0.36, "health": 0.42}

        total = sum(base.values()) or 1.0
        base = {key: value / total for key, value in base.items()}

        if stats:
            attack = max(0.0, stats.get("attack", 0.0))
            defense = max(0.0, stats.get("defense", 0.0))
            health = max(0.0, stats.get("health", 0.0))
            total_stats = attack + defense + health
            if total_stats > 0.0:
                profile = {
                    "attack": attack / total_stats,
                    "defense": defense / total_stats,
                    "health": health / total_stats,
                }
                base = {
                    key: base[key] * 0.6 + profile[key] * 0.4
                    for key in base
                }
                total = sum(base.values()) or 1.0
                base = {key: value / total for key, value in base.items()}

        return tuple(sorted(base.items()))

    def _update_baseline(self, weight: float, *, target: float | None = None) -> None:
        """Blend the baseline fun toward ``target`` using ``weight``."""

        blend = _clamp(weight)
        if not blend:
            self._refresh_momentum()
            return

        target_value = _clamp(target if target is not None else self.fun_level)
        self.base_fun_level = round(
            (1.0 - blend) * self.base_fun_level + blend * target_value,
            3,
        )
        self._refresh_momentum()

    def _refresh_momentum(self) -> None:
        """Refresh the fun momentum cache."""

        self.fun_momentum = round(self.fun_level - self.base_fun_level, 3)
        if self.ai_players:
            self._record_consensus(abs(self.ai_fun_projection - self.fun_level))

    def _record_consensus(self, value: float) -> None:
        """Record background AI consensus drift for volatility tracking."""

        self._ai_consensus_history.append(round(_clamp(value), 3))

    def _calculate_volatility(self) -> float:
        """Return the standard deviation of the fun history."""

        if len(self.fun_history) < 2:
            return 0.0
        mean = sum(self.fun_history) / len(self.fun_history)
        variance = sum((value - mean) ** 2 for value in self.fun_history) / len(
            self.fun_history
        )
        return sqrt(max(0.0, variance))

    def _record_archetypes(self, archetypes: Iterable[str]) -> None:
        """Record preferred archetypes surfaced by AI playtests."""

        for archetype in archetypes:
            if archetype:
                self._archetype_history.append(archetype)

    def top_player(self) -> str | None:
        """Return the player with the highest recorded wins, if any."""

        return max(self.scores, key=self.scores.get) if self.scores else None
