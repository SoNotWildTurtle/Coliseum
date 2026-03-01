"""Apply mitigation plans to simulate fixes within the auto-dev pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalise_codebase_tasks(tasks: Sequence[Any] | None) -> list[dict[str, Any]]:
    normalised: list[dict[str, Any]] = []
    for task in tasks or ():
        if isinstance(task, Mapping):
            entry = {"task": str(task.get("task", ""))}
            entry.update({
                "owner": task.get("owner", "Platform Core"),
                "severity": str(task.get("severity", "medium")).lower(),
            })
        else:
            entry = {
                "task": str(task),
                "owner": "Platform Core",
                "severity": "medium",
            }
        if not entry["task"]:
            continue
        normalised.append(entry)
    return normalised


def _normalise_strings(values: Sequence[Any] | None) -> list[str]:
    result: list[str] = []
    for value in values or ():
        text = str(value).strip()
        if text:
            result.append(text)
    return result


@dataclass
class AutoDevRemediationManager:
    """Implement mitigation actions to improve stability projections."""

    codebase_throughput: int = 2
    network_throughput: int = 2
    research_throughput: int = 1

    def implement_fixes(
        self,
        *,
        codebase: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        guidance: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return deterministic remediation actions derived from mitigation data."""

        codebase = codebase or {}
        mitigation = mitigation or {}
        network = network or {}
        research = research or {}
        guidance = guidance or {}

        codebase_tasks = _normalise_codebase_tasks(
            mitigation.get("codebase_tasks")  # type: ignore[arg-type]
        )
        network_tasks = _normalise_strings(
            mitigation.get("network_tasks")  # type: ignore[arg-type]
        )
        research_tasks = _normalise_strings(
            mitigation.get("research_tasks")  # type: ignore[arg-type]
        )
        intelligence_tasks = _normalise_strings(
            mitigation.get("intelligence_tasks")  # type: ignore[arg-type]
        )

        applied: list[dict[str, Any]] = []
        scheduled: list[dict[str, Any]] = []

        applied_counts = {
            "codebase": 0,
            "network": 0,
            "research": 0,
            "guidance": 0,
        }

        self._apply_codebase_tasks(codebase_tasks, applied, scheduled, applied_counts)
        self._apply_network_tasks(network_tasks, applied, scheduled, applied_counts)
        self._apply_research_tasks(research_tasks, applied, scheduled, applied_counts)
        self._apply_guidance_tasks(intelligence_tasks, applied, scheduled, applied_counts)

        stability_projection = self._stability_projection(
            codebase,
            network,
            research,
            guidance,
            applied_counts,
        )
        network_hardening = self._network_hardening(network, applied_counts["network"])
        research_balancing = self._research_balancing(research, applied_counts["research"])
        holographic_adjustments = self._holographic_adjustments(
            network,
            applied_counts["network"],
        )
        codebase_progress = self._codebase_progress(
            applied,
            codebase.get("module_scorecards"),
        )

        return {
            "applied_fixes": tuple(applied),
            "scheduled_fixes": tuple(scheduled),
            "stability_projection": stability_projection,
            "network_hardening": network_hardening,
            "research_balancing": research_balancing,
            "holographic_adjustments": tuple(holographic_adjustments),
            "codebase_progress": codebase_progress,
        }

    def _apply_codebase_tasks(
        self,
        tasks: Sequence[Mapping[str, Any]],
        applied: list[dict[str, Any]],
        scheduled: list[dict[str, Any]],
        counts: dict[str, int],
    ) -> None:
        throughput = max(0, self.codebase_throughput)
        for task in tasks:
            severity = str(task.get("severity", "medium")).lower()
            owner = str(task.get("owner", "Platform Core"))
            entry = {
                "domain": "codebase",
                "task": task.get("task", ""),
                "owner": owner,
                "severity": severity,
            }
            if counts["codebase"] < throughput and severity in {
                "critical",
                "high",
                "medium",
            }:
                entry["status"] = "applied"
                entry["impact"] = (
                    "coverage_boost"
                    if "test" in str(task.get("task", "")).lower()
                    else "stability"
                )
                applied.append(entry)
                counts["codebase"] += 1
            else:
                entry["status"] = "scheduled"
                scheduled.append(entry)

    def _apply_network_tasks(
        self,
        tasks: Sequence[str],
        applied: list[dict[str, Any]],
        scheduled: list[dict[str, Any]],
        counts: dict[str, int],
    ) -> None:
        throughput = max(0, self.network_throughput)
        for index, task in enumerate(tasks):
            entry = {
                "domain": "network",
                "task": task,
                "owner": "Network Reliability",
            }
            if counts["network"] < throughput:
                entry["status"] = "applied"
                entry["impact"] = "hardening"
                applied.append(entry)
                counts["network"] += 1
            else:
                entry["status"] = "scheduled"
                scheduled.append(entry)

    def _apply_research_tasks(
        self,
        tasks: Sequence[str],
        applied: list[dict[str, Any]],
        scheduled: list[dict[str, Any]],
        counts: dict[str, int],
    ) -> None:
        throughput = max(0, self.research_throughput)
        for task in tasks:
            entry = {
                "domain": "research",
                "task": task,
                "owner": "Intelligence Ops",
            }
            if counts["research"] < throughput:
                entry["status"] = "applied"
                entry["impact"] = "pressure_relief"
                applied.append(entry)
                counts["research"] += 1
            else:
                entry["status"] = "scheduled"
                scheduled.append(entry)

    def _apply_guidance_tasks(
        self,
        tasks: Sequence[str],
        applied: list[dict[str, Any]],
        scheduled: list[dict[str, Any]],
        counts: dict[str, int],
    ) -> None:
        for index, task in enumerate(tasks):
            entry = {
                "domain": "guidance",
                "task": task,
                "owner": "Encounter Direction",
            }
            if index == 0:
                entry["status"] = "applied"
                entry["impact"] = "alignment"
                applied.append(entry)
                counts["guidance"] += 1
            else:
                entry["status"] = "scheduled"
                scheduled.append(entry)

    def _stability_projection(
        self,
        codebase: Mapping[str, Any],
        network: Mapping[str, Any],
        research: Mapping[str, Any],
        guidance: Mapping[str, Any],
        counts: Mapping[str, int],
    ) -> dict[str, Any]:
        coverage = _as_float(codebase.get("coverage_ratio"))
        security_score = _as_float(network.get("network_security_score"))
        pressure_index = _as_float(research.get("research_pressure_index"))
        intelligence = _as_float(guidance.get("general_intelligence_score"))

        projected_coverage = min(1.0, coverage + counts["codebase"] * 0.04)
        projected_security = min(100.0, security_score + counts["network"] * 4.0)
        projected_pressure = max(0.0, pressure_index - counts["research"] * 6.0)
        projected_intelligence = min(
            100.0,
            intelligence + counts["guidance"] * 6.5 + counts["research"] * 3.0,
        )
        overall = min(
            100.0,
            (projected_coverage * 100.0 * 0.25)
            + (projected_security * 0.25)
            + (100.0 - projected_pressure) * 0.25
            + projected_intelligence * 0.25,
        )
        return {
            "coverage": round(coverage, 2),
            "projected_coverage": round(projected_coverage, 2),
            "security_score": round(security_score, 2),
            "projected_security_score": round(projected_security, 2),
            "pressure_index": round(pressure_index, 2),
            "projected_pressure_index": round(projected_pressure, 2),
            "intelligence_score": round(intelligence, 2),
            "projected_intelligence_score": round(projected_intelligence, 2),
            "overall_projection": round(overall, 2),
        }

    def _network_hardening(
        self,
        network: Mapping[str, Any],
        applied_network: int,
    ) -> dict[str, Any]:
        security = network.get("security_auto_dev", {})
        upgrades = network.get("network_security_upgrades", ())
        upgrade_focus = tuple(upgrades)[: applied_network or 2]
        zero_trust = network.get("zero_trust_blueprint", {})
        return {
            "applied_network_tasks": applied_network,
            "security_directive": security.get("directive", "stabilise"),
            "playbooks": tuple(security.get("playbooks", ())),
            "upgrade_focus": upgrade_focus,
            "zero_trust_actions": tuple(zero_trust.get("actions", ())),
        }

    def _research_balancing(
        self,
        research: Mapping[str, Any],
        applied_research: int,
    ) -> dict[str, Any]:
        latest = _as_float(research.get("latest_sample_percent"))
        pressure = _as_float(research.get("research_pressure_index"))
        volatility = _as_float(research.get("volatility_percent"))
        projected_pressure = max(0.0, pressure - applied_research * 6.0)
        return {
            "current_utilization_percent": round(latest, 2),
            "pressure_index": round(pressure, 2),
            "projected_pressure_index": round(projected_pressure, 2),
            "volatility_percent": round(volatility, 2),
            "actions_taken": applied_research,
        }

    def _holographic_adjustments(
        self,
        network: Mapping[str, Any],
        applied_network: int,
    ) -> list[str]:
        enhancements = network.get("holographic_enhancements", {})
        diagnostics = network.get("holographic_diagnostics", {})
        adjustments: list[str] = []
        if applied_network:
            layers = enhancements.get("layer_upgrades", ())
            for layer in layers[:applied_network]:
                adjustments.append(f"Activate holographic layer: {layer}")
            phase = enhancements.get("phase_lock_directives")
            if phase:
                adjustments.append(f"Apply phase directive: {phase}")
        efficiency = diagnostics.get("efficiency_score")
        if efficiency is not None:
            adjustments.append(
                f"Post-application holographic efficiency at {float(efficiency):.2f}"
            )
        if not adjustments:
            adjustments.append("Maintain holographic diagnostics monitoring")
        return adjustments

    def _codebase_progress(
        self,
        applied: Sequence[Mapping[str, Any]],
        scorecards: Sequence[Mapping[str, Any]] | None,
    ) -> tuple[dict[str, Any], ...]:
        cards = list(scorecards or ())
        if not cards:
            return ()
        addressed: set[str] = set()
        for fix in applied:
            if str(fix.get("domain")) != "codebase":
                continue
            task = str(fix.get("task", ""))
            if not task:
                continue
            name = task.split(" :: ")[0]
            addressed.add(name.strip())
        progress: list[dict[str, Any]] = []
        for card in cards:
            name = str(card.get("name", "module"))
            progress.append(
                {
                    "name": name,
                    "risk_level": card.get("risk_level", "low"),
                    "addressed": name in addressed,
                    "stability_modifier": card.get("stability_modifier", 0.0),
                }
            )
        return tuple(progress)
