"""Tests for accessibility manager."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.accessibility_manager import AccessibilityManager


def test_toggle_colorblind():
    mgr = AccessibilityManager()
    assert not mgr.options["colorblind"]
    mgr.toggle("colorblind")
    assert mgr.options["colorblind"]
