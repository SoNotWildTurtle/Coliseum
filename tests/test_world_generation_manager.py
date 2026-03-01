"""Tests for world generation manager."""

import math
import pytest

from hololive_coliseum.world_generation_manager import (
    GOLDEN_ANGLE,
    WorldGenerationManager,
)
from hololive_coliseum.item_manager import ItemManager, Sword, Armor


class DummySeedManager:
    def get_seeds(self):
        return ["abcd1234"]

    def __init__(self):
        self.synced = False

    def sync_with_blockchain(self):
        self.synced = True


class DummyContentManager:
    def __init__(self):
        self.calls = []

    def create(self, kind: str) -> str:
        self.calls.append(kind)
        return f"{kind}_1"


class DummyRegionManager:
    def __init__(self):
        self.added = []
        self.synced = False

    def add_region(self, region):
        self.added.append(region)
    def get_regions(self):
        return self.added

    def sync_with_blockchain(self):
        self.synced = True


def test_generate_region_stores_and_broadcasts(monkeypatch):
    drm = DummyRegionManager()
    calls = []
    monkeypatch.setattr(
        'hololive_coliseum.world_generation_manager.add_region_block',
        lambda region: calls.append(region),
    )
    wg = WorldGenerationManager(DummySeedManager(), DummyContentManager(), drm)
    region = wg.generate_region()
    assert region["seed"] == "abcd1234"
    assert region["radius"] == 1
    assert region["angle"] == pytest.approx(0)
    assert region["position"][0] == pytest.approx(1)
    assert region["position"][1] == pytest.approx(0)
    assert drm.get_regions()[0] == region
    assert calls[0] == region


def test_sync_world_calls_managers():
    seed_mgr = DummySeedManager()
    region_mgr = DummyRegionManager()
    wg = WorldGenerationManager(seed_mgr, DummyContentManager(), region_mgr)
    wg.sync_world()
    assert seed_mgr.synced
    assert region_mgr.synced


def test_sync_world_builds_missing_regions(monkeypatch):
    seed_mgr = DummySeedManager()
    region_mgr = DummyRegionManager()
    content = DummyContentManager()
    calls = []
    monkeypatch.setattr(
        "hololive_coliseum.world_generation_manager.add_region_block",
        lambda region: calls.append(region),
    )
    wg = WorldGenerationManager(seed_mgr, content, region_mgr)
    wg.sync_world()
    assert region_mgr.added[0]["seed"] == "abcd1234"
    assert calls[0]["seed"] == "abcd1234"
    assert content.calls == ["quest"]


def test_radius_expands_with_each_region(monkeypatch):
    seed_mgr = DummySeedManager()
    region_mgr = DummyRegionManager()
    content = DummyContentManager()
    monkeypatch.setattr(
        "hololive_coliseum.world_generation_manager.add_region_block",
        lambda region: None,
    )
    wg = WorldGenerationManager(seed_mgr, content, region_mgr)
    first = wg.generate_region()
    second = wg.generate_region_from_seed("abcd5678")
    assert first["radius"] == 1
    assert first["angle"] == pytest.approx(0)
    assert second["radius"] == 2
    angle = GOLDEN_ANGLE
    assert second["angle"] == pytest.approx(angle)
    assert second["position"][0] == pytest.approx(2 * math.cos(angle))
    assert second["position"][1] == pytest.approx(2 * math.sin(angle))


def test_generate_region_uses_max_radius(monkeypatch):
    """New regions base their radius on the largest existing value."""

    seed_mgr = DummySeedManager()
    region_mgr = DummyRegionManager()
    region_mgr.add_region({"radius": 5, "angle": 0, "position": [5, 0]})
    content = DummyContentManager()
    monkeypatch.setattr(
        "hololive_coliseum.world_generation_manager.add_region_block",
        lambda region: None,
    )
    wg = WorldGenerationManager(seed_mgr, content, region_mgr)
    region = wg.generate_region_from_seed("abcd9999")
    assert region["radius"] == 6
    expect_angle = 5 * GOLDEN_ANGLE
    assert region["angle"] == pytest.approx(expect_angle)
    assert region["position"][0] == pytest.approx(6 * math.cos(expect_angle))
    assert region["position"][1] == pytest.approx(6 * math.sin(expect_angle))


class DummyVotingManager:
    def get_winner(self):
        return "Gawr Gura"


class DummyBiomeManager:
    def get_winner(self):
        return "forest"


class DummyItemManager(ItemManager):
    def __init__(self):
        super().__init__()
        self.add_item(Sword("Wood Sword", {}))
        self.add_item(Armor("Leather Armor", {}))


