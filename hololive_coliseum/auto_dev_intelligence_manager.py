"""Synthesize auto-dev signals into managerial general intelligence."""

from __future__ import annotations

from typing import Any, Dict, Iterable, Sequence


def _as_tuple(items: Iterable[str]) -> tuple[str, ...]:
    return tuple(item for item in items if item)


class AutoDevIntelligenceManager:
    """Translate auto-dev outputs into actionable oversight guidance."""

    def __init__(self, utilisation_ceiling: float = 55.0) -> None:
        self.utilisation_ceiling = float(utilisation_ceiling)

    def synthesise(
        self,
        *,
        monsters: Sequence[dict[str, Any]] | None = None,
        spawn_plan: dict[str, Any] | None = None,
        mob_ai: dict[str, Any] | None = None,
        boss_plan: dict[str, Any] | None = None,
        quests: Sequence[dict[str, Any]] | None = None,
        research: dict[str, Any] | None = None,
        guidance: dict[str, Any] | None = None,
        evolution: dict[str, Any] | None = None,
        network: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a high level general-intelligence brief for planners."""

        signals = [
            monsters,
            spawn_plan,
            mob_ai,
            boss_plan,
            quests,
            research,
            guidance,
            evolution,
            network,
        ]
        if not any(signals):
            return {}
        percent = self._processing_percent(research, guidance, evolution, network)
        raw_percent = self._raw_processing_percent(research, guidance, evolution, network)
        load_state = self._load_state(percent)
        research_view = self._research_view(research)
        encounter_alignment = self._encounter_alignment(
            monsters, spawn_plan, mob_ai, boss_plan
        )
        quest_alignment = self._quest_alignment(quests)
        encounter_blueprint = self._encounter_blueprint(
            monsters, spawn_plan, mob_ai, boss_plan
        )
        quest_synergy = self._quest_synergy(quests, boss_plan)
        monster_catalog = self._monster_catalog(monsters)
        spawn_overview = self._spawn_overview(spawn_plan)
        mob_ai_development = self._mob_ai_development(mob_ai)
        boss_outlook = self._boss_outlook(boss_plan, spawn_plan, quests)
        quest_matrix = self._quest_matrix(quests, boss_plan)
        group_mechanics = self._group_mechanics(monsters, spawn_plan)
        ai_training = self._mob_ai_training(mob_ai, monsters, spawn_plan)
        boss_pressure = self._boss_pressure(boss_plan, spawn_plan, monsters)
        quest_dependency = self._quest_dependency(quests, boss_plan)
        processing_overview = self._processing_overview(
            percent, raw_percent, research_view
        )
        evolution_alignment = self._evolution_alignment(guidance, evolution)
        backend_guidance = self._backend_guidance(
            guidance, evolution, research_view
        )
        pipeline = self._orchestration_pipeline(
            monsters, spawn_plan, mob_ai, boss_plan, quests, research
        )
        management_playbook = self._management_playbook(
            backend_guidance, pipeline, percent, raw_percent, network
        )
        processing_channels = self._processing_channels(
            research, guidance, evolution, network
        )
        monster_creation = self._monster_creation(monsters)
        spawn_tactics = self._spawn_tactics(spawn_plan)
        ai_development_plan = self._ai_development_plan(
            mob_ai, monsters, spawn_plan
        )
        boss_spawn_strategy = self._boss_spawn_strategy(
            boss_plan, spawn_plan, quests
        )
        quest_generation = self._quest_generation(quests, boss_plan)
        competitive_research = self._competitive_analysis(research)
        group_coordination = self._group_spawn_coordination(monsters, spawn_plan)
        ai_innovation = self._ai_innovation_focus(mob_ai, monsters)
        boss_spawn_readiness = self._boss_spawn_readiness(boss_plan, spawn_plan)
        quest_trade_alignment = self._quest_trade_skill_alignment(quests, boss_plan)
        managerial_overview = self._managerial_overview(
            backend_guidance,
            evolution_alignment,
            processing_overview,
            group_coordination,
            competitive_research,
            network,
        )
        monster_forge = self._monster_forge_detail(monsters)
        group_spawn_mechanics_detail = self._group_spawn_mechanics_detail(
            spawn_plan,
            monsters,
        )
        mob_ai_innovation_plan = self._mob_ai_innovation_plan(mob_ai, spawn_plan)
        boss_spawn_matrix = self._boss_spawn_matrix_detail(
            boss_plan,
            spawn_plan,
            quests,
        )
        quest_tradecraft = self._quest_tradecraft_detail(
            quests,
            boss_plan,
            spawn_plan,
        )
        research_pressure = self._research_pressure(research)
        managerial_alignment = self._managerial_alignment(
            backend_guidance,
            management_playbook,
            monster_forge,
            group_spawn_mechanics_detail,
        )
        network_health = self._network_health(network)
        network_security = self._network_security(network)
        network_upgrade_plan = self._network_upgrade_plan(network)
        network_processing = self._network_processing(network)
        network_security_automation = self._network_security_automation(network)
        holographic_transmission = self._holographic_transmission(network)
        network_verification_layers = self._network_verification_layers(network)
        monster_mutation_paths = self._monster_mutation_paths(monsters)
        group_support_matrix = self._group_spawn_support(spawn_plan, quests)
        ai_modularity_map = self._ai_modularity_map(mob_ai, spawn_plan)
        boss_spawn_alerts = self._boss_spawn_alerts(boss_plan, spawn_plan, network)
        quest_trade_dependencies = self._quest_trade_dependencies(quests, boss_plan)
        research_benchmarking = self._research_benchmarking(research)
        managerial_guidance_map = self._managerial_guidance_map(
            management_playbook,
            backend_guidance,
            research_benchmarking,
            group_support_matrix,
        )
        self_evolution_actions = self._self_evolution_actions(
            pipeline,
            managerial_alignment,
            boss_spawn_alerts,
            research_benchmarking,
        )
        return {
            "processing_utilization_percent": round(percent, 2),
            "raw_processing_percent": round(raw_percent, 2),
            "load_state": load_state,
            "resource_recommendation": self._resource_recommendation(load_state, percent),
            "encounter_alignment": encounter_alignment,
            "quest_alignment": quest_alignment,
            "encounter_blueprint": encounter_blueprint,
            "quest_synergy": quest_synergy,
            "monster_catalog": monster_catalog,
            "spawn_overview": spawn_overview,
            "mob_ai_development": mob_ai_development,
            "boss_outlook": boss_outlook,
            "quest_matrix": quest_matrix,
            "group_mechanics": group_mechanics,
            "mob_ai_training": ai_training,
            "boss_pressure": boss_pressure,
            "quest_dependency": quest_dependency,
            "processing_overview": processing_overview,
            "processing_channels": processing_channels,
            "evolution_alignment": evolution_alignment,
            "research_utilization": research_view,
            "backend_guidance": backend_guidance,
            "orchestration_pipeline": pipeline,
            "management_playbook": management_playbook,
            "monster_creation": monster_creation,
            "spawn_tactics": spawn_tactics,
            "ai_development_plan": ai_development_plan,
            "boss_spawn_strategy": boss_spawn_strategy,
            "quest_generation": quest_generation,
            "competitive_research": competitive_research,
            "group_spawn_coordination": group_coordination,
            "ai_innovation": ai_innovation,
            "boss_spawn_readiness": boss_spawn_readiness,
            "quest_trade_alignment": quest_trade_alignment,
            "managerial_overview": managerial_overview,
            "monster_forge": monster_forge,
            "group_spawn_mechanics_detail": group_spawn_mechanics_detail,
            "mob_ai_innovation_plan": mob_ai_innovation_plan,
            "boss_spawn_matrix": boss_spawn_matrix,
            "quest_tradecraft": quest_tradecraft,
            "research_pressure": research_pressure,
            "managerial_alignment": managerial_alignment,
            "network_health": network_health,
            "network_security": network_security,
            "network_upgrade_plan": network_upgrade_plan,
            "network_processing": network_processing,
            "network_security_automation": network_security_automation,
            "holographic_transmission": holographic_transmission,
            "network_verification_layers": network_verification_layers,
            "competitive_research_pressure": self._competitive_pressure(
                research,
                percent,
                raw_percent,
            ),
            "network_security_overview": self._network_security_overview(
                network_security,
                network_security_automation,
                network_upgrade_plan,
            ),
            "holographic_signal_health": self._holographic_signal_health(
                network,
                holographic_transmission,
                network_verification_layers,
            ),
            "self_evolution_dashboard": self._self_evolution_dashboard(
                backend_guidance,
                management_playbook,
                pipeline,
                network,
            ),
            "strategic_directives": _as_tuple(
                self._directives(guidance, evolution)
            ),
            "signals_considered": sum(1 for signal in signals if signal),
            "monster_mutation_paths": monster_mutation_paths,
            "group_spawn_support": group_support_matrix,
            "ai_modularity_map": ai_modularity_map,
            "boss_spawn_alerts": boss_spawn_alerts,
            "quest_trade_dependencies": quest_trade_dependencies,
            "research_benchmarking": research_benchmarking,
            "managerial_guidance_map": managerial_guidance_map,
            "self_evolution_actions": self_evolution_actions,
        }

    def _processing_channels(
        self,
        research: dict[str, Any] | None,
        guidance: dict[str, Any] | None,
        evolution: dict[str, Any] | None,
        network: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Summarise how each auto-dev channel consumes processing time."""

        def _channel_percent(value: float | None) -> float:
            return round(max(0.0, float(value or 0.0)), 2)

        research_percent = 0.0
        if research:
            research_percent = float(
                research.get(
                    "raw_utilization_percent",
                    research.get(
                        "latest_sample_percent",
                        research.get("utilization_percent", 0.0),
                    ),
                )
            )
        guidance_percent = 0.0
        if guidance and "processing_utilization_percent" in guidance:
            guidance_percent = float(guidance["processing_utilization_percent"])
        evolution_percent = 0.0
        if evolution and "processing_utilization_percent" in evolution:
            evolution_percent = float(evolution["processing_utilization_percent"])
        network_percent = 0.0
        if network and "processing_utilization_percent" in network:
            network_percent = float(network["processing_utilization_percent"])
        channels = {
            "research": _channel_percent(research_percent),
            "guidance": _channel_percent(guidance_percent),
            "evolution": _channel_percent(evolution_percent),
            "network": _channel_percent(network_percent),
        }
        total = round(sum(channels.values()), 2)
        primary = max(channels.items(), key=lambda item: item[1])[0] if total else "research"
        return {
            "channels": channels,
            "total": total,
            "primary": primary,
        }

    def _orchestration_pipeline(
        self,
        monsters: Sequence[dict[str, Any]] | None,
        spawn_plan: dict[str, Any] | None,
        mob_ai: dict[str, Any] | None,
        boss_plan: dict[str, Any] | None,
        quests: Sequence[dict[str, Any]] | None,
        research: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Describe the readiness of each orchestration stage."""

        monsters = list(monsters or [])
        spawn_plan = dict(spawn_plan or {})
        directives = list((mob_ai or {}).get("directives", []) or [])
        quests = list(quests or [])

        def stage(
            name: str,
            ready: bool,
            *,
            count: float = 0.0,
            dependencies: Sequence[str] | None = None,
            blockers: Sequence[str] | None = None,
        ) -> dict[str, Any]:
            status = "ready" if ready else "pending"
            deps = tuple(dependencies or ())
            outstanding = tuple(blockers or ())
            return {
                "name": name,
                "status": status,
                "throughput": round(max(0.0, float(count)), 2),
                "dependencies": deps,
                "blockers": outstanding,
            }

        stages: list[dict[str, Any]] = []
        stages.append(
            stage(
                "monster_design",
                bool(monsters),
                count=len(monsters),
                blockers=("Await monster roster",) if not monsters else None,
            )
        )
        group_count = float(spawn_plan.get("group_count", 0.0))
        stages.append(
            stage(
                "group_spawning",
                group_count > 0,
                count=group_count,
                dependencies=("monster_design",),
                blockers=("Populate spawn lanes",) if group_count <= 0 else None,
            )
        )
        stages.append(
            stage(
                "mob_ai",
                bool(directives),
                count=len(directives),
                dependencies=("monster_design", "group_spawning"),
                blockers=("Draft behaviour directives",) if not directives else None,
            )
        )
        stages.append(
            stage(
                "boss_selection",
                bool(boss_plan),
                count=1.0 if boss_plan else 0.0,
                dependencies=("mob_ai",),
                blockers=("Pick boss candidate",) if not boss_plan else None,
            )
        )
        stages.append(
            stage(
                "quest_generation",
                bool(quests),
                count=len(quests),
                dependencies=("boss_selection",),
                blockers=("Draft quest hooks",) if not quests else None,
            )
        )
        research_ready = bool(research)
        research_percent = 0.0
        if research_ready:
            research_percent = float(
                research.get(
                    "raw_utilization_percent",
                    research.get(
                        "latest_sample_percent",
                        research.get("utilization_percent", 0.0),
                    ),
                )
            )
        stages.append(
            stage(
                "research_intelligence",
                research_ready,
                count=research_percent,
                dependencies=("quest_generation",),
                blockers=("Capture utilisation sample",) if not research_ready else None,
            )
        )
        ready_count = sum(1 for stage_info in stages if stage_info["status"] == "ready")
        ratio = ready_count / len(stages)
        next_focus = "stabilise"
        for stage_info in stages:
            if stage_info["status"] != "ready":
                next_focus = stage_info["name"]
                break
        return {
            "stages": tuple(stages),
            "complete": ready_count == len(stages),
            "ready_ratio": round(ratio, 2),
            "next_focus": next_focus,
        }

    def _management_playbook(
        self,
        backend_guidance: dict[str, Any] | None,
        pipeline: dict[str, Any],
        percent: float,
        raw_percent: float,
        network: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Translate backend guidance and pipeline state into actions."""

        backend_guidance = backend_guidance or {}
        actions = list(backend_guidance.get("action_items", ()))
        network_actions = list((network or {}).get("recommendations", ()))
        next_focus = pipeline.get("next_focus", "stabilise")
        if next_focus != "stabilise":
            actions.append(f"Unblock {next_focus.replace('_', ' ')} stage")
        actions.extend(network_actions)
        compute_posture = "balanced"
        if percent >= self.utilisation_ceiling + 20.0:
            compute_posture = "shed_load"
        elif percent >= self.utilisation_ceiling:
            compute_posture = "guard_bandwidth"
        elif percent <= max(5.0, self.utilisation_ceiling * 0.25):
            compute_posture = "expand_scope"
        unique_actions: list[str] = []
        seen: set[str] = set()
        for action in actions:
            if action not in seen:
                unique_actions.append(action)
                seen.add(action)
        return {
            "priority": backend_guidance.get("priority", "balanced"),
            "actions": tuple(unique_actions),
            "compute_posture": compute_posture,
            "pipeline_focus": next_focus,
            "stability_index": pipeline.get("ready_ratio", 0.0),
            "raw_utilization": round(raw_percent, 2),
        }

    def _processing_percent(
        self,
        research: dict[str, Any] | None,
        guidance: dict[str, Any] | None,
        evolution: dict[str, Any] | None,
        network: dict[str, Any] | None,
    ) -> float:
        if research:
            if "raw_utilization_percent" in research:
                return float(research["raw_utilization_percent"])
            if "latest_sample_percent" in research:
                return float(research["latest_sample_percent"])
            if "utilization_percent" in research:
                return float(research["utilization_percent"])
        if guidance and "processing_utilization_percent" in guidance:
            return float(guidance["processing_utilization_percent"])
        if evolution and "processing_utilization_percent" in evolution:
            return float(evolution["processing_utilization_percent"])
        if network and "processing_utilization_percent" in network:
            return float(network["processing_utilization_percent"])
        return 0.0

    def _raw_processing_percent(
        self,
        research: dict[str, Any] | None,
        guidance: dict[str, Any] | None,
        evolution: dict[str, Any] | None,
        network: dict[str, Any] | None,
    ) -> float:
        if research and "raw_utilization_percent" in research:
            return float(research["raw_utilization_percent"])
        if guidance and "processing_utilization_percent" in guidance:
            return float(guidance["processing_utilization_percent"])
        if evolution and "processing_utilization_percent" in evolution:
            return float(evolution["processing_utilization_percent"])
        if network and "raw_processing_percent" in network:
            return float(network["raw_processing_percent"])
        if network and "processing_utilization_percent" in network:
            return float(network["processing_utilization_percent"])
        return 0.0

    def _load_state(self, percent: float) -> str:
        if percent >= self.utilisation_ceiling + 20.0:
            return "critical"
        if percent >= self.utilisation_ceiling:
            return "saturated"
        if percent >= max(10.0, self.utilisation_ceiling * 0.5):
            return "elevated"
        return "balanced"

    def _resource_recommendation(self, load_state: str, percent: float) -> str:
        if load_state == "critical":
            return "Immediately throttle research and free compute budget"
        if load_state == "saturated":
            return "Shift background studies onto slower cadences"
        if load_state == "elevated":
            return "Maintain sampling but monitor utilisation spikes"
        if percent <= 5.0:
            return "Increase sampling to gather competitive insights"
        return "Research allocation is balanced"

    def _encounter_alignment(
        self,
        monsters: Sequence[dict[str, Any]] | None,
        spawn_plan: dict[str, Any] | None,
        mob_ai: dict[str, Any] | None,
        boss_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        hazards = sorted({str(m.get("hazard", "general")) for m in monsters or ()})
        spawn_danger = float((spawn_plan or {}).get("danger", 1.0))
        coordination = "opportunistic"
        if mob_ai and mob_ai.get("directives"):
            coordination = "coordinated"
        boss_name = (boss_plan or {}).get("name", "unassigned")
        return {
            "hazards": hazards,
            "spawn_danger": round(spawn_danger, 2),
            "coordination": coordination,
            "boss": boss_name,
        }

    def _quest_alignment(
        self, quests: Sequence[dict[str, Any]] | None
    ) -> dict[str, Any]:
        quests = list(quests or [])
        trade_skills = sorted(
            {str(q.get("trade_skill", "General")) for q in quests if q.get("trade_skill")}
        )
        return {
            "quest_count": len(quests),
            "trade_skills": trade_skills,
        }

    def _encounter_blueprint(
        self,
        monsters: Sequence[dict[str, Any]] | None,
        spawn_plan: dict[str, Any] | None,
        mob_ai: dict[str, Any] | None,
        boss_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        monsters = list(monsters or [])
        spawn_plan = spawn_plan or {}
        if not monsters:
            return {}
        hazards = sorted({str(monster.get("hazard", "general")) for monster in monsters})
        groups = list(spawn_plan.get("groups", ()))
        average_group_size = 0.0
        if groups:
            total_size = sum(int(group.get("size", 0)) for group in groups)
            average_group_size = round(total_size / len(groups), 2)
        behaviours = []
        for directive in list((mob_ai or {}).get("directives", ())):
            behaviour = directive.get("behaviour")
            if behaviour:
                behaviours.append(str(behaviour))
        boss_hazard = str((boss_plan or {}).get("hazard", "")).lower()
        boss_synergy = bool(boss_hazard and boss_hazard in {h.lower() for h in hazards})
        return {
            "hazards": hazards,
            "group_count": int(spawn_plan.get("group_count", len(groups))),
            "average_group_size": average_group_size,
            "behaviours": _as_tuple(behaviours),
            "boss_synergy": boss_synergy,
        }

    def _quest_synergy(
        self,
        quests: Sequence[dict[str, Any]] | None,
        boss_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        quests = list(quests or [])
        if not quests:
            return {}
        trade_skills = sorted(
            {str(q.get("trade_skill", "General")) for q in quests if q.get("trade_skill")}
        )
        boss_name = str((boss_plan or {}).get("name", ""))
        supports_boss = any(
            boss_name and boss_name.lower() in str(q.get("objective", "")).lower()
            or ("challenge" in str(q.get("title", "")).lower())
            for q in quests
        )
        if not supports_boss:
            boss_hazard = str((boss_plan or {}).get("hazard", "")).lower()
            supports_boss = any(
                boss_hazard
                and boss_hazard in str(q.get("title", "")).lower()
                or boss_hazard in str(q.get("objective", "")).lower()
                for q in quests
            )
        if not supports_boss and boss_plan and trade_skills:
            supports_boss = True
        coverage_ratio = 0.0
        if quests:
            coverage_ratio = round(len(trade_skills) / len(quests), 2)
        return {
            "quests": len(quests),
            "trade_skill_focus": trade_skills,
            "boss_supporting_quest": supports_boss,
            "coverage_ratio": coverage_ratio,
        }

    def _monster_catalog(
        self, monsters: Sequence[dict[str, Any]] | None
    ) -> dict[str, Any]:
        monsters = list(monsters or [])
        if not monsters:
            return {}
        hazards = sorted(
            {str(monster.get("hazard", "")).lower() for monster in monsters if monster}
        )
        threats = [float(monster.get("threat", 1.0)) for monster in monsters]
        average_threat = round(sum(threats) / len(threats), 2) if threats else 0.0
        elite_count = sum(1 for monster in monsters if monster.get("elite"))
        roles = sorted(
            {str(monster.get("role", "vanguard")) for monster in monsters if monster}
        )
        ai_focuses = sorted(
            {str(monster.get("ai_focus", "adaptive")) for monster in monsters if monster}
        )
        spawn_synergies = sorted(
            {str(monster.get("spawn_synergy", "skirmish")) for monster in monsters if monster}
        )
        return {
            "count": len(monsters),
            "hazards": [hazard for hazard in hazards if hazard],
            "average_threat": average_threat,
            "elite_count": elite_count,
            "roles": _as_tuple(roles),
            "ai_focuses": _as_tuple(ai_focuses),
            "spawn_synergies": _as_tuple(spawn_synergies),
        }

    def _monster_creation(
        self, monsters: Sequence[dict[str, Any]] | None
    ) -> dict[str, Any]:
        monsters = list(monsters or [])
        if not monsters:
            return {}
        archetypes = {}
        hazards = set()
        top_threat = None
        for monster in monsters:
            if not monster:
                continue
            role = str(monster.get("role", "general"))
            archetypes[role] = archetypes.get(role, 0) + 1
            hazard = str(monster.get("hazard", ""))
            if hazard:
                hazards.add(hazard)
            threat = float(monster.get("threat", 1.0))
            if top_threat is None or threat > top_threat[1]:
                top_threat = (monster.get("name", role), threat)
        ai_focuses = sorted(
            {str(monster.get("ai_focus", "adaptive")) for monster in monsters if monster}
        )
        spawn_synergies = sorted(
            {
                str(monster.get("spawn_synergy", "skirmish"))
                for monster in monsters
                if monster
            }
        )
        creation_load = "stable"
        if len(monsters) >= 5:
            creation_load = "surging"
        elif len(monsters) >= 3:
            creation_load = "active"
        return {
            "archetype_counts": {
                key: value for key, value in sorted(archetypes.items())
            },
            "hazards": _as_tuple(sorted(hazards)),
            "peak_threat": round(top_threat[1], 2) if top_threat else 0.0,
            "headline_monster": top_threat[0] if top_threat else None,
            "creation_load": creation_load,
            "ai_focuses": tuple(ai_focuses),
            "spawn_synergies": tuple(spawn_synergies),
        }

    def _spawn_overview(self, spawn_plan: dict[str, Any] | None) -> dict[str, Any]:
        spawn_plan = spawn_plan or {}
        groups = list(spawn_plan.get("groups", ()))
        if not spawn_plan and not groups:
            return {}
        group_sizes = [int(group.get("size", 0)) for group in groups if group]
        group_size_total = sum(group_sizes)
        average_group_size = (
            round(group_size_total / len(group_sizes), 2) if group_sizes else 0.0
        )
        group_count = int(spawn_plan.get("group_count", len(groups))) or len(groups)
        interval = float(spawn_plan.get("interval", spawn_plan.get("cooldown", 0.0)))
        tempo = str(spawn_plan.get("tempo", "steady"))
        if tempo == "steady":
            if interval:
                if interval <= 5.0:
                    tempo = "rapid"
                elif interval >= 15.0:
                    tempo = "deliberate"
            elif group_count > 3:
                tempo = "rapid"
        formation = str(spawn_plan.get("formation", "staggered"))
        total_enemies = int(spawn_plan.get("total_enemies", group_size_total or group_count))
        lanes = spawn_plan.get("lanes")
        return {
            "group_count": group_count,
            "average_group_size": average_group_size,
            "total_enemies": total_enemies,
            "tempo": tempo,
            "lanes": _as_tuple(lanes or ()),
            "formation": formation,
        }

    def _spawn_tactics(self, spawn_plan: dict[str, Any] | None) -> dict[str, Any]:
        spawn_plan = spawn_plan or {}
        groups = list(spawn_plan.get("groups", ()))
        if not spawn_plan and not groups:
            return {}
        interval = float(spawn_plan.get("interval", spawn_plan.get("cooldown", 0.0)))
        lanes = [str(lane) for lane in spawn_plan.get("lanes", ()) if lane]
        largest_group = max(
            (int(group.get("size", 0)) for group in groups if group),
            default=0,
        )
        lane_pressure = {lane: 0 for lane in lanes}
        for group in groups:
            lane = str(group.get("entry_point", ""))
            if lane:
                lane_pressure[lane] = lane_pressure.get(lane, 0) + int(
                    group.get("size", 0)
                )
        anchor_lane = None
        if lane_pressure:
            anchor_lane = max(lane_pressure.items(), key=lambda item: item[1])[0]
        reinforcement = str(spawn_plan.get("formation", "staggered"))
        if reinforcement not in {"burst", "wave", "staggered", "onslaught", "incursion"}:
            if interval and interval <= 4.0:
                reinforcement = "burst"
            elif interval >= 12.0:
                reinforcement = "wave"
            else:
                reinforcement = "staggered"
        reinforcement_curve = tuple(
            float(value) for value in spawn_plan.get("reinforcement_curve", ())
        )
        return {
            "lanes": _as_tuple(sorted(lanes)),
            "largest_group_size": largest_group,
            "anchor_lane": anchor_lane,
            "reinforcement_style": reinforcement,
            "lane_pressure": {
                lane: pressure for lane, pressure in sorted(lane_pressure.items())
            },
            "reinforcement_curve": reinforcement_curve,
        }

    def _mob_ai_development(
        self, mob_ai: dict[str, Any] | None
    ) -> dict[str, Any]:
        mob_ai = mob_ai or {}
        directives = list(mob_ai.get("directives", ()))
        if not mob_ai and not directives:
            return {}
        behaviours = [
            str(directive.get("behaviour"))
            for directive in directives
            if directive.get("behaviour")
        ]
        hazard_focus = next(
            (
                str(directive.get("hazard"))
                for directive in directives
                if directive.get("hazard")
            ),
            None,
        )
        adaptive = bool(
            mob_ai.get("learning")
            or mob_ai.get("adaptive")
            or any(directive.get("adapts") for directive in directives)
        )
        training_modules = tuple(mob_ai.get("training_modules", ()))
        ai_focuses = tuple(
            str(directive.get("ai_focus", "adaptive"))
            for directive in directives
            if directive.get("ai_focus")
        )
        coordination = "opportunistic"
        if len(directives) >= 3:
            coordination = "coordinated"
        if mob_ai.get("squads"):
            coordination = "squad-based"
        return {
            "directive_count": len(directives),
            "behaviours": _as_tuple(behaviours[:4]),
            "hazard_focus": hazard_focus,
            "adaptive": adaptive,
            "coordination": coordination,
            "training_modules": training_modules,
            "ai_focuses": ai_focuses,
        }

    def _ai_development_plan(
        self,
        mob_ai: dict[str, Any] | None,
        monsters: Sequence[dict[str, Any]] | None,
        spawn_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        mob_ai = mob_ai or {}
        monsters = list(monsters or [])
        spawn_plan = spawn_plan or {}
        directives = list(mob_ai.get("directives", ()))
        if not mob_ai and not directives:
            return {}
        covered_hazards = {
            str(directive.get("hazard", "")).lower()
            for directive in directives
            if directive
        }
        monster_hazards = {
            str(monster.get("hazard", "")).lower()
            for monster in monsters
            if monster
        }
        uncovered = sorted(h for h in monster_hazards if h and h not in covered_hazards)
        escalation = float(spawn_plan.get("danger", 1.0))
        iteration = "steady"
        if mob_ai.get("learning") or mob_ai.get("adaptive"):
            iteration = "continuous"
        if escalation >= 2.0:
            iteration = "accelerated"
        drills: list[str] = []
        for hazard in sorted(monster_hazards)[:3]:
            drills.append(f"Simulate {hazard} counterplays")
        if uncovered:
            drills.insert(0, f"Develop coverage for {uncovered[0]}")
        return {
            "iteration_mode": iteration,
            "hazards_covered": _as_tuple(sorted(covered_hazards)),
            "hazards_uncovered": _as_tuple(uncovered),
            "training_drills": _as_tuple(drills[:4]),
            "escalation_index": round(escalation, 2),
        }

    def _boss_outlook(
        self,
        boss_plan: dict[str, Any] | None,
        spawn_plan: dict[str, Any] | None,
        quests: Sequence[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        if not boss_plan:
            return {}
        hazard = str(boss_plan.get("hazard", "")).lower()
        threat = float(boss_plan.get("threat", 1.0))
        spawn_danger = float((spawn_plan or {}).get("danger", 1.0))
        quests = list(quests or [])
        supporting_quests = [
            q
            for q in quests
            if hazard
            and hazard in str(q.get("objective", "")).lower()
            or boss_plan.get("name", "").lower()
            in str(q.get("title", "")).lower()
        ]
        recommendation = "Stage support buffs"
        if spawn_danger >= 2.0 or threat >= 2.0:
            recommendation = "Schedule coordinated raids"
        elif spawn_danger <= 1.0 and threat < 1.2:
            recommendation = "Allow flexible party sizes"
        return {
            "name": boss_plan.get("name", "unassigned"),
            "hazard": hazard,
            "threat": round(threat, 2),
            "supporting_quests": len(supporting_quests),
            "recommendation": recommendation,
        }

    def _boss_spawn_strategy(
        self,
        boss_plan: dict[str, Any] | None,
        spawn_plan: dict[str, Any] | None,
        quests: Sequence[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        if not boss_plan:
            return {}
        spawn_plan = spawn_plan or {}
        quests = list(quests or [])
        interval = float(
            boss_plan.get(
                "spawn_interval",
                spawn_plan.get("boss_interval", spawn_plan.get("interval", 0.0)),
            )
        )
        lanes = [str(lane) for lane in spawn_plan.get("lanes", ()) if lane]
        rally_support = sum(
            1
            for quest in quests
            if str(boss_plan.get("name", "")).lower()
            in str(quest.get("objective", "")).lower()
        )
        prep_window = "standard"
        if interval and interval <= 6.0:
            prep_window = "short"
        elif interval >= 15.0:
            prep_window = "extended"
        reinforcement = "solo"
        if rally_support >= 3:
            reinforcement = "raid"
        elif rally_support == 2:
            reinforcement = "party"
        base_strategies = [
            str(strategy)
            for strategy in boss_plan.get("strategies", ())
            if str(strategy).strip()
        ]
        if not base_strategies:
            threat_score = float(boss_plan.get("threat", 1.0))
            if lanes:
                if len(lanes) > 1:
                    base_strategies.append("coordinate_lanes")
                else:
                    base_strategies.append("fortify_lane")
            if reinforcement == "raid":
                base_strategies.append("sustain_raid_pressure")
            elif reinforcement == "party":
                base_strategies.append("coordinate_parties")
            else:
                base_strategies.append("solo_opportunity")
            if prep_window == "extended":
                base_strategies.append("schedule_training")
            elif prep_window == "short":
                base_strategies.append("rapid_response")
            if threat_score >= 2.0:
                base_strategies.append("bolster_defenses")
            elif threat_score <= 1.2:
                base_strategies.append("exploit_openings")
            if not base_strategies:
                base_strategies.append("monitor_signals")
        strategies = list(dict.fromkeys(base_strategies))
        return {
            "interval": round(interval, 2),
            "lanes": _as_tuple(lanes),
            "supporting_quests": rally_support,
            "recommended_group": reinforcement,
            "preparation_window": prep_window,
            "strategies": _as_tuple(strategies),
            "threat": float(boss_plan.get("threat", 1.0)),
        }

    def _quest_matrix(
        self,
        quests: Sequence[dict[str, Any]] | None,
        boss_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        quests = list(quests or [])
        if not quests:
            return {}
        skill_counts: dict[str, int] = {}
        difficulty_counts: dict[str, int] = {}
        for quest in quests:
            skill = str(quest.get("trade_skill", "General"))
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
            difficulty = str(quest.get("difficulty", "standard"))
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
        boss_hazard = str((boss_plan or {}).get("hazard", "")).lower()
        aligned_skills = [
            skill
            for skill, count in skill_counts.items()
            if boss_hazard and boss_hazard in skill.lower()
            or skill.lower() in {"combat", "defense"}
        ]
        return {
            "skills": {skill: count for skill, count in sorted(skill_counts.items())},
            "aligned_skills": _as_tuple(sorted(set(aligned_skills))),
            "quest_total": len(quests),
            "difficulty_breakdown": {k: difficulty_counts.get(k, 0) for k in sorted(difficulty_counts)},
        }

    def _quest_generation(
        self,
        quests: Sequence[dict[str, Any]] | None,
        boss_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        quests = list(quests or [])
        if not quests:
            return {}
        boss_name = str((boss_plan or {}).get("name", ""))
        trade_skills = [str(quest.get("trade_skill", "General")) for quest in quests]
        distinct_skills = sorted({skill for skill in trade_skills if skill})
        boss_hooks = sum(
            1
            for quest in quests
            if quest.get("supports_boss")
            or (
                boss_name
                and boss_name.lower() in str(quest.get("objective", "")).lower()
            )
        )
        cadence = "rotational"
        if len(quests) >= 6:
            cadence = "seasonal"
        elif len(quests) <= 2:
            cadence = "focused"
        difficulty_counts: dict[str, int] = {}
        tag_set: set[str] = set()
        for quest in quests:
            difficulty = str(quest.get("difficulty", "standard"))
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
            tag_set.update(str(tag) for tag in quest.get("tags", ()))
        return {
            "quests_available": len(quests),
            "skills_supported": _as_tuple(distinct_skills),
            "boss_hooks": boss_hooks,
            "cadence": cadence,
            "difficulty_breakdown": {k: difficulty_counts.get(k, 0) for k in sorted(difficulty_counts)},
            "tags": _as_tuple(sorted(tag_set)),
        }

    def _group_mechanics(
        self,
        monsters: Sequence[dict[str, Any]] | None,
        spawn_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        spawn_plan = spawn_plan or {}
        groups = [group for group in spawn_plan.get("groups", ()) if group]
        if not groups:
            return {}
        intervals = [
            float(group.get("spawn_interval", spawn_plan.get("interval", 0.0)))
            for group in groups
        ]
        sizes = [int(group.get("size", 0)) for group in groups]
        total_enemies = sum(sizes)
        average_interval = round(sum(intervals) / len(intervals), 2) if intervals else 0.0
        peak_size = max(sizes) if sizes else 0
        burstiness = round((peak_size / max(1, total_enemies)), 2) if total_enemies else 0.0
        lane_counts: dict[str, int] = {}
        synergies: dict[str, int] = {}
        for group in groups:
            lane = str(group.get("entry_point", "unknown"))
            lane_counts[lane] = lane_counts.get(lane, 0) + 1
            synergy = str(group.get("synergy", "skirmish"))
            synergies[synergy] = synergies.get(synergy, 0) + int(group.get("size", 0))
        hazard_focus = sorted(
            {
                str(monster.get("hazard", "general"))
                for monster in monsters or ()
                if monster
            }
        )
        tempo = "steady"
        if average_interval and average_interval <= 5.0:
            tempo = "aggressive"
        elif average_interval >= 12.0:
            tempo = "measured"
        formation = str(spawn_plan.get("formation", "staggered"))
        return {
            "lanes": tuple({"lane": lane, "groups": count} for lane, count in sorted(lane_counts.items())),
            "average_interval": average_interval,
            "total_enemies": total_enemies,
            "peak_group_size": peak_size,
            "burstiness": burstiness,
            "tempo": tempo,
            "hazard_focus": _as_tuple(hazard_focus),
            "synergy_breakdown": {k: synergies.get(k, 0) for k in sorted(synergies)},
            "formation": formation,
        }

    def _mob_ai_training(
        self,
        mob_ai: dict[str, Any] | None,
        monsters: Sequence[dict[str, Any]] | None,
        spawn_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        if not mob_ai:
            return {}
        directives = list(mob_ai.get("directives", ()))
        if not directives:
            return {}
        hazards_supported = {
            str(directive.get("hazard", "general")) for directive in directives if directive
        }
        monster_hazards = {
            str(monster.get("hazard", "general")) for monster in monsters or () if monster
        }
        missing_hazards = sorted(hazard for hazard in monster_hazards if hazard not in hazards_supported)
        behaviours = [str(directive.get("behaviour")) for directive in directives if directive.get("behaviour")]
        training_focus: list[str] = []
        if missing_hazards:
            training_focus.append(
                f"Author new behaviours for {', '.join(missing_hazards)} cohorts"
            )
        spawn_pressure = float((spawn_plan or {}).get("danger", 1.0))
        if spawn_pressure >= 2.0:
            training_focus.append("Drill high pressure response rotations")
        elif spawn_pressure <= 0.8:
            training_focus.append("Reduce aggression for patrol duties")
        coordination_window = float(
            mob_ai.get("coordination_window", max(8.0, 12.0 / max(0.75, spawn_pressure)))
        )
        modules = tuple(mob_ai.get("training_modules", ()))
        return {
            "behaviours": _as_tuple(behaviours),
            "hazards_supported": _as_tuple(sorted(hazards_supported)),
            "gaps": _as_tuple(missing_hazards),
            "coordination_window": round(coordination_window, 2),
            "training_focus": _as_tuple(training_focus),
            "training_modules": modules,
        }

    def _boss_pressure(
        self,
        boss_plan: dict[str, Any] | None,
        spawn_plan: dict[str, Any] | None,
        monsters: Sequence[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        if not boss_plan:
            return {}
        spawn_danger = float((spawn_plan or {}).get("danger", 1.0))
        hazard = str(boss_plan.get("hazard", "general"))
        supporting_monsters = [
            monster
            for monster in monsters or ()
            if monster and str(monster.get("hazard", "")).lower() == hazard.lower()
        ]
        reinforcement_ratio = round(
            len(supporting_monsters) / max(1, len(monsters or [])), 2
        )
        pressure_rating = "manageable"
        threat = float(boss_plan.get("threat", 1.0))
        if threat >= 1.8 or spawn_danger >= 2.5:
            pressure_rating = "overwhelming"
        elif threat >= 1.3 or spawn_danger >= 1.8:
            pressure_rating = "intense"
        return {
            "hazard": hazard,
            "threat": round(threat, 2),
            "spawn_pressure": round(spawn_danger, 2),
            "supporting_monster_ratio": reinforcement_ratio,
            "pressure_rating": pressure_rating,
        }

    def _quest_dependency(
        self,
        quests: Sequence[dict[str, Any]] | None,
        boss_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        quests = list(quests or [])
        if not quests:
            return {}
        boss_name = str((boss_plan or {}).get("name", ""))
        dependency: dict[str, list[str]] = {}
        for quest in quests:
            skill = str(quest.get("trade_skill", "General"))
            objective = str(quest.get("objective", ""))
            dependency.setdefault(skill, []).append(objective)
        linked_skills = [
            skill
            for skill, objectives in dependency.items()
            if any(boss_name and boss_name.lower() in objective.lower() for objective in objectives)
        ]
        return {
            "skills": {skill: tuple(objectives) for skill, objectives in dependency.items()},
            "boss_linked_skills": _as_tuple(sorted(set(linked_skills))),
        }

    def _processing_overview(
        self, percent: float, raw_percent: float, research_view: dict[str, Any]
    ) -> dict[str, Any]:
        if not research_view:
            return {
                "current_percent": round(percent, 2),
                "raw_percent": round(raw_percent, 2),
            }
        breakdown = {
            "current_percent": round(percent, 2),
            "raw_percent": round(raw_percent, 2),
            "average_percent": research_view.get("average_percent"),
            "samples": research_view.get("samples"),
            "primary_source": research_view.get("primary_source"),
        }
        if research_view.get("recent_samples"):
            breakdown["recent_samples"] = research_view["recent_samples"]
        return breakdown

    def _evolution_alignment(
        self,
        guidance: dict[str, Any] | None,
        evolution: dict[str, Any] | None,
    ) -> dict[str, Any]:
        if not guidance and not evolution:
            return {}
        guidance_priority = (guidance or {}).get("priority", "undetermined")
        evolution_summary = (evolution or {}).get("summary")
        objectives = list((evolution or {}).get("next_objectives", ()))
        directives = list((guidance or {}).get("directives", ()))
        overlaps = [
            directive
            for directive in directives
            if any(str(objective) in str(directive) for objective in objectives)
        ]
        return {
            "guidance_priority": guidance_priority,
            "evolution_summary": evolution_summary,
            "objective_overlap": _as_tuple(overlaps),
            "next_objectives": _as_tuple(objectives[:3]),
        }

    def _research_view(self, research: dict[str, Any] | None) -> dict[str, Any]:
        if not research:
            return {}
        raw_percent = float(research.get("raw_utilization_percent", 0.0))
        latest = float(research.get("latest_sample_percent", raw_percent))
        average = float(research.get("utilization_percent", latest))
        samples = int(research.get("samples", 0))
        primary_source = research.get("primary_source")
        intelligence_focus = research.get("intelligence_focus")
        return {
            "raw_percent": round(raw_percent, 2),
            "latest_percent": round(latest, 2),
            "average_percent": round(average, 2),
            "samples": samples,
            "primary_source": primary_source,
            "recent_samples": tuple(research.get("raw_samples", ()))[:5],
            "intelligence_focus": intelligence_focus,
        }

    def _backend_guidance(
        self,
        guidance: dict[str, Any] | None,
        evolution: dict[str, Any] | None,
        research_view: dict[str, Any],
    ) -> dict[str, Any]:
        if not guidance and not evolution and not research_view:
            return {}
        priority = (guidance or {}).get("priority", "undetermined")
        research_pressure = research_view.get("raw_percent", 0.0)
        summary = (evolution or {}).get("summary")
        next_objectives = list((evolution or {}).get("next_objectives", ()))
        action_items: list[str] = []
        directives = list((guidance or {}).get("directives", ()))
        if directives:
            action_items.append(str(directives[0]))
        for objective in next_objectives:
            action_items.append(str(objective))
            if len(action_items) >= 3:
                break
        trade_focus = research_view.get("intelligence_focus")
        summary_focus = str((guidance or {}).get("summary", ""))
        if summary_focus and summary_focus not in action_items:
            action_items.append(summary_focus)
        return {
            "priority": str(priority),
            "research_pressure": round(float(research_pressure), 2),
            "evolution_summary": summary,
            "next_objectives": _as_tuple(next_objectives[:3]),
            "action_items": _as_tuple(action_items),
            "trade_focus": trade_focus,
            "directive_count": len(directives),
        }

    def _competitive_analysis(self, research: dict[str, Any] | None) -> dict[str, Any]:
        if not research:
            return {"raw_percent": 0.0, "primary_game": None, "games": {}}
        competitive = research.get("competitive_research") or {}
        games = {
            str(game): round(float(percent), 2)
            for game, percent in (competitive.get("games") or {}).items()
        }
        raw_percent = round(float(competitive.get("raw_percent", 0.0)), 2)
        primary = competitive.get("primary_game")
        return {
            "raw_percent": raw_percent,
            "primary_game": primary,
            "games": games,
        }

    def _group_spawn_coordination(
        self,
        monsters: Sequence[dict[str, Any]] | None,
        spawn_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        plan = spawn_plan or {}
        groups = list(plan.get("groups", ()))
        lanes = tuple(plan.get("lanes", ()))
        interval = float(plan.get("interval", 0.0) or 0.0)
        group_count = len(groups)
        lane_count = len(lanes) or 1
        total_units = sum(int(group.get("size", 0) or 0) for group in groups)
        hazard_roles = {
            str(monster.get("role", "general"))
            for monster in monsters or ()
            if monster and monster.get("role")
        }
        cadence = "staggered"
        if interval <= 4.0:
            cadence = "burst"
        elif interval >= 10.0:
            cadence = "glacial"
        coordination_score = round(
            min(1.0, (group_count + lane_count + (total_units / max(1, group_count or 1))) / 12.0),
            2,
        )
        return {
            "group_count": group_count,
            "lane_count": len(lanes),
            "spawn_interval": round(interval, 2),
            "cadence": cadence,
            "total_units": total_units,
            "roles": _as_tuple(sorted(hazard_roles)) if hazard_roles else (),
            "coordination_score": coordination_score,
        }

    def _ai_innovation_focus(
        self,
        mob_ai: dict[str, Any] | None,
        monsters: Sequence[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        directives = list((mob_ai or {}).get("directives", ()))
        if not directives:
            return {}
        behaviours = {
            str(directive.get("behaviour", ""))
            for directive in directives
            if directive.get("behaviour")
        }
        hazards = {
            str(directive.get("hazard", ""))
            for directive in directives
            if directive.get("hazard")
        }
        monster_roles = {
            str(monster.get("role", ""))
            for monster in monsters or ()
            if monster and monster.get("role")
        }
        covered_roles = {
            str(directive.get("role", "")).lower()
            for directive in directives
            if directive.get("role")
        }
        role_gap = any(
            role.lower() not in covered_roles and role
            for role in monster_roles
        )
        adaptive = any(bool(directive.get("adapts")) for directive in directives)
        return {
            "directive_count": len(directives),
            "behaviours": _as_tuple(sorted(behaviours)),
            "hazards": _as_tuple(sorted(hazards)),
            "requires_support_roles": role_gap,
            "adaptive_learning": adaptive,
        }

    def _boss_spawn_readiness(
        self,
        boss_plan: dict[str, Any] | None,
        spawn_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        if not boss_plan:
            return {}
        hazard = str(boss_plan.get("hazard", ""))
        threat = float(boss_plan.get("threat", 1.0))
        interval = float((spawn_plan or {}).get("interval", 0.0) or 0.0)
        danger = float((spawn_plan or {}).get("danger", 1.0))
        readiness = "queued"
        if danger >= 2.0 or threat >= 1.8:
            readiness = "escalating"
        elif danger <= 1.0 and threat <= 1.1:
            readiness = "stable"
        return {
            "hazard": hazard,
            "threat": round(threat, 2),
            "spawn_interval": round(interval, 2),
            "danger": round(danger, 2),
            "readiness": readiness,
        }

    def _quest_trade_skill_alignment(
        self,
        quests: Sequence[dict[str, Any]] | None,
        boss_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        quests = list(quests or [])
        if not quests:
            return {}
        boss_hazard = str((boss_plan or {}).get("hazard", ""))
        boss_name = str((boss_plan or {}).get("name", ""))
        skills: Dict[str, int] = {}
        boss_support = []
        for quest in quests:
            skill = str(quest.get("trade_skill", "General"))
            skills[skill] = skills.get(skill, 0) + 1
            if boss_name and boss_name.lower() in str(quest.get("objective", "")).lower():
                boss_support.append(skill)
        return {
            "skills": skills,
            "boss_support_skills": _as_tuple(sorted(set(boss_support))),
            "boss_hazard": boss_hazard or None,
        }

    def _network_health(self, network: dict[str, Any] | None) -> dict[str, Any]:
        if not network:
            return {
                "status": "unknown",
                "score": 0.0,
                "average_latency_ms": None,
            }
        latency = (network.get("latency") or {}).get("average_ms")
        health = network.get("network_health") or {}
        return {
            "status": health.get("status", "unknown"),
            "score": round(float(health.get("score", 0.0)), 2),
            "average_latency_ms": round(float(latency), 2) if latency is not None else None,
        }

    def _network_security(self, network: dict[str, Any] | None) -> dict[str, Any]:
        if not network:
            return {"risk": "low", "incidents": 0, "focus": ()}
        security = network.get("security") or {}
        focus = security.get("focus") or ()
        return {
            "risk": security.get("risk", "low"),
            "incidents": int(security.get("incidents", 0)),
            "focus": _as_tuple(focus),
        }

    def _network_upgrade_plan(self, network: dict[str, Any] | None) -> dict[str, Any]:
        if not network:
            return {"recommendations": (), "needs_redundancy": False, "relays": 0}
        relay_plan = network.get("relay_plan") or {}
        return {
            "recommendations": _as_tuple(network.get("recommendations", ())),
            "needs_redundancy": bool(relay_plan.get("needs_redundancy")),
            "relays": int(relay_plan.get("relays", 0)),
        }

    def _network_processing(self, network: dict[str, Any] | None) -> dict[str, Any]:
        if not network:
            return {"processing_percent": 0.0, "raw_percent": 0.0}
        return {
            "processing_percent": round(
                float(network.get("processing_utilization_percent", 0.0)), 2
            ),
            "raw_percent": round(float(network.get("raw_processing_percent", 0.0)), 2),
        }

    def _network_security_automation(
        self, network: dict[str, Any] | None
    ) -> dict[str, Any]:
        automation = dict((network or {}).get("security_automation") or {})
        if not automation:
            return {
                "automation_score": 0.0,
                "playbooks": (),
                "recommended_controls": (),
                "automation_tiers": (),
            }
        score = float(automation.get("automation_score", 0.0))
        playbooks = automation.get("playbooks", ())
        controls = automation.get("recommended_controls", ())
        focus = automation.get("security_focus")
        return {
            "automation_score": round(score, 2),
            "playbooks": _as_tuple(playbooks),
            "recommended_controls": _as_tuple(controls),
            "automation_tiers": _as_tuple(automation.get("automation_tiers", ())),
            "focus": str(focus) if focus else "stabilise",
        }

    def _holographic_transmission(
        self, network: dict[str, Any] | None
    ) -> dict[str, Any]:
        holographic = dict((network or {}).get("holographic_channels") or {})
        if not holographic:
            return {
                "layer_count": 0,
                "anchor_quality": 0.0,
                "encrypted_channels": False,
                "spectral_load": 0.0,
                "channel_map": {},
            }
        return {
            "layer_count": int(holographic.get("layer_count", 0)),
            "anchor_quality": round(float(holographic.get("anchor_quality", 0.0)), 3),
            "encrypted_channels": bool(holographic.get("encrypted_channels", False)),
            "spectral_load": round(float(holographic.get("spectral_load", 0.0)), 3),
            "throughput_index": round(float(holographic.get("throughput_index", 0.0)), 2),
            "channel_map": dict(holographic.get("channel_map", {})),
            "triangulation_hint": holographic.get("triangulation_hint", {}),
        }

    def _network_verification_layers(
        self, network: dict[str, Any] | None
    ) -> dict[str, Any]:
        verification = dict((network or {}).get("verification_layers") or {})
        if not verification:
            return {
                "layers": 0,
                "integrity": "stable",
                "severity_focus": (),
                "anchor_quality": 0.0,
            }
        return {
            "layers": int(verification.get("layers", 0)),
            "integrity": verification.get("integrity", "stable"),
            "severity_focus": _as_tuple(verification.get("severity_focus", ())),
            "anchor_quality": round(float(verification.get("anchor_quality", 0.0)), 3),
            "incident_total": int(verification.get("incident_total", 0)),
        }

    def _managerial_overview(
        self,
        backend_guidance: dict[str, Any],
        evolution_alignment: dict[str, Any],
        processing_overview: dict[str, Any],
        group_coordination: dict[str, Any],
        competitive_research: dict[str, Any],
        network: dict[str, Any] | None,
    ) -> dict[str, Any]:
        coordination = group_coordination.get("coordination_score", 0.0)
        raw_percent = processing_overview.get("raw_percent", 0.0)
        research_pressure = backend_guidance.get("research_pressure", 0.0)
        network_health = (network or {}).get("network_health") or {}
        relay_plan = (network or {}).get("relay_plan") or {}
        security_auto = (network or {}).get("security_automation") or {}
        holographic = (network or {}).get("holographic_channels") or {}
        verification = (network or {}).get("verification_layers") or {}
        return {
            "coordination_score": coordination,
            "raw_processing_percent": raw_percent,
            "research_pressure": research_pressure,
            "competitive_focus": competitive_research.get("primary_game"),
            "next_objectives": _as_tuple(
                evolution_alignment.get("next_objectives", ())
            ),
            "network_status": network_health.get("status", "unknown"),
            "network_health_score": round(float(network_health.get("score", 0.0)), 2),
            "relay_needs": bool(relay_plan.get("needs_redundancy")),
            "security_automation_score": round(
                float(security_auto.get("automation_score", 0.0)), 2
            ),
            "holographic_anchor_quality": round(
                float(holographic.get("anchor_quality", 0.0)), 3
            ),
            "verification_layers": int(verification.get("layers", 0)),
        }

    def _monster_forge_detail(
        self,
        monsters: Sequence[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        monsters = list(monsters or [])
        if not monsters:
            return {
                "status": "idle",
                "count": 0,
                "hazards": (),
                "elite_ratio": 0.0,
            }
        hazards = sorted({str(monster.get("hazard", "")) for monster in monsters if monster.get("hazard")})
        elite_count = sum(1 for monster in monsters if monster.get("elite"))
        status = "stable"
        if len(monsters) >= 4 or elite_count >= 2:
            status = "surging"
        elif len(monsters) >= 2:
            status = "active"
        ratio = elite_count / max(1, len(monsters))
        return {
            "status": status,
            "count": len(monsters),
            "hazards": tuple(hazards),
            "elite_ratio": round(ratio, 2),
        }

    def _group_spawn_mechanics_detail(
        self,
        spawn_plan: dict[str, Any] | None,
        monsters: Sequence[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        spawn_plan = dict(spawn_plan or {})
        groups = spawn_plan.get("groups") or ()
        hazard_focus = sorted(
            {
                str(monster.get("hazard", ""))
                for monster in (monsters or [])
                if monster.get("hazard")
            }
        )
        pattern = "staggered"
        interval = float(spawn_plan.get("interval", 0.0) or 0.0)
        if spawn_plan.get("lanes"):
            pattern = "laned"
        if interval <= 4.0 and interval > 0.0:
            pattern = "burst"
        total_enemies = sum(int(group.get("size", 0)) for group in groups)
        return {
            "groups": int(spawn_plan.get("group_count", len(groups))),
            "pattern": pattern,
            "lanes": _as_tuple(spawn_plan.get("lanes", ())),
            "hazards": tuple(hazard_focus),
            "total_enemies": total_enemies,
        }

    def _mob_ai_innovation_plan(
        self,
        mob_ai: dict[str, Any] | None,
        spawn_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        directives = list((mob_ai or {}).get("directives", ()))
        hazards = sorted({str(directive.get("hazard", "")) for directive in directives if directive.get("hazard")})
        iteration_mode = "baseline"
        if (mob_ai or {}).get("learning"):
            iteration_mode = "continuous"
        if (mob_ai or {}).get("adaptive"):
            iteration_mode = "accelerated"
        coordination = "solo"
        if any(directive.get("behaviour") == "coordinated assaults" for directive in directives):
            coordination = "coordinated"
        elif len(directives) > 1:
            coordination = "squad"
        cadence = "standard"
        interval = float((spawn_plan or {}).get("interval", 0.0) or 0.0)
        if interval and interval < 5.0:
            cadence = "rapid"
        elif interval > 8.0:
            cadence = "extended"
        return {
            "directive_count": len(directives),
            "hazards_covered": tuple(hazards),
            "iteration_mode": iteration_mode,
            "coordination": coordination,
            "cadence": cadence,
        }

    def _boss_spawn_matrix_detail(
        self,
        boss_plan: dict[str, Any] | None,
        spawn_plan: dict[str, Any] | None,
        quests: Sequence[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        if not boss_plan:
            return {}
        strategy = self._boss_spawn_strategy(boss_plan, spawn_plan, quests)
        supporting = sum(
            1
            for quest in (quests or [])
            if boss_plan.get("name") and boss_plan.get("name").lower() in str(quest.get("objective", "")).lower()
        )
        return {
            "name": boss_plan.get("name"),
            "hazard": boss_plan.get("hazard"),
            "recommended_group": strategy.get("recommended_group"),
            "interval": strategy.get("interval"),
            "supporting_quests": supporting,
        }

    def _quest_tradecraft_detail(
        self,
        quests: Sequence[dict[str, Any]] | None,
        boss_plan: dict[str, Any] | None,
        spawn_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        quests = list(quests or [])
        if not quests:
            return {
                "skills": (),
                "boss_support": 0,
                "spawn_alignment": (),
            }
        skills = sorted({str(quest.get("trade_skill", "")) for quest in quests if quest.get("trade_skill")})
        boss_name = (boss_plan or {}).get("name")
        boss_support = 0
        for quest in quests:
            title = str(quest.get("title", ""))
            objective = str(quest.get("objective", ""))
            lower_title = title.lower()
            lower_objective = objective.lower()
            if boss_name and (
                boss_name.lower() in lower_title or boss_name.lower() in lower_objective
            ):
                boss_support += 1
                continue
            if "boss" in lower_title or "boss" in lower_objective:
                boss_support += 1
        spawn_hazards = []
        if spawn_plan and spawn_plan.get("lanes"):
            spawn_hazards.extend(spawn_plan.get("lanes", ()))
        hazard = (boss_plan or {}).get("hazard")
        if hazard:
            spawn_hazards.append(hazard)
        return {
            "skills": tuple(skills),
            "boss_support": boss_support,
            "spawn_alignment": _as_tuple(spawn_hazards),
        }

    def _research_pressure(
        self,
        research: dict[str, Any] | None,
    ) -> dict[str, Any]:
        if not research:
            return {
                "competitive_raw_percent": 0.0,
                "competitive_share_percent": 0.0,
            }
        raw_percent = float(research.get("competitive_raw_percent", 0.0))
        share = float(research.get("competitive_share_percent", 0.0))
        latest = float(research.get("raw_utilization_percent", research.get("latest_sample_percent", 0.0)))
        return {
            "competitive_raw_percent": round(raw_percent, 2),
            "competitive_share_percent": round(share, 2),
            "latest_sample_percent": round(latest, 2),
        }

    def _managerial_alignment(
        self,
        backend_guidance: dict[str, Any] | None,
        management_playbook: dict[str, Any] | None,
        monster_forge: dict[str, Any],
        group_spawn_mechanics_detail: dict[str, Any],
    ) -> dict[str, Any]:
        backend_priority = None
        if backend_guidance:
            backend_priority = backend_guidance.get("priority")
        pipeline_focus = None
        if management_playbook:
            pipeline_focus = management_playbook.get("pipeline_focus")
        status = monster_forge.get("status")
        spawn_pattern = group_spawn_mechanics_detail.get("pattern")
        alignment = "balanced"
        if backend_priority and pipeline_focus and backend_priority != pipeline_focus:
            alignment = "divergent"
        elif backend_priority and status == "surging":
            alignment = "escalating"
        return {
            "backend_priority": backend_priority,
            "pipeline_focus": pipeline_focus,
            "monster_status": status,
            "spawn_pattern": spawn_pattern,
            "alignment": alignment,
        }

    def _competitive_pressure(
        self,
        research: dict[str, Any] | None,
        processed_percent: float,
        raw_percent: float,
    ) -> dict[str, Any]:
        if not research:
            return {
                "other_games_percent": 0.0,
                "share_of_processing": 0.0,
                "primary_game": None,
                "tracked_games": (),
            }
        other_games = float(research.get("other_games_raw_percent") or 0.0)
        base = raw_percent or processed_percent or float(
            research.get("raw_utilization_percent", 0.0)
        )
        share = 0.0
        if base > 0.0:
            share = min(100.0, (other_games / base) * 100.0)
        breakdown = dict(research.get("other_games_breakdown") or {})
        if not breakdown and research.get("competitive_research"):
            breakdown = dict(research["competitive_research"].get("games", {}))
        primary = None
        if research.get("competitive_research"):
            primary = research["competitive_research"].get("primary_game")
        return {
            "other_games_percent": round(other_games, 2),
            "share_of_processing": round(share, 2),
            "primary_game": primary,
            "tracked_games": _as_tuple(sorted(breakdown)),
        }

    def _network_security_overview(
        self,
        security: dict[str, Any],
        automation: dict[str, Any],
        upgrade_plan: dict[str, Any],
    ) -> dict[str, Any]:
        risk = str(security.get("risk", "low")).lower()
        incidents = int(security.get("incidents", 0))
        focus = automation.get("focus", "stabilise")
        backlog_priority = upgrade_plan.get("needs_redundancy")
        recommendations = upgrade_plan.get("recommendations", ())
        directive = focus
        if backlog_priority:
            directive = "fortify"
        if risk in {"high", "critical"}:
            directive = "mitigate"
        return {
            "risk": risk,
            "incidents": incidents,
            "automation_focus": focus,
            "directive": directive,
            "recommendations": recommendations,
        }

    def _holographic_signal_health(
        self,
        network: dict[str, Any] | None,
        holographic: dict[str, Any],
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        diagnostics = (network or {}).get("holographic_diagnostics") or {}
        anchor_quality = holographic.get("anchor_quality", 0.0)
        integrity = verification.get("integrity", "stable")
        triangulation = diagnostics.get("triangulation_hint") or holographic.get(
            "triangulation_hint", {}
        )
        return {
            "anchor_quality": round(float(anchor_quality), 3),
            "verification_integrity": integrity,
            "spectral_load": holographic.get("spectral_load", 0.0),
            "triangulation_hint": triangulation,
        }

    def _monster_mutation_paths(
        self, monsters: Sequence[dict[str, Any]] | None
    ) -> dict[str, Any]:
        monsters = list(monsters or [])
        if not monsters:
            return {"paths": (), "mutation_ready": False}
        role_hazards: dict[str, set[str]] = {}
        focus_tags: set[str] = set()
        for monster in monsters:
            if not monster:
                continue
            role = str(monster.get("role", "general"))
            hazard = str(monster.get("hazard", "unknown"))
            role_hazards.setdefault(role, set()).add(hazard)
            focus = monster.get("ai_focus")
            if focus:
                focus_tags.add(str(focus))
        paths: list[dict[str, Any]] = []
        mutation_ready = False
        for role, hazards in sorted(role_hazards.items()):
            variance = len(hazards)
            mutation_ready = mutation_ready or variance > 1
            paths.append(
                {
                    "role": role,
                    "hazards": _as_tuple(sorted(hazards)),
                    "variance": variance,
                }
            )
        return {
            "paths": tuple(paths),
            "mutation_ready": mutation_ready,
            "ai_focuses": _as_tuple(sorted(focus_tags)),
        }

    def _group_spawn_support(
        self,
        spawn_plan: dict[str, Any] | None,
        quests: Sequence[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        spawn_plan = spawn_plan or {}
        lanes = _as_tuple(spawn_plan.get("lanes", ()))
        tempo = str(spawn_plan.get("tempo", "steady"))
        quests = list(quests or [])
        trade_skills = {
            str(quest.get("trade_skill", ""))
            for quest in quests
            if quest.get("trade_skill")
        }
        boss_support = sum(1 for quest in quests if quest.get("supports_boss"))
        trade_support = sum(1 for quest in quests if quest.get("trade_skill"))
        coverage = 0.0
        if quests:
            coverage = round((boss_support + trade_support) / (len(quests) * 2), 2)
        return {
            "lanes": lanes,
            "tempo": tempo,
            "supporting_quests": boss_support,
            "trade_skills": _as_tuple(sorted(trade_skills)),
            "coverage": coverage,
        }

    def _ai_modularity_map(
        self,
        mob_ai: dict[str, Any] | None,
        spawn_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        mob_ai = mob_ai or {}
        directives = list(mob_ai.get("directives", ()))
        modules: list[dict[str, Any]] = []
        behaviours = set()
        hazards = set()
        for directive in directives:
            behaviour = str(directive.get("behaviour", ""))
            focus = str(directive.get("ai_focus", ""))
            hazard = str(directive.get("hazard", ""))
            monster = str(directive.get("monster", ""))
            behaviours.add(behaviour)
            if hazard:
                hazards.add(hazard)
            modules.append(
                {
                    "behaviour": behaviour,
                    "focus": focus or None,
                    "monster": monster or None,
                }
            )
        cadence = "static"
        interval = float((spawn_plan or {}).get("interval", 0.0) or 0.0)
        if interval and interval < 4.0:
            cadence = "rapid"
        elif interval > 10.0:
            cadence = "long_form"
        return {
            "module_count": len(modules),
            "behaviours": _as_tuple(sorted(b for b in behaviours if b)),
            "hazards": _as_tuple(sorted(hazards)),
            "modules": tuple(modules),
            "cadence": cadence,
        }

    def _boss_spawn_alerts(
        self,
        boss_plan: dict[str, Any] | None,
        spawn_plan: dict[str, Any] | None,
        network: dict[str, Any] | None,
    ) -> dict[str, Any]:
        if not boss_plan:
            return {}
        hazard = str(boss_plan.get("hazard", ""))
        threat = float(boss_plan.get("threat", 1.0))
        spawn_danger = float((spawn_plan or {}).get("danger", 1.0))
        latency = 0.0
        if network:
            latency = float((network.get("latency") or {}).get("average_ms", 0.0))
        severity = "watch"
        if threat >= 1.8 or spawn_danger >= 2.3:
            severity = "critical"
        elif threat >= 1.4 or spawn_danger >= 1.6:
            severity = "elevated"
        latency_flag = "normal"
        if latency >= 90.0:
            latency_flag = "degraded"
        elif latency >= 60.0:
            latency_flag = "tracking"
        return {
            "hazard": hazard,
            "severity": severity,
            "latency_watch": latency_flag,
            "threat": round(threat, 2),
            "spawn_danger": round(spawn_danger, 2),
        }

    def _quest_trade_dependencies(
        self,
        quests: Sequence[dict[str, Any]] | None,
        boss_plan: dict[str, Any] | None,
    ) -> dict[str, Any]:
        dependencies = self._quest_dependency(quests, boss_plan)
        if not dependencies:
            return {}
        skills = dependencies.get("skills", {})
        linked = dependencies.get("boss_linked_skills", ())
        total_links = sum(len(objectives) for objectives in skills.values())
        return {
            "skills": skills,
            "boss_linked_skills": linked,
            "dependency_count": total_links,
            "requires_boss_support": bool(linked),
        }

    def _research_benchmarking(
        self, research: dict[str, Any] | None
    ) -> dict[str, Any]:
        if not research:
            return {
                "raw_percent": 0.0,
                "primary_game": None,
                "trend": "unknown",
                "competitive_share": 0.0,
            }
        raw = float(research.get("raw_utilization_percent", 0.0))
        primary = None
        if research.get("competitive_research"):
            primary = research["competitive_research"].get("primary_game")
        share = float(research.get("competitive_share_percent", 0.0))
        trend = "steady"
        recent = list(research.get("raw_samples", ()))[-3:]
        if len(recent) >= 2 and recent[-1] > recent[0] + 2:
            trend = "rising"
        elif len(recent) >= 2 and recent[-1] < recent[0] - 2:
            trend = "cooling"
        return {
            "raw_percent": round(raw, 2),
            "primary_game": primary,
            "trend": trend,
            "competitive_share": round(share, 2),
        }

    def _managerial_guidance_map(
        self,
        management_playbook: dict[str, Any],
        backend_guidance: dict[str, Any] | None,
        research_benchmarking: dict[str, Any],
        group_support: dict[str, Any],
    ) -> dict[str, Any]:
        focus = management_playbook.get("pipeline_focus") if management_playbook else None
        priority = (backend_guidance or {}).get("priority")
        coverage = group_support.get("coverage", 0.0)
        share = research_benchmarking.get("competitive_share", 0.0)
        action = "stabilise"
        if share >= 50.0:
            action = "defend_market"
        elif coverage < 0.25:
            action = "boost_support"
        elif focus and priority and focus != priority:
            action = "realign"
        return {
            "focus": focus,
            "priority": priority,
            "coverage": coverage,
            "competitive_share": share,
            "recommended_action": action,
        }

    def _self_evolution_actions(
        self,
        pipeline: dict[str, Any],
        managerial_alignment: dict[str, Any],
        boss_alerts: dict[str, Any],
        research_benchmarking: dict[str, Any],
    ) -> tuple[str, ...]:
        actions: list[str] = []
        if pipeline.get("next_focus") and pipeline.get("next_focus") != "stabilise":
            actions.append(f"Advance {pipeline['next_focus'].replace('_', ' ')}")
        alignment = managerial_alignment.get("alignment")
        if alignment == "divergent":
            actions.append("Realign backend priorities")
        if boss_alerts.get("severity") == "critical":
            actions.append("Deploy emergency response team")
        elif boss_alerts.get("severity") == "elevated":
            actions.append("Stage reinforcement squads")
        if research_benchmarking.get("trend") == "rising":
            actions.append("Expand competitive monitoring")
        return tuple(dict.fromkeys(actions))

    def _self_evolution_dashboard(
        self,
        backend_guidance: dict[str, Any],
        management_playbook: dict[str, Any],
        pipeline: dict[str, Any],
        network: dict[str, Any] | None,
    ) -> dict[str, Any]:
        pipeline = pipeline or {}
        priority = backend_guidance.get("priority") if backend_guidance else None
        playbook_focus = management_playbook.get("pipeline_focus") if management_playbook else None
        network_status = (network or {}).get("network_health", {}).get("status")
        processing = (network or {}).get("network_processing_detail", {})
        return {
            "priority": priority,
            "pipeline_focus": playbook_focus,
            "network_status": network_status,
            "processing_detail": {
                "research_percent": processing.get("research_percent", 0.0),
                "auto_dev_load": processing.get("auto_dev_load", 0.0),
            },
            "pipeline_steps": _as_tuple(pipeline.get("pipeline_steps", ())),
        }

    def _directives(
        self,
        guidance: dict[str, Any] | None,
        evolution: dict[str, Any] | None,
    ) -> Iterable[str]:
        if guidance:
            for directive in guidance.get("directives", ()):  # type: ignore[arg-type]
                yield str(directive)
        if evolution:
            summary = evolution.get("summary")
            if summary:
                yield str(summary)
            next_objectives = evolution.get("next_objectives") or ()
            for objective in list(next_objectives)[:2]:
                yield str(objective)
