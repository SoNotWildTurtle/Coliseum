"""Tests for the WorldRegionManager's blockchain sync."""

from hololive_coliseum import (
    WorldRegionManager,
    add_region,
    load_chain,
    save_chain,
)


def test_sync_skips_regions_with_bad_hash(tmp_path, monkeypatch):
    monkeypatch.setattr(
        'hololive_coliseum.world_region_manager.SAVE_DIR',
        tmp_path,
    )
    monkeypatch.setattr(
        'hololive_coliseum.world_region_manager.REGION_FILE',
        tmp_path / 'regions.json',
    )
    monkeypatch.setattr(
        'hololive_coliseum.blockchain.SAVE_DIR',
        tmp_path,
    )
    monkeypatch.setattr(
        'hololive_coliseum.blockchain.CHAIN_FILE',
        tmp_path / 'c.json',
    )
    add_region({'name': 'r1', 'seed': 's'})
    chain = load_chain()
    chain[0]['region']['name'] = 'evil'
    save_chain(chain)
    mgr = WorldRegionManager()
    mgr.sync_with_blockchain()
    assert mgr.get_regions() == []