def test_region_includes_vote_monument(monkeypatch):
    drm = DummyRegionManager()
    calls = []
    monkeypatch.setattr(
        'hololive_coliseum.world_generation_manager.add_region_block',
        lambda region: calls.append(region),
    )
    wg = WorldGenerationManager(
        DummySeedManager(),
        DummyContentManager(),
        drm,
        DummyVotingManager(),
    )
    region = wg.generate_region()
    assert region['feature']['character'] == 'Gawr Gura'
    assert region['feature']['type'] == 'monument'


def test_region_includes_biome_and_loot(monkeypatch):
    drm = DummyRegionManager()
    calls = []
    monkeypatch.setattr(
        'hololive_coliseum.world_generation_manager.add_region_block',
        lambda region: calls.append(region),
    )
    wg = WorldGenerationManager(
        DummySeedManager(),
        DummyContentManager(),
        drm,
        DummyVotingManager(),
        DummyBiomeManager(),
        DummyItemManager(),
    )
    region = wg.generate_region()
    assert region['biome'] == 'forest'
    assert region['loot']['weapon'] == 'Wood Sword'
    assert region['loot']['armor'] == 'Leather Armor'


class DummyFeedbackManager:
    def __init__(self) -> None:
        self.calls: list[int] = []

    def estimate_recommended_level(self, base_level: int) -> int:
        self.calls.append(base_level)
        return base_level + 2

    def region_insight(self):
        return {"trending_hazard": "lava"}


class DummyTuningManager:
    def __init__(self) -> None:
        self.calls = 0

    def support_plan(self):
        self.calls += 1
        return {
            "hazard": "lava",
            "target": 6,
            "recommended_powerups": ("shield", "defense"),
            "spawn_multiplier": 0.6,
        }


class DummyProjectionManager:
    def __init__(self) -> None:
        self.calls = 0

    def projection_summary(self):
        self.calls += 1
        return {
            "matches_considered": 4,
            "focus": [
                {
                    "hazard": "lava",
                    "weight": 0.5,
                    "danger_score": 50,
                    "recommended_powerups": ("shield", "defense"),
                    "spawn_multiplier": 0.6,
                }
            ],
        }


