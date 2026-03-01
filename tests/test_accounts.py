"""Tests for accounts."""

import os
import sys
import pytest

pygame = pytest.importorskip("pygame")

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum import (
    load_accounts,
    register_account,
    delete_account,
    AccountsManager,
    renew_key,
    load_private_key,
)


def test_register_and_delete_account(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    path = tmp_path / 'a.json'
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', path)
    from hololive_coliseum import accounts as acc_mod
    acc_mod._DEFAULT_MANAGER.path = path
    os.makedirs(tmp_path, exist_ok=True)
    register_account('alice', 'user', 'PUB')
    assert load_accounts() == {'alice': {'level': 'user', 'public_key': 'PUB'}}
    delete_account('alice')
    assert load_accounts() == {}


def test_execute_account_option(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    path = tmp_path / 'b.json'
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', path)
    from hololive_coliseum import accounts as acc_mod
    acc_mod._DEFAULT_MANAGER.path = path
    from hololive_coliseum.game import Game

    game = Game()
    game.account_id = 'bob'
    game.execute_account_option('Register Account')
    assert load_accounts() == {'bob': {'level': 'user', 'public_key': 'PUBKEY'}}
    game.execute_account_option('Delete Account')
    assert load_accounts() == {}
    pygame.quit()


def test_accounts_manager_class(tmp_path, monkeypatch):
    path = tmp_path / 'c.json'
    mgr = AccountsManager(path)
    mgr.register('id', 'admin', 'KEY')
    assert mgr.load() == {'id': {'level': 'admin', 'public_key': 'KEY'}}
    assert mgr.get('id')['public_key'] == 'KEY'
    mgr.delete('id')
    assert mgr.load() == {}


def test_renew_key_updates_registry(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    path = tmp_path / 'd.json'
    key_fmt = str(tmp_path / '{}_key.pem')
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', path)
    monkeypatch.setattr('hololive_coliseum.accounts.KEY_FILE_FMT', key_fmt)
    from hololive_coliseum import accounts as acc_mod
    acc_mod._DEFAULT_MANAGER.path = path

    register_account('alice', 'user', 'OLD')
    priv = renew_key('alice')
    data = load_accounts()
    assert 'alice' in data and data['alice']['public_key'].startswith('-----BEGIN')
    priv2 = load_private_key('alice')
    assert priv2 == priv
