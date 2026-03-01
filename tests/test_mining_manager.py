"""Tests for mining manager."""

import time
from hololive_coliseum.mining_manager import MiningManager


def test_mining_manager_runs():
    mgr = MiningManager()
    mgr.start(intensity=1.0)
    time.sleep(0.02)
    mgr.stop()
    assert mgr.mined >= 1


def test_mining_manager_records_seeds(tmp_path, monkeypatch):
    import hololive_coliseum.world_seed_manager as wsm

    monkeypatch.setattr(wsm, "SAVE_DIR", tmp_path)
    monkeypatch.setattr(wsm, "SEED_FILE", tmp_path / "seeds.json")
    seed_mgr = wsm.WorldSeedManager()
    miner = MiningManager(seed_manager=seed_mgr)
    miner.start(intensity=1.0)
    time.sleep(0.02)
    miner.stop()
    assert seed_mgr.get_seeds(), "expected at least one recorded seed"


def test_mining_manager_generates_regions(tmp_path, monkeypatch):
    import hololive_coliseum.world_seed_manager as wsm
    import hololive_coliseum.world_region_manager as wrm
    import hololive_coliseum.world_generation_manager as wgm

    monkeypatch.setattr(wsm, "SAVE_DIR", tmp_path)
    monkeypatch.setattr(wsm, "SEED_FILE", tmp_path / "seeds.json")
    monkeypatch.setattr(wrm, "SAVE_DIR", tmp_path)
    monkeypatch.setattr(wrm, "REGION_FILE", tmp_path / "regions.json")
    world_gen = wgm.WorldGenerationManager()
    miner = MiningManager(world_gen=world_gen)
    miner.start(intensity=1.0)
    time.sleep(0.02)
    miner.stop()
    assert world_gen.region_manager.get_regions(), "expected a generated region"