def test_region_includes_auto_dev_insight(monkeypatch):
    drm = DummyRegionManager()
    monkeypatch.setattr(
        'hololive_coliseum.world_generation_manager.add_region_block',
        lambda region: None,
    )
    monkeypatch.setattr(
        'hololive_coliseum.auto_dev_research_manager.AutoDevResearchManager._runtime_percent',
        lambda self: 30.0,
    )
    feedback = DummyFeedbackManager()
    tuning = DummyTuningManager()
    projection = DummyProjectionManager()
    wg = WorldGenerationManager(
        DummySeedManager(),
        DummyContentManager(),
        drm,
        feedback_manager=feedback,
        tuning_manager=tuning,
        projection_manager=projection,
    )
    region = wg.generate_region()
    assert region['recommended_level'] == 3
    assert region['auto_dev']['trending_hazard'] == 'lava'
    support = region['auto_dev']['support_plan']
    assert support['hazard'] == 'lava'
    assert 'shield' in support['recommended_powerups']
    projection_data = region['auto_dev']['projection']
    assert projection_data['focus'][0]['hazard'] == 'lava'
    scenarios = region['auto_dev']['scenarios']
    assert scenarios
    assert scenarios[0]['hazard'] == 'lava'
    assert scenarios[0]['recommended_objectives']
    roadmap = region['auto_dev']['roadmap']
    assert roadmap['focus'] == 'lava'
    assert roadmap['priority_actions']
    focus = region['auto_dev']['focus']
    assert focus['top_focus'] == 'lava'
    assert focus['priorities'][0]['hazard'] == 'lava'
    assert focus['context']['scenario_count'] == len(scenarios)
    monsters = region['auto_dev']['monsters']
    assert monsters and monsters[0]['hazard'] == 'lava'
    spawn_plan = region['auto_dev']['spawn_plan']
    assert spawn_plan['group_count'] >= 1
    mob_ai = region['auto_dev']['mob_ai']
    assert mob_ai['directives'][0]['hazard'] == 'lava'
    boss_plan = region['auto_dev']['boss_plan']
    assert boss_plan['hazard'] == 'lava'
    quests = region['auto_dev']['quests']
    assert quests
    creation_summary = region['auto_dev']['monster_creation_summary']
    assert creation_summary['count'] == len(monsters)
    assert creation_summary['status'] in {'stable', 'active', 'surging'}
    assert creation_summary['ai_focuses']
    assert creation_summary['spawn_synergies']
    spawn_summary = region['auto_dev']['group_spawn_summary']
    assert spawn_summary['groups'] >= spawn_plan['group_count']
    assert spawn_summary['pattern'] in {'burst', 'laned', 'staggered', 'onslaught', 'incursion'}
    assert spawn_summary['reinforcement_curve']
    mob_ai_summary = region['auto_dev']['mob_ai_summary']
    assert mob_ai_summary['directives'] == len(mob_ai['directives'])
    assert mob_ai_summary['training_modules']
    boss_summary = region['auto_dev']['boss_spawn_summary']
    assert boss_summary['name'] == boss_plan['name']
    assert boss_summary['strategies']
    quest_summary = region['auto_dev']['quest_generation_summary']
    assert quest_summary['count'] == len(quests)
    assert quest_summary['difficulty_breakdown']
    research = region['auto_dev']['research']
    assert research['utilization_percent'] >= 0.0
    assert 'latest_sample_percent' in research
    assert research['raw_utilization_percent'] == research['latest_sample_percent']
    assert region['auto_dev']['processing_utilization_percent'] == research['raw_utilization_percent']
    assert region['auto_dev']['raw_processing_utilization_percent'] == research['raw_utilization_percent']
    assert 'competitive_research' in region['auto_dev']
    assert region['auto_dev']['competitive_research']['raw_percent'] >= 0.0
    assert region['auto_dev']['competitive_raw_percent'] >= 0.0
    assert region['auto_dev']['competitive_share_percent'] >= 0.0
    assert region['auto_dev']['other_games_raw_percent'] >= 0.0
    assert isinstance(region['auto_dev']['other_games_breakdown'], dict)
    network = region['auto_dev']['network']
    assert network['latency']['average_ms'] >= 0.0
    assert network['network_health']['status']
    assert network['security']['risk']
    assert network['processing_utilization_percent'] >= 0.0
    assert 'network_processing_detail' in network
    assert network['network_processing_detail']['peak_bandwidth_mbps'] >= 0.0
    assert 'channel_map' in network['network_processing_detail']
    assert network['security_automation']['automation_score'] >= 0.0
    assert network['security_automation']['automation_tiers']
    assert network['holographic_channels']['layer_count'] >= 1
    assert network['holographic_channels']['channel_map']
    assert network['verification_layers']['layers'] == network['holographic_channels']['layer_count']
    assert region['auto_dev']['network_upgrade_backlog']
    assert region['auto_dev']['network_security_overview']
    assert region['auto_dev']['holographic_diagnostics']
    assert region['auto_dev']['network_security_automation']['automation_score'] == network['security_automation']['automation_score']
    assert region['auto_dev']['holographic_channels']['layer_count'] == network['holographic_channels']['layer_count']
    assert region['auto_dev']['network_verification_layers']['layers'] == network['verification_layers']['layers']
    guidance = region['auto_dev']['guidance']
    assert guidance['processing_utilization_percent'] == research['latest_sample_percent']
    assert guidance['directives']
    evolution = region['auto_dev']['evolution']
    assert evolution['processing_utilization_percent'] == guidance['processing_utilization_percent']
    assert evolution['next_objectives']
    intelligence = region['auto_dev']['general_intelligence']
    assert intelligence['processing_utilization_percent'] == research['raw_utilization_percent']
    assert intelligence['raw_processing_percent'] == research['raw_utilization_percent']
    assert intelligence['strategic_directives']
    assert intelligence['encounter_alignment']['boss'] == boss_plan['name']
    assert intelligence['encounter_blueprint']['boss_synergy'] is True
    assert intelligence['encounter_blueprint']['group_count'] >= spawn_plan['group_count']
    assert intelligence['quest_synergy']['boss_supporting_quest'] is True
    assert intelligence['research_utilization']['raw_percent'] == research['raw_utilization_percent']
    assert intelligence['backend_guidance']['priority']
    monster_catalog = intelligence['monster_catalog']
    assert monster_catalog['count'] >= len(monsters)
    spawn_overview = intelligence['spawn_overview']
    assert spawn_overview['group_count'] >= spawn_plan['group_count']
    ai_development = intelligence['mob_ai_development']
    assert ai_development['directive_count'] >= 1
    boss_outlook = intelligence['boss_outlook']
    assert boss_outlook['name'] == boss_plan['name']
    quest_matrix = intelligence['quest_matrix']
    assert quest_matrix['quest_total'] == len(quests)
    group_mechanics = intelligence['group_mechanics']
    assert group_mechanics['total_enemies'] >= spawn_plan['group_count']
    assert group_mechanics['hazard_focus']
    ai_training = intelligence['mob_ai_training']
    assert ai_training['hazards_supported']
    assert ai_training['coordination_window'] > 0.0
    assert region['auto_dev']['monster_mutation_paths']
    assert region['auto_dev']['group_spawn_support']['supporting_quests'] >= 0
    assert region['auto_dev']['ai_modularity_map']['module_count'] >= 0
    assert region['auto_dev']['boss_spawn_alerts']['hazard']
    assert region['auto_dev']['quest_trade_dependencies']['skills']
    assert region['auto_dev']['managerial_guidance_map']['recommended_action']
    assert isinstance(region['auto_dev']['self_evolution_actions'], tuple)
    pressure = intelligence['competitive_research_pressure']
    assert pressure['other_games_percent'] >= 0.0
    overview = intelligence['network_security_overview']
    assert overview['risk']
    signal_health = intelligence['holographic_signal_health']
    assert signal_health['triangulation_hint']
    dashboard = intelligence['self_evolution_dashboard']
    assert isinstance(dashboard['pipeline_steps'], tuple)
    boss_pressure = intelligence['boss_pressure']
    assert boss_pressure['hazard'] == boss_plan['hazard']
    quest_dependency = intelligence['quest_dependency']
    assert quest_dependency['skills']
    processing_overview = intelligence['processing_overview']
    assert processing_overview['current_percent'] == research['raw_utilization_percent']
    assert processing_overview['raw_percent'] == research['raw_utilization_percent']
    channels = intelligence['processing_channels']
    assert channels['channels']['research'] == research['raw_utilization_percent']
    pipeline = intelligence['orchestration_pipeline']
    assert pipeline['stages']
    playbook = intelligence['management_playbook']
    assert playbook['pipeline_focus'] in {
        'stabilise',
        'monster_design',
        'group_spawning',
        'mob_ai',
        'boss_selection',
        'quest_generation',
        'research_intelligence',
    }
    forge = intelligence['monster_forge']
    assert forge['status'] in {'idle', 'stable', 'active', 'surging'}
    mechanics_detail = intelligence['group_spawn_mechanics_detail']
    assert mechanics_detail['groups'] >= spawn_plan['group_count']
    ai_plan = intelligence['mob_ai_innovation_plan']
    assert ai_plan['directive_count'] >= 1
    boss_matrix = intelligence['boss_spawn_matrix']
    assert boss_matrix['name'] == boss_plan['name']
    tradecraft = intelligence['quest_tradecraft']
    assert tradecraft['boss_support'] >= 1
    pressure = intelligence['research_pressure']
    assert pressure['competitive_raw_percent'] >= 0.0
    alignment = intelligence['managerial_alignment']
    assert alignment['alignment'] in {'balanced', 'divergent', 'escalating'}
    assert playbook['raw_utilization'] == research['raw_utilization_percent']
    evolution_alignment = intelligence['evolution_alignment']
    assert evolution_alignment['guidance_priority'] == guidance['priority']
    creation = intelligence['monster_creation']
    assert creation['archetype_counts']
    spawn_tactics = intelligence['spawn_tactics']
    assert spawn_tactics['reinforcement_style']
    ai_plan = intelligence['ai_development_plan']
    assert ai_plan['iteration_mode']
    boss_strategy = intelligence['boss_spawn_strategy']
    assert boss_strategy['recommended_group']
    quest_generation = intelligence['quest_generation']
    assert quest_generation['quests_available'] == len(quests)
    comp_intel = intelligence['competitive_research']
    assert comp_intel['raw_percent'] >= 0.0
    group_coord = intelligence['group_spawn_coordination']
    assert group_coord['group_count'] >= spawn_plan['group_count']
    ai_innovation = intelligence['ai_innovation']
    assert ai_innovation['directive_count'] >= 1
    boss_readiness = intelligence['boss_spawn_readiness']
    assert boss_readiness['hazard'] == boss_plan['hazard']
    quest_alignment = intelligence['quest_trade_alignment']
    assert 'Combat' in quest_alignment['skills'] or 'Smithing' in quest_alignment['skills']
    managerial = intelligence['managerial_overview']
    assert managerial['raw_processing_percent'] == research['raw_utilization_percent']
    assert managerial['network_status'] == intelligence['network_health']['status']
    assert isinstance(managerial['relay_needs'], bool)
    assert managerial['security_automation_score'] == network['security_automation']['automation_score']
    assert managerial['holographic_anchor_quality'] == network['holographic_channels']['anchor_quality']
    assert managerial['verification_layers'] == network['verification_layers']['layers']
    net_health = intelligence['network_health']
    assert net_health['status']
    net_security = intelligence['network_security']
    assert net_security['risk']
    upgrade_plan = intelligence['network_upgrade_plan']
    assert isinstance(upgrade_plan['needs_redundancy'], bool)
    network_proc = intelligence['network_processing']
    assert network_proc['processing_percent'] >= 0.0
