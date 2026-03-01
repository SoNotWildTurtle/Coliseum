"""Blockchain-related gameplay utilities."""

import json
import os
import time
import uuid
import hashlib
import base64
from typing import Any, Dict, List

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from .accounts import get_account

# Path to SavedGames directory used by save_manager
SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'SavedGames')
os.makedirs(SAVE_DIR, exist_ok=True)
CHAIN_FILE = os.path.join(SAVE_DIR, 'chain.json')
BALANCE_FILE = os.path.join(SAVE_DIR, 'balances.json')
CONTRACT_FILE = os.path.join(SAVE_DIR, 'contracts.json')

# simple proof-of-work difficulty: number of leading zeros required
DIFFICULTY = 2


def _load_json(path: str, default: Any) -> Any:
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return default
    return default


def _save_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def load_chain() -> List[Dict[str, Any]]:
    """Return the saved blockchain."""
    return _load_json(CHAIN_FILE, [])


def save_chain(chain: List[Dict[str, Any]]) -> None:
    _save_json(CHAIN_FILE, chain)


def load_balances() -> Dict[str, int]:
    return _load_json(BALANCE_FILE, {})


def save_balances(data: Dict[str, int]) -> None:
    _save_json(BALANCE_FILE, data)


def get_balance(user_id: str) -> int:
    """Return the stored balance for ``user_id`` or ``0`` if missing."""
    balances = load_balances()
    return balances.get(user_id, 0)




def _hash_block(data: Dict[str, Any]) -> str:
    raw = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def hash_region(region: Dict[str, Any]) -> str:
    """Return a deterministic hash for ``region``."""

    raw = json.dumps(region, sort_keys=True).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def _mine_block(block: Dict[str, Any]) -> None:
    """Find a nonce so the block hash starts with ``DIFFICULTY`` zeros."""
    nonce = 0
    while True:
        block['nonce'] = nonce
        h = _hash_block(block)
        if h.startswith('0' * DIFFICULTY):
            block['hash'] = h
            return
        nonce += 1


def mine_dummy_block(difficulty: int = 1) -> Dict[str, Any]:
    """Return a mined dummy block header with adjustable difficulty.

    This helper performs proof-of-work without altering the saved chain and is
    used by the :class:`MiningManager` when players volunteer spare CPU time to
    generate data for future MMORPG content.
    """
    block: Dict[str, Any] = {
        'index': 0,
        'prev_hash': '',
        'timestamp': int(time.time()),
    }
    nonce = 0
    while True:
        block['nonce'] = nonce
        h = _hash_block(block)
        if h.startswith('0' * difficulty):
            block['hash'] = h
            return block
        nonce += 1


def add_seed(seed: str) -> Dict[str, Any]:
    """Append ``seed`` as a block so peers can share world seeds."""

    chain = load_chain()
    prev_hash = chain[-1]['hash'] if chain else ''
    block = {
        'index': len(chain),
        'type': 'seed',
        'seed': seed,
        'timestamp': int(time.time()),
        'prev_hash': prev_hash,
    }
    _mine_block(block)
    chain.append(block)
    save_chain(chain)
    return block


def add_region(region: Dict[str, Any]) -> Dict[str, Any]:
    """Append ``region`` as a block so peers share generated areas."""

    chain = load_chain()
    prev_hash = chain[-1]['hash'] if chain else ''
    block = {
        'index': len(chain),
        'type': 'region',
        'region': region,
        'region_hash': hash_region(region),
        'timestamp': int(time.time()),
        'prev_hash': prev_hash,
    }
    _mine_block(block)
    chain.append(block)
    save_chain(chain)
    return block


def add_game(
    players: List[str],
    winner: str,
    bet: int = 0,
    game_id: str | None = None,
    signing_keys: Dict[str, bytes] | None = None,
    *,
    characters: List[str] | None = None,
) -> Dict[str, Any]:
    """Append a new game result and update balances.

    Each ``player`` must exist in the account registry or a ``ValueError`` is
    raised. When ``signing_keys`` are supplied each player signs the block
    contents so peers can verify their participation. After recording the game
    a second ``seed`` block is added using the game block's hash so future MMO
    world generation can derive regions from match history.
    ``characters`` can list the avatar used by each player so seed blocks
    capture roster usage for later voting.
    """
    for p in players:
        if get_account(p) is None:
            raise ValueError(f"unknown account: {p}")
    chain = load_chain()
    prev_hash = chain[-1]['hash'] if chain else ''
    if game_id is None:
        game_id = uuid.uuid4().hex
    block = {
        'index': len(chain),
        'game_id': game_id,
        'players': players,
        'winner': winner,
        'bet': bet,
        'timestamp': int(time.time()),
        'prev_hash': prev_hash,
    }
    if characters is not None:
        block['characters'] = characters
    unsigned = block.copy()
    signatures: Dict[str, str] = {}
    if signing_keys:
        payload = json.dumps(unsigned, sort_keys=True).encode('utf-8')
        for uid, priv_pem in signing_keys.items():
            key = serialization.load_pem_private_key(priv_pem, password=None)
            sig = key.sign(payload)
            signatures[uid] = base64.b64encode(sig).decode('ascii')
    if signatures:
        block['signatures'] = signatures
    _mine_block(block)
    chain.append(block)

    seed_block = {
        'index': len(chain),
        'type': 'seed',
        'seed': block['hash'],
        'timestamp': int(time.time()),
        'prev_hash': block['hash'],
    }
    if characters is not None:
        seed_block['characters'] = characters
    _mine_block(seed_block)
    chain.append(seed_block)
    save_chain(chain)

    if bet:
        balances = load_balances()
        for p in players:
            balances[p] = balances.get(p, 0) - bet
        balances[winner] = balances.get(winner, 0) + bet * len(players)
        save_balances(balances)
    return block


