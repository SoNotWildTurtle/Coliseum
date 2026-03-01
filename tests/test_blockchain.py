"""Tests for blockchain."""

import os
import sys
import json
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum import (
    load_chain,
    save_chain,
    add_game,
    search,
    add_contract,
    fulfill_contract,
    load_balances,
    verify_chain,
    merge_chain,
    register_account,
    load_accounts,
    add_message,
    decrypt_message,
    admin_decrypt,
    add_region,
    hash_region,
    WorldRegionManager,
    WorldSeedManager,
    add_vote,
)


def test_add_and_search(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'accounts.json')

    register_account('alice', 'user', 'pubA')
    register_account('bob', 'user', 'pubB')
    block = add_game(['alice', 'bob'], 'alice', bet=5, game_id='g1')
    assert block['index'] == 0
    assert search(game_id='g1')[0]['winner'] == 'alice'

    balances = load_balances()
    assert balances['alice'] == 5
    assert balances['bob'] == -5
    from hololive_coliseum.blockchain import get_balance
    assert get_balance('alice') == 5
    assert get_balance('bob') == -5


def test_contract_flow(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'accounts.json')

    register_account('a', 'user', 'pubA')
    register_account('b', 'user', 'pubB')
    add_contract('req1', ['a', 'b'], 2)
    block = fulfill_contract('req1', 'b')
    assert block['game_id'] == 'req1'
    chain = load_chain()
    assert len(chain) == 2
    assert chain[0]['winner'] == 'b'


def test_verify_and_merge(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'accounts.json')

    register_account('a', 'user', 'pubA')
    register_account('b', 'user', 'pubB')
    block1 = add_game(['a'], 'a', game_id='g1')
    block2 = add_game(['a', 'b'], 'b', game_id='g2')
    remote = load_chain()
    # truncate local chain to first block
    save_chain([block1])
    assert verify_chain(remote)
    merge_chain(remote)
    assert load_chain() == remote


def test_message_encryption(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'accounts.json')

    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    admin_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    admin_pub = admin_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    user_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    user_pub = user_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    register_account('bob', 'user', user_pub.decode('ascii'))
    block = add_message('alice', 'bob', 'hello', admin_pub)

    msg_user = decrypt_message(block, user_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ))
    msg_admin = admin_decrypt(block, admin_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ))
    assert msg_user == 'hello'
    assert msg_admin == 'hello'


def test_region_blocks_store_hash(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    block = add_region({'name': 'r1', 'seed': 's'})
    expect = hash_region({'name': 'r1', 'seed': 's'})
    assert block['region_hash'] == expect
    chain = load_chain()
    chain[0]['region']['name'] = 'r2'
    save_chain(chain)
    assert not verify_chain(load_chain())


def test_signed_blocks(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'accounts.json')

    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    import base64

    a_key = ed25519.Ed25519PrivateKey.generate()
    b_key = ed25519.Ed25519PrivateKey.generate()
    a_pub = a_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    b_pub = b_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    register_account('alice', 'user', a_pub.decode('ascii'))
    register_account('bob', 'user', b_pub.decode('ascii'))

    block = add_game(
        ['alice', 'bob'],
        'alice',
        signing_keys={
            'alice': a_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            ),
            'bob': b_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            ),
        },
    )
    chain = load_chain()
    assert 'signatures' in block
    assert verify_chain(chain)

    signed_block = next(b for b in chain if 'signatures' in b)
    sig = signed_block['signatures']['alice']
    bad = base64.b64encode(base64.b64decode(sig)[::-1]).decode('ascii')
    chain[0]['signatures']['alice'] = bad
    assert not verify_chain(chain)


def test_add_seed_and_sync(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.world_seed_manager.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.world_seed_manager.SEED_FILE', tmp_path / 'seeds.json')

    from hololive_coliseum import add_seed, WorldSeedManager

    add_seed('deadbeef')
    mgr = WorldSeedManager()
    mgr.sync_with_blockchain()
    assert 'deadbeef' in mgr.get_seeds()


def test_add_region_and_sync(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.world_region_manager.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.world_region_manager.REGION_FILE', tmp_path / 'regions.json')

    add_region({'name': 'region_1', 'seed': 'deadbeef'})
    mgr = WorldRegionManager()
    mgr.sync_with_blockchain()
    assert any(r['name'] == 'region_1' for r in mgr.get_regions())


def test_game_result_creates_seed(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'accounts.json')
    monkeypatch.setattr('hololive_coliseum.world_seed_manager.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.world_seed_manager.SEED_FILE', tmp_path / 'seeds.json')

    register_account('alice', 'user', 'pubA')
    register_account('bob', 'user', 'pubB')
    block = add_game(['alice', 'bob'], 'alice')
    mgr = WorldSeedManager()
    mgr.sync_with_blockchain()
    assert block['hash'] in mgr.get_seeds()


def test_vote_block_and_characters(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'accounts.json')

    register_account('alice', 'user', 'pubA')
    add_game(['alice'], 'alice', characters=['Gura'])
    chain = load_chain()
    assert chain[1]['characters'] == ['Gura']
    add_vote('alice', 'expand')
    assert load_chain()[-1]['type'] == 'vote'
