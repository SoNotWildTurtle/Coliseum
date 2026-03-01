"""Tests for transmission manager."""

from hololive_coliseum.transmission_manager import TransmissionManager


def test_transmission_roundtrip():
    tx = TransmissionManager(encrypt_key=b"k", level=9, algorithm="lzma")
    msg = {"foo": "bar"}
    packet = tx.compress(msg)
    out = tx.decompress(packet)
    assert out == msg


def test_transmission_bz2_roundtrip():
    tx = TransmissionManager(encrypt_key=b"k", level=9, algorithm="bz2")
    msg = {"foo": "baz"}
    packet = tx.compress(msg)
    out = tx.decompress(packet)
    assert out == msg
