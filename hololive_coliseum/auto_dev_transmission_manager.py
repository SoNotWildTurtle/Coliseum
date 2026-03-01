"""Calibrate holographic transmissions for the auto-dev networking stack."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@dataclass
class AutoDevTransmissionManager:
    """Derive holographic compression and security directives from telemetry."""

    base_algorithm: str = "zlib"
    baseline_level: int = 6
    aggressive_threshold: float = 0.72
    secure_threshold: float = 0.55

    def calibrate(
        self,
        network: Mapping[str, Any] | None = None,
        *,
        research: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return deterministic calibration data for holographic transmissions."""

        network = network or {}
        research = research or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        security = security or {}

        holographic = dict(network.get("holographic_channels", {}))
        diagnostics = dict(network.get("holographic_diagnostics", {}))
        verification = dict(network.get("verification_layers", {}))
        processing_detail = dict(network.get("network_processing_detail", {}))
        security_auto_dev = dict(network.get("security_auto_dev", {}))
        resilience = dict(network.get("resilience_matrix", {}))
        enhancements = dict(network.get("holographic_enhancements", {}))
        bandwidth = dict(network.get("bandwidth", {}))
        guardrails = dict(network.get("transmission_guardrails", {}))
        lithographic = dict(network.get("lithographic_integrity", {}))

        efficiency = _as_float(diagnostics.get("efficiency_score"))
        phase = _as_float(diagnostics.get("phase_coherence_index"))
        encrypted = _as_int(holographic.get("encrypted_channels", processing_detail.get("encrypted_channels")))
        layer_count = _as_int(holographic.get("layer_count", verification.get("layers")))
        severity_focus: Sequence[str] = verification.get("severity_focus", ())  # type: ignore[assignment]
        integrity = str(verification.get("integrity", "stable"))
        average_bandwidth = _as_float(bandwidth.get("average_mbps"))
        auto_load = _as_float(network.get("processing_utilization_percent"))

        compression = self._compression_profile(
            efficiency,
            phase,
            encrypted,
            layer_count,
            security_auto_dev.get("directive"),
        )
        phase_alignment = self._phase_alignment(
            phase,
            integrity,
            enhancements.get("phase_lock_directives"),
            mitigation.get("holographic_upgrades"),
        )
        security_layers = self._security_layers(
            layer_count,
            severity_focus,
            integrity,
            security_auto_dev.get("verification_layers"),
        )
        utilization_projection = self._utilization_projection(
            research,
            remediation.get("applied_fixes"),
            mitigation.get("priority"),
        )
        bandwidth_budget = self._bandwidth_budget(
            average_bandwidth,
            compression["level"],
            auto_load,
            resilience.get("score"),
        )
        notes = self._notes(
            compression,
            security_layers,
            mitigation.get("holographic_upgrades"),
            remediation.get("holographic_adjustments"),
        )
        guardrail_review = self._guardrail_review(
            guardrails,
            remediation.get("holographic_adjustments"),
        )
        lithographic_snapshot = self._lithographic_snapshot(
            diagnostics,
            guardrail_review,
            lithographic,
        )
        spectral_waveform = self._spectral_waveform(
            diagnostics,
            holographic,
            enhancements,
            guardrail_review,
        )
        lattice_overlay = self._lattice_overlay(
            security.get("holographic_lattice", {}),
            spectral_waveform,
            guardrail_review,
        )

        return {
            "compression_profile": compression,
            "phase_alignment": phase_alignment,
            "security_layers": security_layers,
            "bandwidth_budget_mbps": bandwidth_budget,
            "utilization_projection_percent": utilization_projection,
            "notes": notes,
            "guardrails": guardrail_review,
            "lithographic_integrity": lithographic_snapshot,
            "spectral_waveform": spectral_waveform,
            "lattice_overlay": lattice_overlay,
        }

    def _compression_profile(
        self,
        efficiency: float,
        phase: float,
        encrypted_channels: int,
        layer_count: int,
        directive: Any,
    ) -> dict[str, Any]:
        algorithm = self.base_algorithm
        level = self.baseline_level
        if efficiency >= self.aggressive_threshold and phase >= 0.6 and layer_count >= 3:
            algorithm = "auto"
            level = max(3, self.baseline_level - 2)
        elif efficiency <= self.secure_threshold or encrypted_channels < 2:
            algorithm = "lzma"
            level = min(9, self.baseline_level + 1)
        elif str(directive).lower() in {"fortify", "triage"}:
            algorithm = "lzma"
        return {
            "algorithm": algorithm,
            "level": level,
            "efficiency": round(efficiency, 2),
            "phase": round(phase, 2),
            "encrypted_channels": encrypted_channels,
            "layer_count": layer_count,
        }

    def _phase_alignment(
        self,
        phase: float,
        integrity: str,
        phase_directives: Any,
        holographic_upgrades: Any,
    ) -> dict[str, Any]:
        if integrity == "reinforce":
            target = 0.9
        elif integrity == "harden":
            target = 0.82
        else:
            target = max(0.75, phase)
        actions: list[str] = []
        if phase < target:
            actions.append("Increase lithographic anchor synchronisation")
        if phase_directives:
            actions.append(str(phase_directives))
        for upgrade in holographic_upgrades or ():
            actions.append(str(upgrade))
        return {
            "current": round(phase, 2),
            "target": round(target, 2),
            "actions": tuple(dict.fromkeys(actions)),
        }

    def _security_layers(
        self,
        layer_count: int,
        severity_focus: Sequence[str],
        integrity: str,
        verification_layers: Any,
    ) -> dict[str, Any]:
        recommended = layer_count
        if layer_count < 3 and integrity != "stable":
            recommended = layer_count + 2
        elif layer_count < 3:
            recommended = layer_count + 1
        verification_layers = _as_int(verification_layers, layer_count)
        return {
            "active_layers": layer_count,
            "recommended_layers": recommended,
            "severity_focus": tuple(str(item) for item in severity_focus),
            "verification_layers": verification_layers,
        }

    def _utilization_projection(
        self,
        research: Mapping[str, Any],
        applied_fixes: Any,
        mitigation_priority: Any,
    ) -> float:
        latest = research.get("latest_sample_percent")
        if latest is None:
            latest = research.get("raw_utilization_percent")
        base = _as_float(latest)
        applied_count = len(list(applied_fixes or ()))
        priority = str(mitigation_priority or "monitor").lower()
        bonus = 0.5
        if priority in {"high", "critical"}:
            bonus = 1.5
        elif priority == "medium":
            bonus = 1.0
        projected = min(100.0, base + applied_count * bonus)
        return round(projected, 2)

    def _bandwidth_budget(
        self,
        average_bandwidth: float,
        compression_level: int,
        auto_load: float,
        resilience_score: Any,
    ) -> float:
        if average_bandwidth <= 0:
            return 0.0
        resilience_factor = 1.0
        score = _as_float(resilience_score)
        if score < 45.0:
            resilience_factor = 0.85
        elif score > 70.0:
            resilience_factor = 1.1
        load_factor = max(0.6, 1.0 - (auto_load / 200.0))
        compression_factor = max(0.65, min(1.05, 1.0 - (compression_level - 4) * 0.03))
        budget = average_bandwidth * resilience_factor * load_factor * compression_factor
        return round(budget, 2)

    def _notes(
        self,
        compression: Mapping[str, Any],
        security_layers: Mapping[str, Any],
        upgrades: Any,
        adjustments: Any,
    ) -> tuple[str, ...]:
        notes: list[str] = []
        algorithm = compression.get("algorithm", "zlib")
        notes.append(f"Compression algorithm set to {algorithm}")
        notes.append(
            f"Security layers active/recommended: {security_layers.get('active_layers', 0)}"
            f"/{security_layers.get('recommended_layers', 0)}"
        )
        for upgrade in upgrades or ():
            notes.append(f"Mitigation upgrade queued: {upgrade}")
        for adjustment in adjustments or ():
            notes.append(f"Remediation adjustment applied: {adjustment}")
        return tuple(dict.fromkeys(notes))

    def _guardrail_review(
        self,
        guardrails: Mapping[str, Any],
        adjustments: Any,
    ) -> dict[str, Any]:
        status = str(guardrails.get("status", "nominal"))
        severity = str(guardrails.get("severity", "monitor"))
        actions: Sequence[str] = guardrails.get("actions", ())  # type: ignore[assignment]
        follow_up: list[str] = []
        for adjustment in adjustments or ():
            if "holographic" in str(adjustment).lower():
                follow_up.append(str(adjustment))
        return {
            "status": status,
            "severity": severity,
            "actions": tuple(dict.fromkeys(actions)),
            "follow_up": tuple(dict.fromkeys(follow_up)),
        }

    def _lithographic_snapshot(
        self,
        diagnostics: Mapping[str, Any],
        guardrails: Mapping[str, Any],
        network_snapshot: Mapping[str, Any],
    ) -> dict[str, Any]:
        efficiency = _as_float(diagnostics.get("efficiency_score"))
        phase = _as_float(diagnostics.get("phase_coherence_index"))
        base_score = _as_float(network_snapshot.get("score"), efficiency)
        severity = str(guardrails.get("severity", network_snapshot.get("severity", "monitor")))
        modifier = 0.0
        if severity == "critical":
            modifier = -12.0
        elif severity == "elevated":
            modifier = -6.0
        composite = max(0.0, min(100.0, base_score + modifier))
        headline = network_snapshot.get("headline_action") or guardrails.get(
            "actions",
            ("Maintain guardrails",),
        )
        if isinstance(headline, (list, tuple)):
            headline_action = headline[0] if headline else "Maintain guardrails"
        else:
            headline_action = str(headline)
        return {
            "score": round(composite, 2),
            "phase": round(phase, 2),
            "efficiency": round(efficiency, 2),
            "severity": severity,
            "headline_action": headline_action,
        }

    def _spectral_waveform(
        self,
        diagnostics: Mapping[str, Any],
        holographic: Mapping[str, Any],
        enhancements: Mapping[str, Any],
        guardrails: Mapping[str, Any],
    ) -> dict[str, Any]:
        phase = _as_float(diagnostics.get("phase_coherence_index"))
        efficiency = _as_float(diagnostics.get("efficiency_score"))
        layers = _as_int(holographic.get("layer_count", 0))
        guardrail_status = str(guardrails.get("status", "nominal"))
        stability = "steady"
        if phase < 0.5:
            stability = "turbulent"
        elif phase < 0.7:
            stability = "drifting"
        recommended: list[str] = []
        if stability != "steady":
            recommended.append("Apply lattice smoothing")
        if layers < 3:
            recommended.append("Increase holographic layer density")
        stability_phase = str(enhancements.get("stability_phase", "adaptive"))
        if guardrail_status != "nominal" and stability_phase == "adaptive":
            recommended.append("Lock guardrail anchors")
        if not recommended:
            recommended.append("Maintain spectral balance")
        return {
            "stability": stability,
            "bandwidth_density": round(max(0.0, min(1.0, efficiency)), 3),
            "phase_index": round(phase, 3),
            "recommended_actions": tuple(dict.fromkeys(recommended)),
        }

    def _lattice_overlay(
        self,
        lattice: Mapping[str, Any],
        waveform: Mapping[str, Any],
        guardrails: Mapping[str, Any],
    ) -> dict[str, Any]:
        density = _as_float(lattice.get("density"))
        coherence = _as_float(lattice.get("coherence"))
        stability = str(lattice.get("stability", waveform.get("stability", "steady")))
        overlay_actions: list[str] = []
        overlay_actions.extend(str(action) for action in lattice.get("actions", ()))
        for action in waveform.get("recommended_actions", ()):  # type: ignore[assignment]
            overlay_actions.append(str(action))
        guardrail_status = str(guardrails.get("status", "nominal"))
        if guardrail_status in {"reinforce", "elevated"}:
            overlay_actions.append("Synchronise lattice with guardrail review")
        if not overlay_actions:
            overlay_actions.append("Maintain lattice stability checks")
        return {
            "density": round(max(0.0, min(1.0, density)), 3),
            "coherence": round(max(0.0, min(1.0, coherence)), 3),
            "stability": stability,
            "actions": tuple(dict.fromkeys(overlay_actions)),
        }
