"""Tests for the StateSync helper."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.state_sync import StateSync

def test_state_sync_tolerance():
    sync = StateSync(tolerances={'x': 0.5})
    delta1 = sync.encode({'x': 0.0})
    assert delta1['x'] == 0.0
    delta2 = sync.encode({'x': 0.2})
    assert 'x' not in delta2
    delta3 = sync.encode({'x': 1.0})
    assert delta3['x'] == 1.0
