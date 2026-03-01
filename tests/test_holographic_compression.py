"""Tests for holographic compression."""

import json
from cryptography.hazmat.primitives.asymmetric import ed25519
from hololive_coliseum.holographic_compression import (
    compress_packet,
    decompress_packet,
)


def test_compress_roundtrip():
    msg = {"type": "demo", "value": 42}
    packet = compress_packet(msg)
    out = decompress_packet(packet)
    assert out == msg


def test_compress_encrypt_roundtrip():
    msg = {"type": "demo", "value": 43}
    key = b"key"
    packet = compress_packet(msg, key)
    wrapper = json.loads(packet.decode("utf-8"))
    assert "n" in wrapper
    out = decompress_packet(packet, key)
    assert out == msg


def test_wrong_key_returns_none():
    msg = {"type": "demo", "value": 44}
    packet = compress_packet(msg, b"a")
    assert decompress_packet(packet, b"b") is None


def test_compress_custom_level():
    msg = {"t": 1}
    packet = compress_packet(msg, level=9)
    out = decompress_packet(packet)
    assert out == msg


def test_compress_lzma_algorithm():
    msg = {"x": 2}
    packet = compress_packet(msg, algorithm="lzma")
    out = decompress_packet(packet)
    assert out == msg


def test_compress_bz2_algorithm():
    msg = {"x": 3}
    packet = compress_packet(msg, algorithm="bz2")
    out = decompress_packet(packet)
    assert out == msg


def test_auto_algorithm_roundtrip():
    msg = {"x": 4}
    packet = compress_packet(msg, algorithm="auto")
    wrapper = json.loads(packet.decode("utf-8"))
    assert wrapper["alg"] in {"zlib", "lzma"}
    assert decompress_packet(packet) == msg


def test_anchor_points_present():
    msg = {"hello": "world"}
    packet = compress_packet(msg)
    wrapper = json.loads(packet.decode("utf-8"))
    anchors = wrapper.get("p")
    assert isinstance(anchors, list) and len(anchors) == 4
    layers = wrapper.get("layers")
    assert isinstance(layers, list) and len(layers) >= 1
    expected = [
        ([0, 0, 1], "cyan"),
        ([0, 0, 0], "white"),
        ([1, 1, 1], "black"),
        ([1, 1, 0], "red"),
    ]
    for anchor, (pos, color) in zip(anchors, expected):
        assert anchor["pos"] == pos
        assert anchor["color"] == color
        assert "vparam" in anchor
        for key in ("size", "lum", "bw"):
            assert key in anchor
    for layer in layers:
        assert "hash" in layer and layer["hash"]
        assert "density" in layer
        assert "virtual_channel" in layer
        assert "energy" in layer
    spectral = wrapper.get("spectral")
    assert spectral["entropy"] >= 0.0
    assert spectral["diversity"] >= 0.0
    phase = wrapper.get("phase")
    assert phase["coherence"] >= 0.0
    assert -1.0 <= phase["phase"] <= 1.0
    assert "anchor_quality" in wrapper
    channel_map = wrapper.get("channel_map")
    assert channel_map["layer_count"] == len(layers)
    assert "coherence" in channel_map
    assert "stability_index" in channel_map
    vectors = wrapper.get("channel_vectors")
    assert vectors["coherence"] == phase["coherence"]
    triangulation = wrapper.get("triangulation")
    assert triangulation["origin"] == [0, 0, 0]
    assert triangulation["axes"]
    assert wrapper.get("anchor_vectors")
    assert wrapper.get("vparam_map")
    profile = wrapper.get("bandwidth_profile")
    assert profile["payload_bytes"] >= 0.0
    assert profile["peak_layer"] <= profile["payload_bytes"] + 1
    assert profile["entropy"] == spectral["entropy"]
    telemetry = wrapper.get("telemetry_signature")
    assert telemetry["layer_hashes"]
    assert "anchor_stability" in wrapper


def test_signature_roundtrip():
    msg = {"k": 5}
    key = ed25519.Ed25519PrivateKey.generate()
    packet = compress_packet(msg, sign_key=key)
    wrapper = json.loads(packet.decode("utf-8"))
    assert "c" in wrapper and "s" in wrapper and "id" in wrapper
    out = decompress_packet(packet)
    assert out == msg


def test_signature_verify_failure():
    msg = {"k": 6}
    key = ed25519.Ed25519PrivateKey.generate()
    packet = compress_packet(msg, sign_key=key)
    wrapper = json.loads(packet.decode("utf-8"))
    wrapper["s"] = "AA"  # invalid signature
    tampered = json.dumps(wrapper).encode("utf-8")
    assert decompress_packet(tampered) is None


def test_decompress_invalid_digest_returns_none():
    msg = {"data": 123}
    packet = compress_packet(msg)
    tampered = bytearray(packet)
    tampered[-1] ^= 0xFF  # flip last byte to corrupt payload
    assert decompress_packet(bytes(tampered)) is None


def test_rle_applied_for_repetition():
    msg = {"data": "A" * 100}
    packet = compress_packet(msg)
    wrapper = json.loads(packet.decode("utf-8"))
    assert wrapper.get("rle") is True
    assert decompress_packet(packet) == msg

