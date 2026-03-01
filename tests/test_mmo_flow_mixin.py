"""Coverage for MMO flow mixin helpers."""

from __future__ import annotations

from hololive_coliseum.game_mmo_flow import GameMMOFlow
from hololive_coliseum.game_mmo_logic import GameMMOLogic


class DummyRegionManager:
    def __init__(self, regions):
        self._regions = regions

    def get_regions(self):
        return list(self._regions)


class DummyWorldGenerationManager:
    def __init__(self, regions):
        self.region_manager = DummyRegionManager(regions)


class DummyWorldPlayerManager:
    def __init__(self, pos):
        self._pos = pos

    def get_position(self, player_id):
        return self._pos


class DummyReputationManager:
    def __init__(self):
        self.rep = {}

    def get(self, name):
        return int(self.rep.get(name, 0))

    def modify(self, name, delta):
        self.rep[name] = self.get(name) + int(delta)


class DummyGame(GameMMOLogic, GameMMOFlow):
    def __init__(self, regions, player_pos=(0.0, 0.0)):
        self.world_generation_manager = DummyWorldGenerationManager(regions)
        self.world_player_manager = DummyWorldPlayerManager(player_pos)
        self.mmo_player_id = "player"
        self.mmo_biome_filter = "all"
        self.mmo_sort_mode = "distance"
        self.mmo_sort_modes = ["distance", "level", "biome", "threat"]
        self.mmo_region_index = 0
        self.mmo_message = ""
        self.mmo_threat_history = {}
        self.mmo_threat_history_window = 6
        self.mmo_last_patrol_dispatch = 0
        self.mmo_patrol_dispatch_interval = 0
        self.mmo_stats = {}
        self.mmo_resource_cache = {}
        self.mmo_weather_cache = {}
        self.mmo_directive_sequence = 1
        self.mmo_directives = []
        self.mmo_bounties = []
        self.mmo_projects = []
        self.mmo_training_queue = []
        self.mmo_operations = []
        self.mmo_contracts = []
        self.mmo_expeditions = []
        self.mmo_favorites = set()
        self.mmo_trade_routes = []
        self.mmo_stockpile = {}
        self.mmo_shipments = []
        self.mmo_auto_agents = []
        self.mmo_remote_positions = {}
        self.mmo_outposts = []
        self.mmo_world_events = []
        self.mmo_guilds = []
        self.mmo_influence = {}
        self.mmo_auto_dev_interval = 10000
        self.mmo_last_auto_dev_tick = 0
        self.mmo_last_shipment_auto = 0
        self.mmo_auto_dev_shipment_cooldown = 100
        self.mmo_focus_region_threat = 0.0
        self.mmo_ai_seed = 42
        self.mmo_credits = 0
        self.mmo_last_world_tick = 0
        self.mmo_world_tick_interval = 1000
        self.reputation_manager = DummyReputationManager()
        self.mmo_event_log = []

    def _mmo_log_event(self, message: str) -> None:
        self.mmo_event_log.append(message)

    def _mmo_assign_directive(self, directive: dict[str, object]) -> None:
        directive["status"] = "assigned"

    def _mmo_assign_bounty(self, bounty: dict[str, object]) -> None:
        bounty["status"] = "assigned"

    def _mmo_start_project(self, project: dict[str, object]) -> None:
        project["status"] = "active"

    def _mmo_start_training(self, training: dict[str, object]) -> None:
        training["status"] = "active"

    def _mmo_append_contract(self) -> None:
        self.mmo_contracts.append({"status": "open"})

    def _mmo_append_operation(self) -> None:
        self.mmo_operations.append({"status": "open"})

    def _mmo_append_project(self) -> None:
        self.mmo_projects.append({"status": "open"})

    def _mmo_append_training(self) -> None:
        self.mmo_training_queue.append({"status": "open"})


def test_biome_from_hazard_mapping():
    assert DummyGame._mmo_biome_from_hazard("ice storm") == "tundra"
    assert DummyGame._mmo_biome_from_hazard("lava surge") == "desert"
    assert DummyGame._mmo_biome_from_hazard("poison fog") == "forest"
    assert DummyGame._mmo_biome_from_hazard("wind shear") == "plains"


def test_focus_region_prefers_preferred_biome():
    regions = [
        {"name": "A", "biome": "plains", "recommended_level": 1},
        {"name": "B", "biome": "forest", "recommended_level": 3},
    ]
    game = DummyGame(regions)
    plan = {"overview": {"preferred_biome": "forest"}}
    focus = game._mmo_focus_region(plan)
    assert focus is not None
    assert focus["name"] == "B"


def test_auto_escort_assigns_high_risk_shipments():
    game = DummyGame(regions=[])
    game.mmo_credits = 20
    game.mmo_shipments = [
        {
            "status": "in_transit",
            "risk": "high",
            "escorted": False,
            "eta": 4,
            "destination": "Frontier",
        }
    ]
    game._mmo_auto_escort_shipments(now=1000)
    assert game.mmo_shipments[0]["escorted"] is True
    assert game.mmo_credits == 5


def test_assign_patrol_creates_agent():
    region = {"name": "Alpha", "position": [0.2, 0.1]}
    game = DummyGame(regions=[region])
    game.mmo_auto_agents = []
    game._mmo_assign_patrol(region)
    assert len(game.mmo_auto_agents) == 1
    agent = game.mmo_auto_agents[0]
    assert agent.get("assignment") == "Alpha"
    assert agent.get("target") == [0.2, 0.1]


def test_patrol_dispatch_prefers_events():
    regions = [
        {"name": "Alpha", "position": [0.0, 0.0]},
        {"name": "Bravo", "position": [0.5, 0.0]},
    ]
    game = DummyGame(regions=regions)
    game.mmo_world_events = [
        {"region": "Bravo", "severity": "High"},
        {"region": "Alpha", "severity": "Low"},
    ]
    game.mmo_patrol_dispatch_interval = 0
    game.mmo_auto_agents = []
    game._mmo_dispatch_patrols(now=1000)
    assert game.mmo_auto_agents
    assert game.mmo_auto_agents[0].get("assignment") == "Bravo"
