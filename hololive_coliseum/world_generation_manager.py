"""Generate MMO regions from world seeds and dynamic content."""

from __future__ import annotations

import math
from typing import Dict, Sequence, TYPE_CHECKING
import random

from .world_seed_manager import WorldSeedManager
from .world_region_manager import WorldRegionManager
from .dynamic_content_manager import DynamicContentManager
from .blockchain import add_region as add_region_block
from .voting_manager import VotingManager
from .item_manager import ItemManager, Weapon, Armor
from .trade_skill_crafting_manager import TradeSkillCraftingManager
from .leveling_manager import LevelingManager
from .auto_dev_scenario_manager import AutoDevScenarioManager
from .auto_dev_roadmap_manager import AutoDevRoadmapManager
from .objective_manager import ObjectiveManager
from .auto_dev_focus_manager import AutoDevFocusManager
from .auto_dev_monster_manager import AutoDevMonsterManager
from .auto_dev_spawn_manager import AutoDevSpawnManager
from .auto_dev_mob_ai_manager import AutoDevMobAIManager
from .auto_dev_boss_manager import AutoDevBossManager
from .auto_dev_quest_manager import AutoDevQuestManager
from .auto_dev_research_manager import AutoDevResearchManager
from .auto_dev_guidance_manager import AutoDevGuidanceManager
from .auto_dev_evolution_manager import AutoDevEvolutionManager
from .auto_dev_intelligence_manager import AutoDevIntelligenceManager
from .auto_dev_network_manager import AutoDevNetworkManager
from .auto_dev_pipeline import AutoDevPipeline

if TYPE_CHECKING:  # pragma: no cover - imported for typing only
    from .auto_dev_feedback_manager import AutoDevFeedbackManager
    from .auto_dev_tuning_manager import AutoDevTuningManager
    from .auto_dev_projection_manager import AutoDevProjectionManager

# The golden angle in radians. Offsetting each region by this angle spreads
# positions evenly around expanding circles.
GOLDEN_ANGLE = math.pi * (3 - math.sqrt(5))


