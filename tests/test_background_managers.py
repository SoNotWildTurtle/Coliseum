"""Tests for background managers."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.script_manager import ScriptManager
from hololive_coliseum.localization_manager import LocalizationManager
from hololive_coliseum.resource_manager import ResourceManager
from hololive_coliseum.cluster_manager import ClusterManager
from hololive_coliseum.matchmaking_manager import MatchmakingManager
from hololive_coliseum.load_balancer_manager import LoadBalancerManager
from hololive_coliseum.migration_manager import MigrationManager
from hololive_coliseum.billing_manager import BillingManager
from hololive_coliseum.ad_manager import AdManager
from hololive_coliseum.api_manager import APIManager
from hololive_coliseum.support_manager import SupportManager


def test_script_manager_basic():
    sm = ScriptManager()
    sm.add_script("start", "print('hi')")
    assert sm.get_script("start") == "print('hi')"
    sm.remove_script("start")
    assert sm.get_script("start") is None


def test_localization_and_resources():
    lm = LocalizationManager()
    lm.set("es", "hello", "hola")
    assert lm.translate("hello", "es") == "hola"
    rm = ResourceManager()
    loaded = rm.load("x", lambda p: p.upper())
    assert loaded == "X" and rm.load("x", lambda p: "y") == "X"


def test_cluster_matchmaking_balance_and_migration():
    cm = ClusterManager()
    cm.register("s1")
    lb = LoadBalancerManager()
    lb.update_load("s1", 5)
    assert lb.best_server() == "s1"
    mm = MatchmakingManager()
    mm.join("p1")
    mm.join("p2")
    assert mm.match() == ["p1", "p2"]
    mig = MigrationManager()
    mig.request_transfer("p3", "s2")
    assert mig.complete_transfer("p3") == "s2"


def test_billing_ad_api_support():
    bm = BillingManager()
    bm.add_purchase("u", "sword")
    assert bm.get_purchases("u") == ["sword"]
    adm = AdManager()
    adm.add_ad("sale")
    assert adm.current_ads() == ["sale"]
    api = APIManager()
    api.add_endpoint("discord", "url")
    assert api.get("discord") == "url"
    sup = SupportManager()
    tid = sup.submit("help")
    assert sup.get(tid) == "help"