def add_vote(account_id: str, choice: str, category: str = "character") -> Dict[str, Any]:
    """Record a weekly vote on the blockchain.

    ``category`` allows multiple vote types to coexist, such as character or
    biome selections.
    """

    if get_account(account_id) is None:
        raise ValueError(f"unknown account: {account_id}")
    chain = load_chain()
    prev_hash = chain[-1]['hash'] if chain else ''
    block = {
        'index': len(chain),
        'type': 'vote',
        'account': account_id,
        'choice': choice,
        'category': category,
        'timestamp': int(time.time()),
        'prev_hash': prev_hash,
    }
    _mine_block(block)
    chain.append(block)
    save_chain(chain)
    return block


def search(game_id: str | None = None, user_id: str | None = None) -> List[Dict[str, Any]]:
    """Search blocks by game ID and/or user ID."""
    chain = load_chain()
    results = chain
    if game_id is not None:
        results = [b for b in results if b.get('game_id') == game_id]
    if user_id is not None:
        results = [b for b in results if user_id in b.get('players', [])]
    return results


def add_contract(request_id: str, players: List[str], bet: int) -> None:
    contracts = _load_json(CONTRACT_FILE, {})
    contracts[request_id] = {'players': players, 'bet': bet}
    _save_json(CONTRACT_FILE, contracts)


def fulfill_contract(request_id: str, winner: str) -> Dict[str, Any] | None:
    contracts = _load_json(CONTRACT_FILE, {})
    contract = contracts.pop(request_id, None)
    if contract is None:
        return None
    _save_json(CONTRACT_FILE, contracts)
    return add_game(contract['players'], winner, contract['bet'], game_id=request_id)


def verify_chain(chain: List[Dict[str, Any]]) -> bool:
    """Return ``True`` if hashes and signatures are valid."""
    prev_hash = ''
    for block in chain:
        unsigned = {k: block[k] for k in block if k not in ('hash', 'signatures', 'nonce')}
        data_for_hash = {k: block[k] for k in block if k != 'hash'}
        expect = _hash_block(data_for_hash)
        if (
            block.get('prev_hash') != prev_hash
            or block.get('hash') != expect
            or not expect.startswith('0' * DIFFICULTY)
        ):
            return False
        if block.get('type') == 'region':
            region = block.get('region')
            if hash_region(region) != block.get('region_hash'):
                return False
        sigs = block.get('signatures', {})
        payload = json.dumps(unsigned, sort_keys=True).encode('utf-8')
        for uid, sig_b64 in sigs.items():
            acc = get_account(uid)
            if acc is None:
                return False
            pub = serialization.load_pem_public_key(acc['public_key'].encode('utf-8'))
            try:
                pub.verify(base64.b64decode(sig_b64), payload)
            except InvalidSignature:
                return False
        prev_hash = block['hash']
    return True


def merge_chain(remote: List[Dict[str, Any]]) -> None:
    """Merge a remote chain with the local one if it is valid and longer."""
    if not verify_chain(remote):
        return
    local = load_chain()
    if len(remote) > len(local):
        save_chain(remote)


def add_message(
    sender: str,
    recipient: str,
    message: str,
    admin_public_key_pem: bytes,
) -> Dict[str, Any]:
    """Encrypt ``message`` for ``recipient`` and append it as a block.

    The message is encrypted with a random symmetric key. That key is encrypted
    twice: once with the recipient's public key and once with the admin key so
    moderators can decrypt abusive messages if necessary.
    """
    recipient_info = get_account(recipient)
    if recipient_info is None:
        raise ValueError("unknown recipient")

    rec_pub = serialization.load_pem_public_key(
        recipient_info["public_key"].encode("utf-8")
    )
    admin_pub = serialization.load_pem_public_key(admin_public_key_pem)

    sym_key = Fernet.generate_key()
    cipher = Fernet(sym_key).encrypt(message.encode("utf-8"))

    enc_rec = rec_pub.encrypt(
        sym_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    enc_admin = admin_pub.encrypt(
        sym_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )

    chain = load_chain()
    prev_hash = chain[-1]["hash"] if chain else ""
    block = {
        "index": len(chain),
        "type": "message",
        "sender": sender,
        "recipient": recipient,
        "cipher": base64.b64encode(cipher).decode("ascii"),
        "key_user": base64.b64encode(enc_rec).decode("ascii"),
        "key_admin": base64.b64encode(enc_admin).decode("ascii"),
        "timestamp": int(time.time()),
        "prev_hash": prev_hash,
    }
    _mine_block(block)
    chain.append(block)
    save_chain(chain)
    return block


def decrypt_message(block: Dict[str, Any], private_key_pem: bytes) -> str:
    """Return the plaintext of ``block`` using the recipient's private key."""
    if block.get("type") != "message":
        raise ValueError("not a message block")
    priv = serialization.load_pem_private_key(private_key_pem, password=None)
    sym_key = priv.decrypt(
        base64.b64decode(block["key_user"]),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    return Fernet(sym_key).decrypt(base64.b64decode(block["cipher"])).decode("utf-8")


def admin_decrypt(block: Dict[str, Any], admin_private_key_pem: bytes) -> str:
    """Decrypt a message block using the admin private key."""
    if block.get("type") != "message":
        raise ValueError("not a message block")
    priv = serialization.load_pem_private_key(admin_private_key_pem, password=None)
    sym_key = priv.decrypt(
        base64.b64decode(block["key_admin"]),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    return Fernet(sym_key).decrypt(base64.b64decode(block["cipher"])).decode("utf-8")
