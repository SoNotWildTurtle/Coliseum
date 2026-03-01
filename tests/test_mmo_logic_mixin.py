"""Coverage for MMO logic mixin helpers."""

from __future__ import annotations

from hololive_coliseum.game_mmo_logic import GameMMOLogic
from hololive_coliseum.mmo_world_state_manager import MMOWorldStateManager


class DummyRegionManager:
    def __init__(self, regions):
        self._regions = regions

    def get_regions(self):
        return list(self._regions)

    def set_regions(self, regions):
        self._regions = list(regions)


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


class DummyEconomyManager:
    def __init__(self):
        self.prices = {}

    def get_price(self, resource):
        return int(self.prices.get(resource, 10))

    def set_price(self, resource, price):
        self.prices[resource] = int(price)


class DummyGame(GameMMOLogic):
    def __init__(self, regions, player_pos=(0.0, 0.0)):
        self.world_generation_manager = DummyWorldGenerationManager(regions)
        self.world_player_manager = DummyWorldPlayerManager(player_pos)
        self.mmo_player_id = "player"
        self.mmo_biome_filter = "all"
        self.mmo_sort_mode = "distance"
        self.mmo_sort_modes = ["distance", "level", "biome", "threat"]
        self.mmo_resource_cache = {}
        self.mmo_weather_cache = {}
        self.mmo_weather_forecast_steps = 3
        self.mmo_threat_history = {}
        self.mmo_threat_history_window = 6
        self.mmo_world_events = []
        self.mmo_contracts = []
        self.mmo_operations = []
        self.mmo_outposts = []
        self.mmo_trade_routes = []
        self.mmo_shipments = []
        self.mmo_stockpile = {}
        self.mmo_stats = {}
        self.mmo_strategy = {}
        self.mmo_region_index = 0
        self.mmo_favorites = set()
        self.mmo_remote_positions = {}
        self.mmo_auto_agents = []
        self.mmo_influence = {}
        self.reputation_manager = DummyReputationManager()
        self.economy_manager = DummyEconomyManager()
        self.mmo_market_orders = []
        self.mmo_crafting_queue = []
        self.mmo_world_events = []
        self.mmo_campaigns_active = []
        self.mmo_campaign_sequence = 0
        self.mmo_training_queue = []
        self.mmo_projects = []
        self.mmo_contracts = []
        self.mmo_operations = []
        self.mmo_bounties = []
        self.mmo_directives = []
        self.mmo_guilds = []
        self.mmo_expeditions = []
        self.mmo_auto_dev_interval = 10000
        self.mmo_last_auto_dev_tick = 0
        self.mmo_last_shipment_auto = 0
        self.mmo_auto_dev_shipment_cooldown = 5000
        self.mmo_focus_region_threat = 0.0
        self.mmo_ai_seed = 42
        self.mmo_credits = 0
        self.mmo_message = ""
        self.mmo_event_log = []
        self.mmo_event_log_limit = 20
        self.mmo_notifications = []
        self.mmo_world_tick_interval = 1000
        self.mmo_last_world_tick = 0
        self.mmo_market_items = []
        self.mmo_infra_index = 0
        self.mmo_patrol_index = 0
        self.mmo_waypoint = None
        self.mmo_projects_seeded = False

    def _mmo_log_event(self, message: str) -> None:
        self.mmo_event_log.append(message)

    def _mmo_notify(self, message: str, *, level: str = "info") -> None:
        self.mmo_notifications.append({"text": message, "level": level})

    def _mmo_flash_notice(self, message: str, *, color=(200, 200, 200)) -> None:
        self.mmo_notifications.append({"text": message, "color": color})

    def _mmo_add_alert(self, message: str, *, level: str = "warn") -> None:
        self.mmo_notifications.append({"text": message, "level": level})

    def _mmo_prune_alerts(self, now: int) -> None:
        return None


class DummyPresence:
    def __init__(self) -> None:
        self.positions = {}
        self.last_seen = {}


class DummyShardGame(GameMMOLogic):
    def __init__(self) -> None:
        self.mmo_shard_id = "shard-1"
        self.mmo_shard_selected = True
        self.mmo_world_state = MMOWorldStateManager()
        self.mmo_world_state_cache = {}
        self.mmo_shard_cache_ttl_ms = 120000
        self.mmo_world_tombstones = []
        self.mmo_influence = {}
        self.mmo_world_events = []
        self.mmo_outposts = []
        self.mmo_operations = []
        self.mmo_trade_routes = []
        self.mmo_directives = []
        self.mmo_bounties = []
        self.mmo_presence = DummyPresence()
        self.mmo_remote_states = {}
        self.mmo_match_group = None
        self.mmo_match_status = "idle"
        self.mmo_match_id = None
        self.mmo_message = ""
        self.mmo_verifier = None
        self.world_generation_manager = DummyWorldGenerationManager([])
        self._joined = False
        self._snapshot_requested = False
        self._world_snapshot_requested = False

    def _mmo_leave_match(self) -> None:
        self.mmo_match_status = "idle"

    def _mmo_network_leave(self) -> None:
        self._joined = False

    def _mmo_network_join(self) -> None:
        self._joined = True

    def _request_mmo_snapshot(self) -> None:
        self._snapshot_requested = True

    def _request_mmo_world_snapshot(self) -> None:
        self._world_snapshot_requested = True

    def _apply_mmo_world_state(self, state: dict[str, object]) -> None:
        regions = state.get("regions")
        if isinstance(regions, list):
            self.world_generation_manager.region_manager.set_regions(
                [dict(region) for region in regions if isinstance(region, dict)]
            )
        influence = state.get("influence")
        if isinstance(influence, dict):
            self.mmo_influence = dict(influence)
        self.mmo_world_events = list(state.get("world_events") or [])
        self.mmo_outposts = list(state.get("outposts") or [])
        self.mmo_operations = list(state.get("operations") or [])
        self.mmo_trade_routes = list(state.get("trade_routes") or [])
        self.mmo_directives = list(state.get("directives") or [])
        self.mmo_bounties = list(state.get("bounties") or [])


