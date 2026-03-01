"""Tests for saving and loading iteration snapshots."""

import json
from hololive_coliseum.iteration_manager import IterationManager


def test_save_and_load_iteration(tmp_path):
    mgr = IterationManager(directory=str(tmp_path))
    path = mgr.save({"score": 42})
    assert path in mgr.list()
    data = mgr.load(path)
    assert data["score"] == 42
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    assert raw == data