class WorldGenerationManager:
    """Create world regions using stored seeds and procedural content."""

    def __init__(
        self,
        seed_manager: WorldSeedManager | None = None,
        content_manager: DynamicContentManager | None = None,
        region_manager: WorldRegionManager | None = None,
        voting_manager: VotingManager | None = None,
        biome_manager: VotingManager | None = None,
        item_manager: ItemManager | None = None,
        level_manager: LevelingManager | None = None,
        feedback_manager: AutoDevFeedbackManager | None = None,
        tuning_manager: "AutoDevTuningManager" | None = None,
        projection_manager: "AutoDevProjectionManager" | None = None,
        objective_manager: ObjectiveManager | None = None,
        scenario_manager: AutoDevScenarioManager | None = None,
        roadmap_manager: AutoDevRoadmapManager | None = None,
        focus_manager: AutoDevFocusManager | None = None,
        monster_manager: AutoDevMonsterManager | None = None,
        spawn_manager: AutoDevSpawnManager | None = None,
        mob_ai_manager: AutoDevMobAIManager | None = None,
        boss_manager: AutoDevBossManager | None = None,
        quest_manager: AutoDevQuestManager | None = None,
        research_manager: AutoDevResearchManager | None = None,
        guidance_manager: AutoDevGuidanceManager | None = None,
        evolution_manager: AutoDevEvolutionManager | None = None,
        intelligence_manager: AutoDevIntelligenceManager | None = None,
        network_manager: AutoDevNetworkManager | None = None,
        crafting_manager: TradeSkillCraftingManager | None = None,
        auto_dev_pipeline: AutoDevPipeline | None = None,
    ) -> None:
        self.seed_manager = seed_manager or WorldSeedManager()
        self.content_manager = content_manager or DynamicContentManager()
        self.region_manager = region_manager or WorldRegionManager()
        self.voting_manager = voting_manager
        self.biome_manager = biome_manager
        self.item_manager = item_manager or ItemManager()
        self.level_manager = level_manager or LevelingManager()
        self.feedback_manager = feedback_manager
        self.tuning_manager = tuning_manager
        self.projection_manager = projection_manager
        self.objective_manager = objective_manager or ObjectiveManager()
        self.scenario_manager = scenario_manager or AutoDevScenarioManager(
            projection_manager=self.projection_manager,
            objective_manager=self.objective_manager,
        )
        self.roadmap_manager = roadmap_manager or AutoDevRoadmapManager()
        self.focus_manager = focus_manager or AutoDevFocusManager()
        self.monster_manager = monster_manager or AutoDevMonsterManager()
        self.spawn_manager = spawn_manager or AutoDevSpawnManager()
        self.mob_ai_manager = mob_ai_manager or AutoDevMobAIManager()
        self.boss_manager = boss_manager or AutoDevBossManager()
        self.quest_manager = quest_manager or AutoDevQuestManager()
        self.research_manager = research_manager or AutoDevResearchManager()
        self.guidance_manager = guidance_manager or AutoDevGuidanceManager()
        self.evolution_manager = evolution_manager or AutoDevEvolutionManager()
        self.intelligence_manager = intelligence_manager or AutoDevIntelligenceManager()
        self.network_manager = network_manager or AutoDevNetworkManager()
        self.crafting_manager = crafting_manager or TradeSkillCraftingManager(
            self.item_manager
        )
        self.auto_dev_pipeline = auto_dev_pipeline or AutoDevPipeline()
        self.pipeline_bias: dict[str, object] = {}
        # Keep the scenario manager aligned if callers injected a partially
        # configured instance.
        if self.scenario_manager.objective_manager is None:
            self.scenario_manager.objective_manager = self.objective_manager
        if self.projection_manager and self.scenario_manager.projection_manager is None:
            self.scenario_manager.projection_manager = self.projection_manager

    def set_pipeline_bias(self, plan: dict[str, object]) -> None:
        """Record auto-dev plan hints to steer future region generation."""
        overview = plan.get("overview", {}) if isinstance(plan, dict) else {}
        boss_plan = plan.get("boss_plan", {}) if isinstance(plan, dict) else {}
        hazards = []
        if isinstance(overview, dict):
            hazards = list(overview.get("hazards") or [])
        hazard_focus = str(boss_plan.get("hazard") or "")
        if hazards and not hazard_focus:
            hazard_focus = str(hazards[0])
        preferred_biome = self._biome_from_hazard(hazard_focus)
        self.pipeline_bias = {
            "hazard_focus": hazard_focus,
            "preferred_biome": preferred_biome,
            "boss_name": str(boss_plan.get("name") or ""),
            "spawn_tempo": str((overview or {}).get("spawn_tempo") or ""),
        }

    @staticmethod
    def _biome_from_hazard(hazard: str) -> str | None:
        hazard = str(hazard).lower()
        if hazard in {"ice", "frost", "snow"}:
            return "tundra"
        if hazard in {"lava", "fire", "heat"}:
            return "desert"
        if hazard in {"poison", "forest", "nature"}:
            return "forest"
        if hazard in {"storm", "lightning", "wind"}:
            return "plains"
        return None

    def _apply_pipeline_bias(
        self,
        region: Dict[str, object],
        *,
        pipeline_summary: dict[str, object] | None = None,
        pipeline_plan: dict[str, object] | None = None,
    ) -> None:
        bias = dict(self.pipeline_bias)
        if pipeline_summary:
            bias.update(pipeline_summary)
        preferred_biome = bias.get("preferred_biome")
        if preferred_biome:
            region["biome"] = preferred_biome
        feature = region.get("feature") or {}
        if not feature and bias.get("boss_name"):
            region["feature"] = {
                "type": "boss_lair",
                "boss": bias.get("boss_name"),
            }
        if pipeline_plan:
            quests = pipeline_plan.get("quests")
            if isinstance(quests, list) and quests:
                region["quest"] = quests[0]

    def sync_world(self) -> None:
        """Sync seeds and regions from the blockchain and rebuild gaps."""

        self.seed_manager.sync_with_blockchain()
        self.region_manager.sync_with_blockchain()
        existing = {r.get("seed") for r in self.region_manager.get_regions()}
        for seed in self.seed_manager.get_seeds():
            if seed not in existing:
                self.generate_region_from_seed(seed)

    def generate_region_from_seed(self, seed: str, player_id: str | None = None) -> Dict[str, object]:
        """Return a region generated deterministically from ``seed``.

        Each mined region lands on the next outward ring of a golden-angle
        spiral. The next ring is determined from the largest radius already
        stored so gaps cannot pull new regions inward. The ring radius grows by
        one each time and the angle advances by :data:`GOLDEN_ANGLE`, spreading
        regions evenly around the map so it expands in ever-larger circles. The
        resulting ``region`` records the radius, angle and 2-D position for
        later verification.
        """

        region_id = int(seed[:8], 16) % 1000
        quest = self.content_manager.create("quest")
        existing = self.region_manager.get_regions()
        index = max((r.get("radius", 0) for r in existing), default=0)
        radius = index + 1
        angle = index * GOLDEN_ANGLE
        position = [radius * math.cos(angle), radius * math.sin(angle)]
        feature: Dict[str, str] = {}
        if self.voting_manager:
            winner = self.voting_manager.get_winner()
            if winner:
                feature = {"type": "monument", "character": winner}
        biome_choices = ["plains", "forest", "desert", "tundra"]
        biome = random.choice(biome_choices)
        if self.biome_manager:
            biome = self.biome_manager.get_winner() or biome
        loot: Dict[str, str] = {}
        if self.item_manager:
            weapons = [i for i in self.item_manager.list_items() if isinstance(i, Weapon)]
            armors = [i for i in self.item_manager.list_items() if isinstance(i, Armor)]
            if weapons:
                loot['weapon'] = random.choice(weapons).name
            if armors:
                loot['armor'] = random.choice(armors).name
        region = {
            "name": f"region_{region_id}",
            "seed": seed,
            "quest": quest,
            "radius": radius,
            "angle": angle,
            "position": position,
            "feature": feature,
            "biome": biome,
            "loot": loot,
            "recommended_level": self.level_manager.get_level(player_id) if player_id else 1,
        }
        if self.objective_manager:
            self.objective_manager.ensure_region_objectives(region)
        auto_dev_data: Dict[str, object] = {}
        feedback_summary: Dict[str, object] | None = None
        support_plan: Dict[str, object] | None = None
        projection_summary: Dict[str, object] | None = None
        scenario_briefs: list[Dict[str, object]] = []
        roadmap_entry: Dict[str, object] | None = None
        focus_report: Dict[str, object] | None = None
        if self.feedback_manager:
            base_level = region["recommended_level"]
            region["recommended_level"] = self.feedback_manager.estimate_recommended_level(
                base_level
            )
            feedback_summary = self.feedback_manager.region_insight()
            if feedback_summary:
                auto_dev_data.update(feedback_summary)
        if self.tuning_manager:
            support_plan = self.tuning_manager.support_plan()
            if support_plan:
                auto_dev_data["support_plan"] = support_plan
        if self.projection_manager:
            projection_summary = self.projection_manager.projection_summary()
            if projection_summary:
                auto_dev_data["projection"] = projection_summary
        if self.scenario_manager:
            scenario_briefs = self.scenario_manager.scenario_briefs()
            if scenario_briefs:
                auto_dev_data["scenarios"] = scenario_briefs
        if self.roadmap_manager:
            roadmap_entry = self.roadmap_manager.compile_iteration(
                feedback=feedback_summary,
                feedback_manager=self.feedback_manager,
                projection=projection_summary,
                scenarios=scenario_briefs,
                support_plan=support_plan,
            )
            if roadmap_entry:
                auto_dev_data["roadmap"] = roadmap_entry
        if self.focus_manager:
            focus_report = self.focus_manager.analyse(
                roadmap=roadmap_entry,
                feedback=feedback_summary,
                projection=projection_summary,
                scenarios=scenario_briefs,
                support_plan=support_plan,
            )
            if focus_report:
                auto_dev_data["focus"] = focus_report
        trade_skills = self._derive_trade_skills(roadmap_entry, scenario_briefs)
        if self.crafting_manager:
            crafted_records = self.crafting_manager.craft_items(trade_skills)
            if crafted_records:
                auto_dev_data["trade_crafting"] = [
                    record.as_dict() for record in crafted_records
                ]
        monsters: list[Dict[str, object]] = []
        if self.monster_manager:
            monsters = self.monster_manager.generate_monsters(
                focus=focus_report,
                scenarios=scenario_briefs,
                trade_skills=trade_skills,
            )
            if monsters:
                auto_dev_data["monsters"] = monsters
        spawn_plan: Dict[str, object] = {}
        if self.spawn_manager:
            spawn_plan = self.spawn_manager.plan_groups(
                monsters,
                scenarios=scenario_briefs,
            )
            if spawn_plan:
                auto_dev_data["spawn_plan"] = spawn_plan
        if self.mob_ai_manager:
            ai_directives = self.mob_ai_manager.ai_directives(
                monsters,
                spawn_plan=spawn_plan,
                projection=projection_summary,
            )
            if ai_directives:
                auto_dev_data["mob_ai"] = ai_directives
        boss_plan: Dict[str, object] = {}
        if self.boss_manager:
            boss_plan = self.boss_manager.select_boss(
                monsters,
                roadmap=roadmap_entry,
                projection=projection_summary,
                spawn_plan=spawn_plan,
                trade_skills=trade_skills,
            )
            if boss_plan:
                auto_dev_data["boss_plan"] = boss_plan
        if self.quest_manager:
            quests = self.quest_manager.generate_quests(
                trade_skills,
                boss_plan=boss_plan,
                spawn_plan=spawn_plan,
            )
            if quests:
                auto_dev_data["quests"] = quests
        if monsters:
            auto_dev_data["monster_creation_summary"] = self._summarise_monsters(
                monsters,
                trade_skills,
            )
        if spawn_plan:
            auto_dev_data["group_spawn_summary"] = self._summarise_spawn_plan(
                spawn_plan,
                monsters,
            )
        if auto_dev_data.get("mob_ai"):
            auto_dev_data["mob_ai_summary"] = self._summarise_mob_ai(
                auto_dev_data["mob_ai"],
                monsters,
            )
        if boss_plan:
            auto_dev_data["boss_spawn_summary"] = self._summarise_boss_plan(
                boss_plan,
                spawn_plan,
                quests or [],
            )
        if auto_dev_data.get("quests"):
            auto_dev_data["quest_generation_summary"] = self._summarise_quests(
                auto_dev_data["quests"],
                trade_skills,
                boss_plan,
            )
        if self.research_manager:
            self.research_manager.update_from_intensity(0.2, source="auto_dev")
            rival_focus = (boss_plan or {}).get("name") or region["biome"].title()
            rival_percent = float((spawn_plan or {}).get("danger", 1.0)) * 12.0
            rival_percent += len(monsters) * 1.5
            rival_percent = max(5.0, min(55.0, rival_percent))
            self.research_manager.record_competitive_research(
                rival_percent,
                game=f"{rival_focus} Rival",
            )
            self.research_manager.capture_runtime_utilization(source="runtime_probe")
            research = self.research_manager.intelligence_brief()
            if research:
                auto_dev_data["research"] = research
                raw_percent = research.get(
                    "raw_utilization_percent",
                    research.get(
                        "latest_sample_percent",
                        research.get("utilization_percent", 0.0),
                    ),
                )
                auto_dev_data["processing_utilization_percent"] = raw_percent
                auto_dev_data["raw_processing_utilization_percent"] = raw_percent
                if research.get("competitive_research"):
                    auto_dev_data["competitive_research"] = research["competitive_research"]
                auto_dev_data["competitive_raw_percent"] = research.get(
                    "competitive_raw_percent",
                    0.0,
                )
                auto_dev_data["competitive_share_percent"] = research.get(
                    "competitive_share_percent",
                    0.0,
                )
                auto_dev_data["other_games_raw_percent"] = research.get(
                    "other_games_raw_percent",
                    0.0,
                )
                auto_dev_data["other_games_breakdown"] = research.get(
                    "other_games_breakdown",
                    {},
                )
        if self.guidance_manager:
            guidance_summary = self.guidance_manager.compose_guidance(
                monsters=monsters,
                spawn_plan=spawn_plan,
                mob_ai=auto_dev_data.get("mob_ai"),
                boss_plan=boss_plan or None,
                quests=auto_dev_data.get("quests"),
                research=auto_dev_data.get("research"),
            )
            if guidance_summary:
                auto_dev_data["guidance"] = guidance_summary

        if self.evolution_manager:
            evolution_brief = self.evolution_manager.evolution_brief(
                guidance=auto_dev_data.get("guidance"),
                roadmap=roadmap_entry,
                focus=focus_report,
                research=auto_dev_data.get("research"),
                monsters=monsters,
                spawn_plan=spawn_plan or None,
                quests=auto_dev_data.get("quests"),
            )
            if evolution_brief:
                auto_dev_data["evolution"] = evolution_brief
        if self.network_manager:
            network_summary = self.network_manager.assess_network(
                nodes=self._network_nodes(spawn_plan, focus_report, auto_dev_data.get("guidance")),
                bandwidth_samples=self._network_bandwidth_samples(
                    spawn_plan,
                    monsters,
                    auto_dev_data.get("research"),
                ),
                security_events=self._network_security_events(
                    boss_plan,
                    auto_dev_data.get("quests"),
                    auto_dev_data.get("guidance"),
                ),
                research=auto_dev_data.get("research"),
                auto_dev_load=auto_dev_data.get("processing_utilization_percent"),
            )
            if network_summary:
                auto_dev_data["network"] = network_summary
                auto_dev_data["network_security_automation"] = network_summary.get(
                    "security_automation"
                )
                auto_dev_data["holographic_channels"] = network_summary.get(
                    "holographic_channels"
                )
                auto_dev_data["network_verification_layers"] = network_summary.get(
                    "verification_layers"
                )
                auto_dev_data["network_upgrade_backlog"] = network_summary.get(
                    "upgrade_backlog",
                )
                auto_dev_data["network_security_overview"] = network_summary.get(
                    "security_auto_dev",
                )
                auto_dev_data["holographic_diagnostics"] = network_summary.get(
                    "holographic_diagnostics",
                )
                if self.guidance_manager and auto_dev_data.get("guidance"):
                    refreshed_guidance = self.guidance_manager.compose_guidance(
                        monsters=monsters,
                        spawn_plan=spawn_plan,
                        mob_ai=auto_dev_data.get("mob_ai"),
                        boss_plan=boss_plan or None,
                        quests=auto_dev_data.get("quests"),
                        research=auto_dev_data.get("research"),
                        network=network_summary,
                    )
                    if refreshed_guidance:
                        auto_dev_data["guidance"] = refreshed_guidance
        if self.intelligence_manager:
            intelligence_brief = self.intelligence_manager.synthesise(
                monsters=monsters or None,
                spawn_plan=spawn_plan or None,
                mob_ai=auto_dev_data.get("mob_ai"),
                boss_plan=boss_plan or None,
                quests=auto_dev_data.get("quests"),
                research=auto_dev_data.get("research"),
                guidance=auto_dev_data.get("guidance"),
                evolution=auto_dev_data.get("evolution"),
                network=auto_dev_data.get("network"),
            )
            if intelligence_brief:
                auto_dev_data["general_intelligence"] = intelligence_brief
                auto_dev_data["general_intelligence_competitive"] = intelligence_brief.get(
                    "competitive_research_pressure"
                )
                auto_dev_data["general_intelligence_security"] = intelligence_brief.get(
                    "network_security_overview"
                )
                auto_dev_data["holographic_signal_health"] = intelligence_brief.get(
                    "holographic_signal_health"
                )
                auto_dev_data["self_evolution_dashboard"] = intelligence_brief.get(
                    "self_evolution_dashboard"
                )
                auto_dev_data["monster_mutation_paths"] = intelligence_brief.get(
                    "monster_mutation_paths"
                )
                auto_dev_data["group_spawn_support"] = intelligence_brief.get(
                    "group_spawn_support"
                )
                auto_dev_data["ai_modularity_map"] = intelligence_brief.get(
                    "ai_modularity_map"
                )
                auto_dev_data["boss_spawn_alerts"] = intelligence_brief.get(
                    "boss_spawn_alerts"
                )
                auto_dev_data["quest_trade_dependencies"] = intelligence_brief.get(
                    "quest_trade_dependencies"
                )
                auto_dev_data["managerial_guidance_map"] = intelligence_brief.get(
                    "managerial_guidance_map"
                )
                auto_dev_data["self_evolution_actions"] = intelligence_brief.get(
                    "self_evolution_actions"
                )
        pipeline_plan: dict[str, object] = {}
        if self.auto_dev_pipeline:
            pipeline_plan = self.auto_dev_pipeline.build_plan(
                focus=focus_report,
                scenarios=scenario_briefs,
                trade_skills=trade_skills,
                network_nodes=self._network_nodes(
                    spawn_plan,
                    focus_report,
                    auto_dev_data.get("guidance"),
                ),
                bandwidth_samples=self._network_bandwidth_samples(
                    spawn_plan,
                    monsters,
                    auto_dev_data.get("research"),
                ),
                security_events=self._network_security_events(
                    boss_plan,
                    auto_dev_data.get("quests"),
                    auto_dev_data.get("guidance"),
                ),
                research_sample=float(
                    auto_dev_data.get("processing_utilization_percent", 0.0)
                ),
            )
            if pipeline_plan:
                overview = pipeline_plan.get("overview", {})
                boss = pipeline_plan.get("boss_plan", {})
                summary = {
                    "boss_name": boss.get("name"),
                    "hazards": overview.get("hazards", ()),
                    "spawn_tempo": overview.get("spawn_tempo"),
                    "network_upgrades": overview.get("network_upgrades", ()),
                    "preferred_biome": self._biome_from_hazard(
                        str(boss.get("hazard") or "")
                    ),
                }
                auto_dev_data["auto_dev_plan"] = pipeline_plan
                auto_dev_data["auto_dev_plan_summary"] = summary
                self.set_pipeline_bias(pipeline_plan)
                self._apply_pipeline_bias(
                    region,
                    pipeline_summary=summary,
                    pipeline_plan=pipeline_plan,
                )
        if auto_dev_data:
            region["auto_dev"] = auto_dev_data
        self.region_manager.add_region(region)
        add_region_block(region)
        if player_id:
            self.level_manager.add_xp(player_id, 50)
        return region

    def generate_region(self, player_id: str | None = None) -> Dict[str, object]:
        """Return a simple region dict derived from the latest seed.

        The seed's leading hex digits determine a region id while the dynamic
        content manager supplies a placeholder quest. An empty dict is returned
        if no seeds have been collected yet.
        """

        seeds = self.seed_manager.get_seeds()
        if not seeds:
            return {}
        return self.generate_region_from_seed(seeds[-1], player_id)

    def _network_nodes(
        self,
        spawn_plan: Dict[str, object],
        focus_report: Dict[str, object] | None,
        guidance: Dict[str, object] | None,
    ) -> list[Dict[str, object]]:
        lanes = list(spawn_plan.get("lanes", ())) or ["central"]
        danger = float(spawn_plan.get("danger", 1.0) or 1.0)
        base_latency = 30.0 + danger * 8.0
        hazard_focus = ""
        if focus_report and focus_report.get("top_focus"):
            hazard_focus = str(focus_report["top_focus"]).lower()
        priority = str((guidance or {}).get("priority", "")).lower()
        nodes: list[Dict[str, object]] = []
        for index, lane in enumerate(lanes):
            latency = base_latency + index * 4.0
            uptime = max(0.6, 0.94 - index * 0.05)
            nodes.append(
                {
                    "name": f"{lane}_relay",
                    "role": "relay",
                    "latency_ms": latency,
                    "uptime_ratio": uptime,
                    "trusted": hazard_focus not in {"chaos", "void"},
                }
            )
        nodes.append(
            {
                "name": "core_hub",
                "role": "core",
                "latency_ms": max(10.0, base_latency - 6.0),
                "uptime_ratio": 0.97,
                "trusted": True,
            }
        )
        if priority in {"high", "critical"}:
            nodes.append(
                {
                    "name": "priority_bridge",
                    "role": "relay",
                    "latency_ms": base_latency + 2.0,
                    "uptime_ratio": 0.92,
                    "trusted": True,
                }
            )
        return nodes

    def _network_bandwidth_samples(
        self,
        spawn_plan: Dict[str, object],
        monsters: Sequence[Dict[str, object]],
        research: Dict[str, object] | None,
    ) -> list[float]:
        group_count = float(spawn_plan.get("group_count", 1.0) or 1.0)
        danger = float(spawn_plan.get("danger", 1.0) or 1.0)
        monster_load = max(0, len(monsters))
        research_percent = 0.0
        if research:
            research_percent = float(
                research.get("raw_utilization_percent")
                or research.get("latest_sample_percent")
                or research.get("utilization_percent")
                or 0.0
            )
        baseline = max(2.5, group_count * 2.5)
        second = baseline + monster_load * 0.8 + research_percent / 10.0
        peak = second + max(1.5, danger * 3.5)
        return [round(baseline, 2), round(second, 2), round(peak, 2)]

    def _network_security_events(
        self,
        boss_plan: Dict[str, object] | None,
        quests: Sequence[Dict[str, object]] | None,
        guidance: Dict[str, object] | None,
    ) -> list[Dict[str, str]]:
        events: list[Dict[str, str]] = []
        hazard = str((boss_plan or {}).get("hazard", ""))
        if hazard:
            severity = "high" if hazard.lower() in {"void", "chaos", "shadow"} else "medium"
            events.append({"severity": severity, "type": f"{hazard}_surge"})
        if guidance and str(guidance.get("priority", "")).lower() in {"high", "critical"}:
            events.append({"severity": "medium", "type": "priority_throttle"})
        for quest in quests or ():
            objective = str(quest.get("objective", "")).lower()
            if "breach" in objective or "defend" in objective:
                events.append({"severity": "critical", "type": "player_security"})
                break
        return events

    def _summarise_monsters(
        self,
        monsters: Sequence[Dict[str, object]],
        trade_skills: Sequence[str],
    ) -> Dict[str, object]:
        hazards = sorted({str(monster.get("hazard")) for monster in monsters if monster.get("hazard")})
        elites = sum(1 for monster in monsters if monster.get("elite"))
        load_state = "stable"
        if len(monsters) >= 5 or elites >= 2:
            load_state = "surging"
        elif len(monsters) >= 3:
            load_state = "active"
        weaknesses = sorted({str(monster.get("weakness")) for monster in monsters if monster.get("weakness")})
        supporting_skills = sorted({skill for skill in trade_skills if skill in weaknesses})
        ai_focuses = sorted({str(monster.get("ai_focus", "adaptive")) for monster in monsters})
        synergies = sorted({str(monster.get("spawn_synergy", "skirmish")) for monster in monsters})
        return {
            "count": len(monsters),
            "hazards": tuple(hazards),
            "elite_count": elites,
            "status": load_state,
            "supporting_trade_skills": tuple(supporting_skills),
            "ai_focuses": tuple(ai_focuses),
            "spawn_synergies": tuple(synergies),
        }

    def _summarise_spawn_plan(
        self,
        spawn_plan: Dict[str, object],
        monsters: Sequence[Dict[str, object]],
    ) -> Dict[str, object]:
        groups = spawn_plan.get("groups") or ()
        total = sum(int(group.get("size", 0)) for group in groups)
        largest = max((int(group.get("size", 0)) for group in groups), default=0)
        hazard_focus = sorted({str(monster.get("hazard")) for monster in monsters if monster.get("hazard")})
        pattern = str(spawn_plan.get("formation", "staggered"))
        tempo = str(spawn_plan.get("tempo", "balanced"))
        reinforcement_curve = tuple(float(interval) for interval in spawn_plan.get("reinforcement_curve", ()))
        lanes = tuple(spawn_plan.get("lanes", ())) or ("central",)
        return {
            "groups": int(spawn_plan.get("group_count", len(groups))),
            "total_enemies": total,
            "largest_group": largest,
            "pattern": pattern,
            "lanes": lanes,
            "tempo": tempo,
            "reinforcement_curve": reinforcement_curve,
            "hazards": tuple(hazard_focus),
        }

    def _summarise_mob_ai(
        self,
        mob_ai: Dict[str, object],
        monsters: Sequence[Dict[str, object]],
    ) -> Dict[str, object]:
        directives = mob_ai.get("directives") or ()
        hazards = sorted({str(item.get("hazard")) for item in directives if item.get("hazard")})
        if not hazards:
            hazards = sorted({str(monster.get("hazard")) for monster in monsters if monster.get("hazard")})
        iteration_mode = "steady"
        if mob_ai.get("learning"):
            iteration_mode = "continuous"
        if mob_ai.get("adaptive"):
            iteration_mode = "accelerated"
        coordination = "solo"
        if any(item.get("behaviour") == "coordinated assaults" for item in directives):
            coordination = "coordinated"
        elif len(directives) > 1:
            coordination = "squad"
        training_modules = tuple(mob_ai.get("training_modules", ()))
        focus_cycle = tuple(
            str(item.get("ai_focus", "adaptive"))
            for item in directives
            if item.get("ai_focus")
        )
        return {
            "directives": len(directives),
            "hazards": tuple(hazards),
            "iteration_mode": iteration_mode,
            "coordination": coordination,
            "training_modules": training_modules,
            "ai_focuses": focus_cycle,
        }

    def _summarise_boss_plan(
        self,
        boss_plan: Dict[str, object],
        spawn_plan: Dict[str, object] | None,
        quests: Sequence[Dict[str, object]],
    ) -> Dict[str, object]:
        boss_name = boss_plan.get("name")
        supporting = 0
        for quest in quests:
            title = str(quest.get("title", ""))
            objective = str(quest.get("objective", ""))
            lower_title = title.lower()
            lower_objective = objective.lower()
            if boss_name and (
                boss_name.lower() in lower_title or boss_name.lower() in lower_objective
            ):
                supporting += 1
                continue
            if "boss" in lower_title or "boss" in lower_objective:
                supporting += 1
        interval = float((spawn_plan or {}).get("interval", 0.0))
        if interval <= 0.0:
            interval = float(boss_plan.get("interval", 0.0))
        recommended = boss_plan.get("recommended_group")
        if not recommended:
            group_count = int((spawn_plan or {}).get("group_count", 1))
            recommended = "raid" if group_count >= 3 else "party"
        return {
            "name": boss_plan.get("name"),
            "hazard": boss_plan.get("hazard"),
            "threat": boss_plan.get("threat", 1.0),
            "recommended_group": recommended,
            "spawn_interval": interval,
            "supporting_quests": supporting,
            "strategies": tuple(boss_plan.get("strategies", ())),
        }

    def _summarise_quests(
        self,
        quests: Sequence[Dict[str, object]],
        trade_skills: Sequence[str],
        boss_plan: Dict[str, object] | None,
    ) -> Dict[str, object]:
        skills = sorted({str(quest.get("trade_skill")) for quest in quests if quest.get("trade_skill")})
        boss_name = (boss_plan or {}).get("name")
        boss_support = 0
        difficulty_counts: Dict[str, int] = {}
        tags: set[str] = set()
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
            difficulty = str(quest.get("difficulty", "standard"))
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
            tags.update(str(tag) for tag in quest.get("tags", ()))
        trade_alignment = sorted(skill for skill in trade_skills if skill in skills)
        return {
            "count": len(quests),
            "skills": tuple(skills),
            "boss_support": boss_support,
            "trade_alignment": tuple(trade_alignment),
            "difficulty_breakdown": {k: difficulty_counts.get(k, 0) for k in sorted(difficulty_counts)},
            "tags": tuple(sorted(tags)),
        }

    def _derive_trade_skills(
        self,
        roadmap_entry: Dict[str, object] | None,
        scenarios: Sequence[Dict[str, object]],
    ) -> list[str]:
        skills: list[str] = []
        if roadmap_entry and roadmap_entry.get("focus"):
            focus = str(roadmap_entry["focus"]).title()
            skills.append(f"{focus} Engineering")
        for scenario in scenarios:
            hazard = scenario.get("hazard")
            if hazard:
                skills.append(f"{str(hazard).title()} Crafting")
        if not skills:
            skills = ["Mining", "Smithing", "Alchemy"]
        # Preserve order while removing duplicates.
        seen: set[str] = set()
        ordered: list[str] = []
        for skill in skills:
            if skill not in seen:
                ordered.append(skill)
                seen.add(skill)
        return ordered