def test_region_distance_handles_missing_position():
    game = DummyGame(regions=[])
    region = {"name": "Nowhere"}
    assert game._mmo_region_distance(region, (0.0, 0.0)) == float("inf")


def test_region_resources_are_cached():
    game = DummyGame(regions=[])
    region = {"name": "Aurora", "seed": "seed-1"}
    first = game._mmo_region_resources(region)
    second = game._mmo_region_resources(region)
    assert first == second
    assert game.mmo_resource_cache["seed-1"] == first


def test_region_threat_includes_event_severity():
    region = {"name": "Citadel", "recommended_level": 2, "feature": {"type": "ruins"}}
    game = DummyGame(regions=[region])
    game.mmo_world_events = [{"region": "Citadel", "severity": "high"}]
    assert game._mmo_region_threat(region) == 5.5


def test_regions_sort_by_distance_and_filter():
    regions = [
        {"name": "Alpha", "position": [0, 0], "biome": "forest"},
        {"name": "Bravo", "position": [3, 0], "biome": "plains"},
    ]
    game = DummyGame(regions=regions, player_pos=(0.0, 0.0))
    game.mmo_sort_mode = "distance"
    game.mmo_biome_filter = "all"
    sorted_regions = game._mmo_regions()
    assert [r["name"] for r in sorted_regions] == ["Alpha", "Bravo"]
    game.mmo_biome_filter = "forest"
    filtered = game._mmo_regions()
    assert [r["name"] for r in filtered] == ["Alpha"]


def test_threat_trend_rising():
    game = DummyGame(regions=[])
    game.mmo_threat_history = {"Alpha": [2.0, 2.6, 3.2]}
    assert game._mmo_threat_trend("Alpha") == "Rising"


def test_market_order_expiration_refunds_sell():
    game = DummyGame(regions=[])
    game.mmo_stockpile = {}
    game.mmo_market_orders = [
        {
            "kind": "sell",
            "quantity": 5,
            "price": 3,
            "resource": "Aether Ore",
            "status": "open",
            "eta": 5,
            "expires_in": 1,
        }
    ]
    game._mmo_market_tick()
    assert game.mmo_market_orders[0]["status"] == "expired"
    assert game.mmo_stockpile["Aether Ore"] == 5


def test_market_order_expiration_refunds_buy():
    game = DummyGame(regions=[])
    game.mmo_credits = 0
    game.mmo_market_orders = [
        {
            "kind": "buy",
            "quantity": 4,
            "price": 7,
            "resource": "Sunsteel",
            "status": "open",
            "eta": 5,
            "expires_in": 1,
        }
    ]
    game._mmo_market_tick()
    assert game.mmo_market_orders[0]["status"] == "expired"
    assert game.mmo_credits == 28


def test_cancel_open_order_refunds_sell():
    game = DummyGame(regions=[])
    game.mmo_stockpile = {}
    game.mmo_market_orders = [
        {
            "kind": "sell",
            "quantity": 3,
            "price": 4,
            "resource": "Crystal",
            "status": "open",
            "eta": 5,
            "expires_in": 6,
        }
    ]
    game._mmo_cancel_open_order()
    assert game.mmo_market_orders[0]["status"] == "cancelled"
    assert game.mmo_stockpile["Crystal"] == 3


def test_mmo_switch_shard_caches_world_state():
    game = DummyShardGame()
    snapshot = {
        "regions": [{"name": "Alpha"}],
        "influence": {"Alpha": 3},
        "world_events": [],
        "outposts": [],
        "operations": [],
        "trade_routes": [],
        "directives": [],
        "bounties": [],
        "tombstones": [],
        "updated_at": 10,
        "shard": "shard-1",
    }
    game.mmo_world_state.load_snapshot(snapshot, sequence=4)
    game._apply_mmo_world_state(snapshot)
    game._mmo_switch_shard("shard-2", reason="Switched to")
    assert "shard-1" in game.mmo_world_state_cache
    assert game.mmo_shard_id == "shard-2"
    assert game.world_generation_manager.region_manager.get_regions() == []
    assert game._world_snapshot_requested is True


def test_mmo_switch_shard_restores_cached_state():
    game = DummyShardGame()
    cached = {
        "regions": [{"name": "Beta"}],
        "influence": {"Beta": 5},
        "world_events": [],
        "outposts": [],
        "operations": [],
        "trade_routes": [],
        "directives": [],
        "bounties": [],
        "tombstones": [],
        "updated_at": 12,
        "shard": "shard-2",
    }
    game.mmo_world_state_cache["shard-2"] = {
        "state": cached,
        "seq": 2,
        "tombstones": [],
    }
    game._mmo_switch_shard("shard-2", reason="Switched to")
    regions = game.world_generation_manager.region_manager.get_regions()
    assert regions and regions[0]["name"] == "Beta"
    assert game.mmo_influence["Beta"] == 5


def test_mmo_shard_cache_ttl_expires_entries():
    game = DummyShardGame()
    game.mmo_shard_cache_ttl_ms = 1
    game.mmo_world_state_cache["shard-2"] = {
        "state": {"regions": [], "influence": {}, "shard": "shard-2"},
        "seq": 1,
        "tombstones": [],
        "cached_at": 0,
    }
    assert game._mmo_restore_world_state("shard-2") is False
