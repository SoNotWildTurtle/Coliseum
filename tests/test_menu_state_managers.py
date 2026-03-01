"""Tests for menu state managers."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.menu_manager import MenuManager
from hololive_coliseum.game_state_manager import GameStateManager


def test_menu_manager_wraps():
    mgr = MenuManager()
    mgr.move(1, 3)
    assert mgr.index == 1
    mgr.move(-1, 3)
    assert mgr.index == 0
    mgr.move(-1, 3)
    assert mgr.index == 2


def test_game_state_manager_change_and_revert():
    mgr = GameStateManager("a")
    mgr.change("b")
    assert mgr.state == "b" and mgr.previous == "a"
    mgr.revert()
    assert mgr.state == "a"
