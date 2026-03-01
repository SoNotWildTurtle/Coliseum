"""Tests for voting manager."""

import json
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum import blockchain, accounts, voting_manager
from hololive_coliseum.accounts import register_account
from hololive_coliseum.voting_manager import VotingManager


def test_vote_once_per_week(tmp_path, monkeypatch):
    monkeypatch.setattr(blockchain, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(blockchain, 'CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr(blockchain, 'BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr(blockchain, 'CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr(voting_manager, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(voting_manager, 'VOTE_FILE', tmp_path / 'votes.json')
    monkeypatch.setattr(accounts, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(accounts, 'ACCOUNTS_FILE', tmp_path / 'a.json')
    monkeypatch.setattr(accounts, 'KEY_FILE_FMT', str(tmp_path / '{}_key.pem'))

    register_account('alice', 'user', 'pub')
    blockchain.add_game(['alice'], 'alice', characters=['Gura'])
    vm = VotingManager()
    opts = vm.get_options()
    assert 'Gura' in opts
    vm.cast_vote('alice', 'Gura')
    assert not vm.can_vote('alice')
    with pytest.raises(ValueError):
        vm.cast_vote('alice', 'Gura')

    with open(voting_manager.VOTE_FILE, 'r', encoding='utf-8') as handle:
        stored = json.load(handle)
    assert 'character' in stored['alice']

    biome_vm = VotingManager(['forest'], category='biome')
    assert biome_vm.can_vote('alice')
    biome_vm.cast_vote('alice', 'forest')
    with pytest.raises(ValueError):
        biome_vm.cast_vote('alice', 'forest')

    with open(voting_manager.VOTE_FILE, 'r', encoding='utf-8') as handle:
        stored = json.load(handle)
    assert set(stored['alice']) == {'character', 'biome'}

    refreshed = VotingManager()
    assert not refreshed.can_vote('alice')


def test_get_winner_counts_votes(tmp_path, monkeypatch):
    monkeypatch.setattr(blockchain, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(blockchain, 'CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr(blockchain, 'BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr(blockchain, 'CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr(voting_manager, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(voting_manager, 'VOTE_FILE', tmp_path / 'votes.json')
    monkeypatch.setattr(accounts, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(accounts, 'ACCOUNTS_FILE', tmp_path / 'a.json')
    monkeypatch.setattr(accounts, 'KEY_FILE_FMT', str(tmp_path / '{}_key.pem'))

    register_account('alice', 'user', 'pub')
    register_account('bob', 'user', 'pub2')
    blockchain.add_vote('alice', 'Gura')
    blockchain.add_vote('bob', 'Ame')
    blockchain.add_vote('bob', 'Ame')
    vm = VotingManager()
    assert vm.get_winner() == 'Ame'


def test_biome_vote_counts(tmp_path, monkeypatch):
    monkeypatch.setattr(blockchain, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(blockchain, 'CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr(blockchain, 'BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr(blockchain, 'CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr(voting_manager, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(voting_manager, 'VOTE_FILE', tmp_path / 'votes.json')
    monkeypatch.setattr(accounts, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(accounts, 'ACCOUNTS_FILE', tmp_path / 'a.json')
    monkeypatch.setattr(accounts, 'KEY_FILE_FMT', str(tmp_path / '{}_key.pem'))

    register_account('alice', 'user', 'pub')
    blockchain.add_vote('alice', 'forest', category='biome')
    vm = VotingManager(['forest', 'desert'], category='biome')
    assert vm.get_winner() == 'forest'


def test_vote_file_backward_compatible(tmp_path, monkeypatch):
    monkeypatch.setattr(blockchain, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(blockchain, 'CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr(blockchain, 'BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr(blockchain, 'CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr(voting_manager, 'SAVE_DIR', tmp_path)
    votes_path = tmp_path / 'votes.json'
    monkeypatch.setattr(voting_manager, 'VOTE_FILE', votes_path)
    votes_path.write_text(json.dumps({'alice': int(time.time())}))

    vm = VotingManager()
    assert not vm.can_vote('alice')

    biome_vm = VotingManager(['forest'], category='biome')
    assert biome_vm.can_vote('alice')
