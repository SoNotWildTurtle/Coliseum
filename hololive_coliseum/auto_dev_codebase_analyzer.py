"""Analyse auto-dev modules to highlight weak areas and mitigation steps."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _bool(value: Any) -> bool:
    return bool(value)


def _count_flags(values: Iterable[bool]) -> int:
    return sum(1 for value in values if value)


def _missing_indices(flags: Sequence[bool]) -> tuple[int, ...]:
    return tuple(index for index, flag in enumerate(flags, 1) if not flag)


def _risk_level(score: float) -> str:
    if score >= 4.0:
        return "critical"
    if score >= 2.5:
        return "high"
    if score >= 1.5:
        return "elevated"
    if score >= 0.5:
        return "moderate"
    return "low"


@dataclass
class AutoDevCodebaseAnalyzer:
    """Provide a deterministic assessment of codebase health signals."""

    complexity_threshold: float = 12.0
    warning_threshold: float = 18.0
    min_test_ratio: float = 0.65

    def evaluate(
        self,
        modules: Sequence[Mapping[str, Any]] | None,
        tests: Sequence[Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Return a snapshot of weak areas and recommended mitigations."""

        module_list = list(modules or [])
        test_list = list(tests or [])
        total_modules = len(module_list)
        total_tests = len(test_list)
        if total_modules == 0:
            return {
                "status": "no-data",
                "coverage_ratio": 0.0,
                "average_complexity": 0.0,
                "weakness_signals": ("No modules supplied for analysis",),
                "mitigation_plan": ("Instrument module metrics before next sprint",),
            }

        complexities = [_as_float(module.get("complexity"), 8.0) for module in module_list]
        docstring_flags = [_bool(module.get("docstring", True)) for module in module_list]
        test_flags = [_bool(module.get("has_tests")) for module in module_list]
        incidents = [
            _count_flags(module.get("recent_incidents", ())) for module in module_list
        ]

        avg_complexity = sum(complexities) / total_modules
        test_ratio = _count_flags(test_flags) / total_modules if total_modules else 0.0
        docstring_ratio = _count_flags(docstring_flags) / total_modules
        instability_index = self._instability_index(complexities, incidents)

        weakness_signals = self._weakness_signals(
            complexities,
            test_flags,
            docstring_flags,
            incidents,
        )
        mitigation_plan = self._mitigation_plan(
            weakness_signals,
            docstring_ratio,
            test_ratio,
            instability_index,
        )
        debt_profile = self._debt_profile(
            complexities,
            test_flags,
            docstring_flags,
            incidents,
            instability_index,
        )
        scorecards = self._module_scorecards(
            module_list,
            complexities,
            test_flags,
            docstring_flags,
            incidents,
        )
        modernization_targets = self._modernization_targets(
            scorecards,
            debt_profile,
            mitigation_plan,
        )

        functionality_gap_index, functionality_gaps = self._functionality_gaps(
            module_list,
            complexities,
            test_flags,
            docstring_flags,
            total_modules,
        )
        mechanics_alignment_score = self._mechanics_alignment_score(
            functionality_gap_index,
            instability_index,
        )
        design_fragility_index, design_focus_modules, design_recommendations = (
            self._design_fragility(
                module_list,
                functionality_gaps,
                scorecards,
                modernization_targets,
            )
        )
        (
            systems_fragility_index,
            systems_focus_modules,
            systems_recommendations,
            systems_alignment_index,
        ) = self._systems_fragility(
            module_list,
            functionality_gap_index,
            mechanics_alignment_score,
            design_fragility_index,
            debt_profile,
            modernization_targets,
        )

        creation_gap_index = min(
            100.0,
            functionality_gap_index * 0.45
            + design_fragility_index * 0.35
            + systems_fragility_index * 0.3,
        )
        creation_focus_sources: list[str] = []
        for gap in functionality_gaps[:4]:
            label = str(gap).strip()
            if label and label not in creation_focus_sources:
                creation_focus_sources.append(label)
        for module in (*design_focus_modules, *systems_focus_modules):
            label = str(module).strip()
            if label and label not in creation_focus_sources:
                creation_focus_sources.append(label)
        creation_recommendations = []
        for recommendation in (*design_recommendations, *systems_recommendations):
            text = str(recommendation).strip()
            if text and text not in creation_recommendations:
                creation_recommendations.append(text)
        if not creation_recommendations:
            creation_recommendations.extend(functionality_gaps[:2])
        creation_alignment_score = max(
            0.0,
            min(
                100.0,
                mechanics_alignment_score * 0.5
                + (100.0 - functionality_gap_index) * 0.2
                + (100.0 - design_fragility_index) * 0.15
                + (100.0 - systems_fragility_index) * 0.15,
            ),
        )
        convergence_focus_modules: list[str] = []
        for source in creation_focus_sources:
            text = str(source).strip()
            if text and text not in convergence_focus_modules:
                convergence_focus_modules.append(text)
        for target in modernization_targets[:4]:
            label = str(target.get("name", "")).strip()
            if label and label not in convergence_focus_modules:
                convergence_focus_modules.append(label)
        convergence_gap_index = min(
            100.0,
            creation_gap_index * 0.4
            + (100.0 - mechanics_alignment_score) * 0.25
            + (100.0 - creation_alignment_score) * 0.2
            + instability_index * 22.0,
        )
        convergence_gap_index = max(0.0, convergence_gap_index)
        convergence_alignment_score = max(
            0.0,
            min(
                100.0,
                creation_alignment_score * 0.4
                + systems_alignment_index * 0.3
                + (100.0 - creation_gap_index) * 0.2
                + (100.0 - design_fragility_index) * 0.1,
            ),
        )
        implementation_gap_index = min(
            100.0,
            convergence_gap_index * 0.45
            + creation_gap_index * 0.35
            + functionality_gap_index * 0.25
            + instability_index * 18.0,
        )
        implementation_gap_index = max(0.0, implementation_gap_index)
        implementation_alignment_score = max(
            0.0,
            min(
                100.0,
                convergence_alignment_score * 0.4
                + creation_alignment_score * 0.3
                + systems_alignment_index * 0.2
                + (1.0 - debt_profile["risk_score"]) * 100.0 * 0.1,
            ),
        )
        implementation_focus_modules: list[str] = []
        for module in convergence_focus_modules[:4]:
            label = str(module).strip()
            if label and label not in implementation_focus_modules:
                implementation_focus_modules.append(label)
        for recommendation in creation_recommendations[:3]:
            label = str(recommendation).split(":", 1)[0].strip()
            if label and label not in implementation_focus_modules:
                implementation_focus_modules.append(label)
        for card in scorecards:
            risk_level = str(card.get("risk_level", "low")).lower()
            name = str(card.get("name", "")).strip()
            if risk_level in {"high", "critical"} and name and name not in implementation_focus_modules:
                implementation_focus_modules.append(name)
        implementation_focus_modules = implementation_focus_modules[:6]
        implementation_recommendations: list[str] = []
        for action in mitigation_plan[:3]:
            text = str(action).strip()
            if text and text not in implementation_recommendations:
                implementation_recommendations.append(text)
        for signal in weakness_signals[:2]:
            text = str(signal).strip()
            if text:
                note = f"Investigate: {text}"
                if note not in implementation_recommendations:
                    implementation_recommendations.append(note)

        execution_gap_index = min(
            100.0,
            implementation_gap_index * 0.5
            + convergence_gap_index * 0.25
            + creation_gap_index * 0.2
            + instability_index * 18.0,
        )
        execution_gap_index = max(0.0, execution_gap_index)
        execution_alignment_score = max(
            0.0,
            min(
                100.0,
                implementation_alignment_score * 0.4
                + convergence_alignment_score * 0.25
                + creation_alignment_score * 0.2
                + (1.0 - debt_profile["risk_score"]) * 100.0 * 0.15,
            ),
        )
        execution_focus_modules: list[str] = []
        for module in implementation_focus_modules:
            text = str(module).strip()
            if text and text not in execution_focus_modules:
                execution_focus_modules.append(text)
        for module in convergence_focus_modules[:4]:
            text = str(module).strip()
            if text and text not in execution_focus_modules:
                execution_focus_modules.append(text)
        for target in modernization_targets[:3]:
            name = str(target.get("name", "")).strip()
            if name and name not in execution_focus_modules:
                execution_focus_modules.append(name)
        if not execution_focus_modules:
            execution_focus_modules.extend(creation_focus_sources[:3])
        execution_recommendations: list[str] = []
        for recommendation in implementation_recommendations[:4]:
            text = str(recommendation).strip()
            if text and text not in execution_recommendations:
                execution_recommendations.append(text)
        for target in modernization_targets[:2]:
            steps: Sequence[Any] = target.get("modernization_steps", ())  # type: ignore[assignment]
            if not steps:
                continue
            step_text = ", ".join(str(step).strip() for step in steps if str(step).strip())
            if step_text:
                entry = f"{target.get('name', 'module')}: {step_text}".strip()
                if entry and entry not in execution_recommendations:
                    execution_recommendations.append(entry)
        if not execution_recommendations:
            execution_recommendations.extend(weakness_signals[:2])

        blueprint_gap_index = min(
            100.0,
            creation_gap_index * 0.35
            + functionality_gap_index * 0.35
            + (100.0 - mechanics_alignment_score) * 0.2
            + design_fragility_index * 0.18
            + systems_fragility_index * 0.18,
        )
        blueprint_gap_index = max(0.0, blueprint_gap_index)
        blueprint_alignment_score = max(
            0.0,
            min(
                100.0,
                creation_alignment_score * 0.28
                + mechanics_alignment_score * 0.28
                + systems_alignment_index * 0.2
                + (100.0 - blueprint_gap_index) * 0.14
                + (100.0 - design_fragility_index) * 0.1,
            ),
        )
        blueprint_focus_modules: list[str] = []
        for module in (
            *creation_focus_sources,
            *design_focus_modules,
            *systems_focus_modules,
            *convergence_focus_modules,
        ):
            name = str(module).strip()
            if name and name not in blueprint_focus_modules:
                blueprint_focus_modules.append(name)
        blueprint_recommendations: list[str] = []
        for recommendation in (
            *creation_recommendations,
            *design_recommendations,
            *systems_recommendations,
            *implementation_recommendations,
        ):
            text = str(recommendation).strip()
            if text and text not in blueprint_recommendations:
                blueprint_recommendations.append(text)
        if not blueprint_recommendations:
            blueprint_recommendations.extend(weakness_signals[:2])

        iteration_gap_index = min(
            100.0,
            creation_gap_index * 0.32
            + functionality_gap_index * 0.32
            + blueprint_gap_index * 0.2
            + (100.0 - mechanics_alignment_score) * 0.16,
        )
        iteration_gap_index = max(0.0, iteration_gap_index)
        iteration_alignment_score = max(
            0.0,
            min(
                100.0,
                creation_alignment_score * 0.22
                + blueprint_alignment_score * 0.24
                + mechanics_alignment_score * 0.2
                + systems_alignment_index * 0.14
                + (100.0 - iteration_gap_index) * 0.2,
            ),
        )
        iteration_focus_modules: list[str] = []
        for module in (
            *creation_focus_sources,
            *blueprint_focus_modules,
            *functionality_gaps[:4],
        ):
            text = str(module).strip()
            if text and text not in iteration_focus_modules:
                iteration_focus_modules.append(text)
        iteration_recommendations: list[str] = []
        for recommendation in (
            *creation_recommendations,
            *blueprint_recommendations,
            *implementation_recommendations,
            *functionality_gaps[:3],
        ):
            text = str(recommendation).strip()
            if text and text not in iteration_recommendations:
                iteration_recommendations.append(text)
        if not iteration_recommendations:
            iteration_recommendations.extend(weakness_signals[:2])

        return {
            "status": "analysed",
            "coverage_ratio": round(test_ratio, 2),
            "average_complexity": round(avg_complexity, 2),
            "docstring_ratio": round(docstring_ratio, 2),
            "instability_index": round(instability_index, 2),
            "weakness_signals": tuple(weakness_signals),
            "mitigation_plan": tuple(mitigation_plan),
            "total_modules": total_modules,
            "total_tests": total_tests,
            "debt_profile": debt_profile,
            "stability_outlook": debt_profile["stability_outlook"],
            "debt_risk_score": debt_profile["risk_score"],
            "module_scorecards": tuple(scorecards),
            "modernization_targets": tuple(modernization_targets),
            "functionality_gap_index": round(functionality_gap_index, 2),
            "functionality_gaps": tuple(functionality_gaps),
            "mechanics_alignment_score": round(mechanics_alignment_score, 2),
            "design_fragility_index": round(design_fragility_index, 2),
            "design_focus_modules": tuple(design_focus_modules),
            "design_recommendations": tuple(design_recommendations),
            "systems_fragility_index": round(systems_fragility_index, 2),
            "systems_focus_modules": tuple(systems_focus_modules),
            "systems_recommendations": tuple(systems_recommendations),
            "systems_alignment_index": round(systems_alignment_index, 2),
            "creation_gap_index": round(creation_gap_index, 2),
            "creation_focus_modules": tuple(creation_focus_sources[:6]),
            "creation_recommendations": tuple(creation_recommendations[:6]),
            "creation_alignment_score": round(creation_alignment_score, 2),
            "blueprint_gap_index": round(blueprint_gap_index, 2),
            "blueprint_alignment_score": round(blueprint_alignment_score, 2),
            "blueprint_focus_modules": tuple(blueprint_focus_modules[:6]),
            "blueprint_recommendations": tuple(blueprint_recommendations[:6]),
            "iteration_gap_index": round(iteration_gap_index, 2),
            "iteration_alignment_score": round(iteration_alignment_score, 2),
            "iteration_focus_modules": tuple(iteration_focus_modules[:6]),
            "iteration_recommendations": tuple(iteration_recommendations[:6]),
            "convergence_gap_index": round(convergence_gap_index, 2),
            "convergence_alignment_score": round(convergence_alignment_score, 2),
            "convergence_focus_modules": tuple(convergence_focus_modules[:6]),
            "implementation_gap_index": round(implementation_gap_index, 2),
            "implementation_alignment_score": round(implementation_alignment_score, 2),
            "implementation_focus_modules": tuple(implementation_focus_modules),
            "implementation_recommendations": tuple(
                implementation_recommendations[:6]
            ),
            "execution_gap_index": round(execution_gap_index, 2),
            "execution_alignment_score": round(execution_alignment_score, 2),
            "execution_focus_modules": tuple(execution_focus_modules[:6]),
            "execution_recommendations": tuple(execution_recommendations[:6]),
        }

    def _instability_index(
        self,
        complexities: Sequence[float],
        incidents: Sequence[int],
    ) -> float:
        if not complexities:
            return 0.0
        max_complexity = max(complexities)
        total_incidents = sum(incidents)
        trend = (max_complexity / (self.warning_threshold or 1.0))
        return min(2.0, trend + total_incidents * 0.1)

    def _weakness_signals(
        self,
        complexities: Sequence[float],
        test_flags: Sequence[bool],
        docstring_flags: Sequence[bool],
        incidents: Sequence[int],
    ) -> list[str]:
        signals: list[str] = []
        for index, complexity in enumerate(complexities):
            if complexity >= self.warning_threshold:
                signals.append(f"Module {index + 1} complexity exceeds warning threshold")
            elif complexity >= self.complexity_threshold:
                signals.append(f"Module {index + 1} complexity trending high")
        missing_tests = [idx for idx, flag in enumerate(test_flags, 1) if not flag]
        if missing_tests:
            display = ", ".join(str(idx) for idx in missing_tests[:3])
            signals.append(f"Tests missing for modules: {display}")
        missing_docstrings = [
            idx for idx, flag in enumerate(docstring_flags, 1) if not flag
        ]
        if missing_docstrings:
            display = ", ".join(str(idx) for idx in missing_docstrings[:3])
            signals.append(f"Docstrings absent for modules: {display}")
        hot_modules = [idx for idx, value in enumerate(incidents, 1) if value]
        if hot_modules:
            display = ", ".join(str(idx) for idx in hot_modules[:3])
            signals.append(f"Recent incidents recorded for modules: {display}")
        if not signals:
            signals.append("Codebase health stable")
        return signals

    def _mitigation_plan(
        self,
        weakness_signals: Sequence[str],
        docstring_ratio: float,
        test_ratio: float,
        instability_index: float,
    ) -> list[str]:
        plan: list[str] = []
        if any("Tests missing" in signal for signal in weakness_signals):
            plan.append("Schedule regression tests for uncovered modules")
        if docstring_ratio < 0.9:
            plan.append("Document critical modules to support auto-dev reasoning")
        if test_ratio < self.min_test_ratio:
            plan.append("Increase automated test creation to reach baseline coverage")
        if instability_index >= 1.5:
            plan.append("Refactor high complexity hotspots before next release")
        if not plan:
            plan.append("Maintain cadence: no critical remediation required")
        return plan

    def _debt_profile(
        self,
        complexities: Sequence[float],
        test_flags: Sequence[bool],
        docstring_flags: Sequence[bool],
        incidents: Sequence[int],
        instability_index: float,
    ) -> dict[str, Any]:
        high_complexity = tuple(
            index + 1 for index, value in enumerate(complexities) if value >= self.warning_threshold
        )
        trending_complexity = tuple(
            index + 1
            for index, value in enumerate(complexities)
            if self.complexity_threshold <= value < self.warning_threshold
        )
        missing_tests = _missing_indices(test_flags)
        missing_docstrings = _missing_indices(docstring_flags)
        incident_modules = tuple(
            index + 1 for index, count in enumerate(incidents) if count
        )
        risk_score = round(
            min(
                1.0,
                (instability_index / 2.0)
                + (len(missing_tests) * 0.05)
                + (len(incident_modules) * 0.08)
                + (len(high_complexity) * 0.07),
            ),
            2,
        )
        outlook = self._stability_outlook(
            instability_index,
            len(missing_tests),
            len(incident_modules),
            len(high_complexity),
        )
        return {
            "high_complexity": high_complexity,
            "complexity_watch": trending_complexity,
            "missing_tests": missing_tests,
            "missing_docstrings": missing_docstrings,
            "incident_modules": incident_modules,
            "risk_score": risk_score,
            "stability_outlook": outlook,
        }

    def _stability_outlook(
        self,
        instability_index: float,
        missing_tests: int,
        incidents: int,
        high_complexity: int,
    ) -> str:
        if instability_index >= 1.7 or high_complexity >= 2:
            return "refactor-critical"
        if missing_tests >= 2 or incidents >= 2:
            return "stabilise"
        if instability_index <= 0.6 and missing_tests == 0 and incidents == 0:
            return "steady"
        return "improve"

    def _module_scorecards(
        self,
        modules: Sequence[Mapping[str, Any]],
        complexities: Sequence[float],
        test_flags: Sequence[bool],
        docstring_flags: Sequence[bool],
        incidents: Sequence[int],
    ) -> list[dict[str, Any]]:
        scorecards: list[dict[str, Any]] = []
        for index, module in enumerate(modules):
            name = str(module.get("name") or f"module_{index + 1}")
            complexity = float(complexities[index])
            tested = bool(test_flags[index])
            documented = bool(docstring_flags[index])
            incident_count = int(incidents[index])
            flags: list[str] = []
            actions: list[str] = []
            score = 0.0
            if complexity >= self.warning_threshold:
                flags.append("Complexity above warning threshold")
                actions.append("Refactor critical branches for stability")
                score += 2.6
            elif complexity >= self.complexity_threshold:
                flags.append("Complexity trending high")
                actions.append("Break module into focused helpers")
                score += 1.4
            if not tested:
                flags.append("Missing automated tests")
                actions.append("Add regression tests covering auto-dev behaviours")
                score += 1.7
            if not documented:
                flags.append("Docstring missing")
                actions.append("Document module intent for auto-dev tooling")
                score += 0.6
            if incident_count:
                flags.append(f"{incident_count} recent incident(s)")
                actions.append("Audit incident causes and add safeguards")
                score += min(2.0, incident_count * 0.8)
            stability_modifier = min(1.0, max(0.0, score / 5.0))
            risk_level = _risk_level(score)
            scorecards.append(
                {
                    "name": name,
                    "complexity": round(complexity, 2),
                    "has_tests": tested,
                    "docstring": documented,
                    "recent_incidents": incident_count,
                    "risk_flags": tuple(dict.fromkeys(flags)) or ("Healthy",),
                    "risk_level": risk_level,
                    "stability_modifier": round(stability_modifier, 2),
                    "recommended_actions": tuple(dict.fromkeys(actions)),
                }
            )
        return scorecards

    def _module_label(self, module: Mapping[str, Any], index: int) -> str:
        name = str(module.get("name") or f"module-{index + 1}")
        name = name.strip() or f"module-{index + 1}"
        return name[:48]

    def _functionality_gaps(
        self,
        modules: Sequence[Mapping[str, Any]],
        complexities: Sequence[float],
        test_flags: Sequence[bool],
        docstring_flags: Sequence[bool],
        total_modules: int,
    ) -> tuple[float, list[str]]:
        if not total_modules:
            return 0.0, []

        missing_tests = [index for index, flag in enumerate(test_flags, 1) if not flag]
        missing_docstrings = [
            index for index, flag in enumerate(docstring_flags, 1) if not flag
        ]
        high_complexity = [
            index
            for index, complexity in enumerate(complexities, 1)
            if complexity >= self.complexity_threshold
        ]

        gap_index = (
            (len(missing_tests) / total_modules) * 55.0
            + (len(missing_docstrings) / total_modules) * 25.0
            + (len(high_complexity) / total_modules) * 35.0
        )
        gap_index = min(100.0, max(0.0, gap_index))

        gaps: list[str] = []
        for idx in range(total_modules):
            module = modules[idx]
            issues: list[str] = []
            position = idx + 1
            if position in missing_tests:
                issues.append("tests")
            if position in missing_docstrings:
                issues.append("docs")
            if position in high_complexity:
                issues.append("complexity")
            if issues:
                label = self._module_label(module, idx)
                issues_display = ", ".join(issues)
                gaps.append(f"{label} lacks {issues_display} coverage")

        return gap_index, gaps

    def _mechanics_alignment_score(
        self,
        functionality_gap_index: float,
        instability_index: float,
    ) -> float:
        stability_drag = max(0.0, (instability_index - 0.8) * 32.0)
        score = 100.0 - functionality_gap_index * 0.6 - stability_drag
        return max(0.0, min(100.0, score))

    def _design_fragility(
        self,
        modules: Sequence[Mapping[str, Any]],
        functionality_gaps: Sequence[str],
        scorecards: Sequence[Mapping[str, Any]],
        modernization_targets: Sequence[Mapping[str, Any]],
    ) -> tuple[float, list[str], list[str]]:
        total_modules = len(modules)
        if total_modules == 0:
            return 0.0, [], []

        high_risk_modules = [
            str(card.get("name", "module"))
            for card in scorecards
            if str(card.get("risk_level", "")).lower() in {"critical", "high"}
        ]
        modernization_focus = [
            str(target.get("name", "module"))
            for target in modernization_targets
            if isinstance(target, Mapping)
        ]
        coverage_pressure = len(functionality_gaps) / total_modules if total_modules else 0.0
        fragility_index = min(
            100.0,
            coverage_pressure * 55.0
            + len(high_risk_modules) * 6.5
            + len(modernization_focus) * 4.5,
        )

        focus_modules: list[str] = []
        for name in (*high_risk_modules, *modernization_focus):
            label = name.strip()
            if label and label not in focus_modules:
                focus_modules.append(label)
        if not focus_modules:
            sample_names = [
                str(module.get("name") or f"module_{index + 1}")
                for index, module in enumerate(modules[:3])
            ]
            focus_modules.extend(sample_names)

        recommendations: list[str] = []
        for target in modernization_targets[:3]:
            if not isinstance(target, Mapping):
                continue
            steps: Sequence[Any] = target.get("modernization_steps", ())  # type: ignore[assignment]
            if not steps:
                continue
            step_text = ", ".join(str(step).strip() for step in steps if str(step).strip())
            if step_text:
                recommendations.append(
                    f"{target.get('name', 'module')}: {step_text}".strip()
                )
        if not recommendations:
            recommendations.extend(functionality_gaps[:2])
        if not recommendations:
            recommendations.append("Maintain design cadence across auto-dev modules")

        return fragility_index, focus_modules[:5], recommendations[:5]

    def _systems_fragility(
        self,
        modules: Sequence[Mapping[str, Any]],
        functionality_gap_index: float,
        mechanics_alignment_score: float,
        design_fragility_index: float,
        debt_profile: Mapping[str, Any],
        modernization_targets: Sequence[Mapping[str, Any]],
    ) -> tuple[float, list[str], list[str], float]:
        risk_score = float(debt_profile.get("risk_score", 0.0))
        fragility_index = min(
            100.0,
            functionality_gap_index * 0.5
            + max(0.0, 80.0 - mechanics_alignment_score) * 0.4
            + design_fragility_index * 0.35
            + risk_score * 22.0,
        )

        focus_modules: list[str] = []
        for target in modernization_targets:
            if not isinstance(target, Mapping):
                continue
            name = str(target.get("name", "")).strip()
            if name and name not in focus_modules:
                focus_modules.append(name)

        high_complexity = debt_profile.get("high_complexity", ())
        for index in high_complexity[:3]:
            position = int(index) - 1
            if 0 <= position < len(modules):
                label = self._module_label(modules[position], position)
                if label and label not in focus_modules:
                    focus_modules.append(label)

        if not focus_modules:
            fallback = [
                str(module.get("name") or f"module_{idx + 1}")
                for idx, module in enumerate(modules[:3])
            ]
            focus_modules.extend(fallback)

        recommendations: list[str] = []
        for target in modernization_targets[:3]:
            if not isinstance(target, Mapping):
                continue
            steps: Sequence[Any] = target.get("modernization_steps", ())  # type: ignore[assignment]
            if not steps:
                continue
            step_text = ", ".join(
                str(step).strip() for step in steps if str(step).strip()
            )
            if step_text:
                name = str(target.get("name", "module")).strip()
                recommendations.append(f"{name or 'module'}: {step_text}")
        if not recommendations:
            recommendations.append(
                "Schedule systems alignment review for auto-dev modules"
            )

        alignment_index = max(
            0.0,
            min(
                100.0,
                mechanics_alignment_score * 0.6
                + (100.0 - design_fragility_index) * 0.25
                + (1.0 - risk_score) * 25.0,
            ),
        )

        return fragility_index, focus_modules[:5], recommendations[:5], alignment_index

    def _modernization_targets(
        self,
        scorecards: Sequence[Mapping[str, Any]],
        debt_profile: Mapping[str, Any],
        mitigation_plan: Sequence[str],
    ) -> list[dict[str, Any]]:
        targets: list[dict[str, Any]] = []
        for card in scorecards:
            risk_level = str(card.get("risk_level", "low"))
            if risk_level not in {"critical", "high"}:
                continue
            actions: Sequence[str] = card.get("recommended_actions", ())  # type: ignore[assignment]
            targets.append(
                {
                    "name": card.get("name", "module"),
                    "risk_level": risk_level,
                    "modernization_steps": tuple(actions[:3]) if actions else ("Schedule review",),
                    "stability_modifier": float(card.get("stability_modifier", 0.0)),
                }
            )
        if not targets and debt_profile.get("risk_score", 0.0) >= 0.3:
            focus = next(iter(mitigation_plan), "Expand regression coverage")
            targets.append(
                {
                    "name": "auto-dev-governance",
                    "risk_level": "moderate",
                    "modernization_steps": (str(focus),),
                    "stability_modifier": float(debt_profile.get("risk_score", 0.0)),
                }
            )
        if not targets:
            targets.append(
                {
                    "name": "baseline",
                    "risk_level": "low",
                    "modernization_steps": ("Maintain automated cleanups",),
                    "stability_modifier": 0.0,
                }
            )
        return targets[:5]
