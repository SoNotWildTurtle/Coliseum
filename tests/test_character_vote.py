"""Tests for character vote."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum import (
    game as game_module,
    blockchain,
    accounts,
    voting_manager,
    save_manager,
)
from hololive_coliseum.game import Game, load_character_names
from hololive_coliseum.accounts import register_account
from hololive_coliseum.player import character_class_exists, get_player_class


def test_load_character_names(tmp_path, monkeypatch):
    doc = tmp_path / "DEV_PLAN_CHARACTERS.md"
    doc.write_text("- **Foo**: ability\n- **Bar**: ability\n")
    monkeypatch.setattr(game_module, "CHARACTER_PLAN_FILE", doc)
    assert load_character_names() == ["Foo", "Bar"]


def test_menu_vote_required(tmp_path, monkeypatch):
    pytest.importorskip("pygame")
    monkeypatch.setattr(blockchain, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(blockchain, 'CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr(blockchain, 'BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr(blockchain, 'CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr(voting_manager, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(voting_manager, 'VOTE_FILE', tmp_path / 'v.json')
    monkeypatch.setattr(accounts, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(accounts, 'ACCOUNTS_FILE', tmp_path / 'a.json')
    register_account('p', 'user', 'pub')
    g = Game()
    g.account_id = 'p'
    g.selected_character = g.characters[0]
    g._setup_level()
    assert hasattr(g, 'apply_vote_balancing')
    assert not hasattr(g, '_cast_character_vote')
    assert g.voting_manager.can_vote('p')
    options = g.voting_manager.get_options()
    if not options:
        options = [g.characters[0]]
    g.voting_manager.cast_vote('p', options[0])
    assert not g.voting_manager.can_vote('p')


def test_unknown_character_filtered(tmp_path, monkeypatch):
    pytest.importorskip("pygame")
    doc = tmp_path / "DEV_PLAN_CHARACTERS.md"
    doc.write_text("- **Foo**: ability\n")
    monkeypatch.setattr(game_module, "CHARACTER_PLAN_FILE", doc)
    monkeypatch.setattr(save_manager, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(accounts, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(accounts, 'ACCOUNTS_FILE', tmp_path / 'a.json')
    monkeypatch.setattr(accounts, 'KEY_FILE_FMT', str(tmp_path / '{}_key.pem'))
    g = Game()
    assert character_class_exists("Gawr Gura")
    assert "Foo" not in g.characters
    assert not character_class_exists("Foo")


def test_vote_balancing_modifies_stats(tmp_path, monkeypatch):
    pytest.importorskip("pygame")
    monkeypatch.setattr(blockchain, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(blockchain, 'CHAIN_FILE', tmp_path / 'chain.json')
    monkeypatch.setattr(blockchain, 'BALANCE_FILE', tmp_path / 'balances.json')
    monkeypatch.setattr(blockchain, 'CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr(voting_manager, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(voting_manager, 'VOTE_FILE', tmp_path / 'votes.json')
    monkeypatch.setattr(accounts, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(accounts, 'ACCOUNTS_FILE', tmp_path / 'accounts.json')
    monkeypatch.setattr(accounts, 'KEY_FILE_FMT', str(tmp_path / '{}_key.pem'))

    register_account('p', 'user', 'pubp')
    register_account('a', 'user', 'puba')
    register_account('b', 'user', 'pubb')

    g = Game()
    assert len(g.characters) >= 2
    low = g.characters[0]
    high = g.characters[1]

    blockchain.add_vote('a', high)
    blockchain.add_vote('b', high)

    g.account_id = 'p'

    g.selected_character = low
    g._setup_level()
    base_low = get_player_class(low)(0, 0, None)
    assert g.vote_adjustments[low] >= 0
    assert g.player.stats.get('attack') >= base_low.stats.get('attack')

    g.selected_character = high
    g._setup_level()
    base_high = get_player_class(high)(0, 0, None)
    assert g.vote_adjustments[high] <= 0
    assert g.player.stats.get('attack') <= base_high.stats.get('attack')


def test_vote_balancing_no_votes_keeps_stats(tmp_path, monkeypatch):
    pytest.importorskip("pygame")
    monkeypatch.setattr(blockchain, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(blockchain, 'CHAIN_FILE', tmp_path / 'chain.json')
    monkeypatch.setattr(blockchain, 'BALANCE_FILE', tmp_path / 'balances.json')
    monkeypatch.setattr(blockchain, 'CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr(voting_manager, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(voting_manager, 'VOTE_FILE', tmp_path / 'votes.json')
    monkeypatch.setattr(accounts, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(accounts, 'ACCOUNTS_FILE', tmp_path / 'accounts.json')
    monkeypatch.setattr(accounts, 'KEY_FILE_FMT', str(tmp_path / '{}_key.pem'))

    g = Game()
    name = g.characters[0]
    base = get_player_class(name)(0, 0, None)

    g.selected_character = name
    g._setup_level()

    assert g.vote_adjustments[name] == 0
    assert g.player.stats.get('attack') == base.stats.get('attack')
    assert g.player.stats.get('defense') == base.stats.get('defense')
    assert g.player.stats.get('max_health') == base.stats.get('max_health')
