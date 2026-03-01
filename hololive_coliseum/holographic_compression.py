"""Holographic packet compression with anchors and lightweight encryption."""

import base64
import json
import zlib
import bz2
import lzma
import hashlib
import math
import os
from typing import Tuple, Dict, Any, List, Sequence
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

ANCHOR = "HLPC"
BUFFER_SIZE = 4096

# Four color-coded anchor points define the bounding box of the
# holographic pointcloud. Each anchor also stores virtual size,
# luminosity and a black/white level so peers can reconstruct the
# payload with multiple detail levels.
# Anchor layout:
# - Cyan  at (0, 0, 1) marks the starting corner.
# - White at (0, 0, 0) marks the front-bottom corner.
# - Black at (1, 1, 1) marks the far back-right corner.
# - Red   at (1, 1, 0) marks the near bottom-right corner.
ANCHOR_POINTS: List[dict[str, object]] = [
    {"pos": [0, 0, 1], "color": "cyan"},     # start
    {"pos": [0, 0, 0], "color": "white"},    # front-bottom
    {"pos": [1, 1, 1], "color": "black"},    # back-right
    {"pos": [1, 1, 0], "color": "red"},      # bottom-right
]


def _triangulation_profile(anchors: List[Dict[str, object]]) -> Dict[str, object]:
    """Return geometric diagnostics for the provided anchor points."""

    if len(anchors) < 4:
        return {"origin": [0, 0, 0], "axes": {}, "volume": 0.0, "vectors": {}}

    def _length(a: Sequence[float], b: Sequence[float]) -> float:
        return math.sqrt(sum((float(x) - float(y)) ** 2 for x, y in zip(a, b)))

    origin = list(anchors[1]["pos"])  # white anchor at front-bottom
    top = list(anchors[0]["pos"])  # cyan anchor at start corner
    far = list(anchors[2]["pos"])  # black anchor at back-right
    bottom_right = list(anchors[3]["pos"])  # red anchor at bottom-right

    axes = {
        "x": round(float(bottom_right[0]) - float(origin[0]), 3),
        "y": round(float(far[1]) - float(origin[1]), 3),
        "z": round(float(top[2]) - float(origin[2]), 3),
    }
    vectors = {
        "origin_to_top": round(_length(origin, top), 3),
        "origin_to_far": round(_length(origin, far), 3),
        "origin_to_bottom_right": round(_length(origin, bottom_right), 3),
    }
    volume = round(abs(axes["x"] * axes["y"] * axes["z"]), 3)
    return {
        "origin": origin,
        "axes": axes,
        "volume": volume,
        "vectors": vectors,
    }


def _layer_metadata(raw: bytes) -> List[Dict[str, object]]:
    """Return deterministic metadata describing pointcloud layers."""

    if not raw:
        return []
    layers: List[Dict[str, object]] = []
    chunk = max(1, len(raw) // 3)
    for index in range(3):
        start = index * chunk
        end = len(raw) if index == 2 else min(len(raw), start + chunk)
        segment = raw[start:end]
        if not segment:
            continue
        digest = hashlib.sha256(segment).hexdigest()[:16]
        density = sum(segment) / (len(segment) * 255.0)
        energy = sum(byte * (index + 1) for index, byte in enumerate(segment))
        energy /= (len(segment) or 1) * 255.0
        layers.append(
            {
                "index": index,
                "hash": digest,
                "size": len(segment),
                "density": round(density, 4),
                "virtual_channel": f"L{index + 1}",
                "energy": round(energy, 4),
            }
        )
    return layers


def _spectral_hint(raw: bytes) -> Dict[str, float]:
    """Return lightweight spectral data for holographic verification."""

    if not raw:
        return {"entropy": 0.0, "diversity": 0.0}
    unique = len(set(raw))
    diversity = unique / min(len(raw), 256)
    # Shannon entropy approximation using byte frequency counts.
    freq: Dict[int, int] = {}
    for value in raw:
        freq[value] = freq.get(value, 0) + 1
    total = float(len(raw))
    entropy = 0.0
    for count in freq.values():
        probability = count / total
        if probability > 0.0:
            entropy -= probability * math.log2(probability)
    max_entropy = math.log2(min(len(raw), 256)) if len(raw) else 1.0
    if max_entropy <= 0.0:
        normalised_entropy = 0.0
    else:
        normalised_entropy = min(1.0, entropy / max_entropy)
    return {
        "entropy": round(normalised_entropy, 4),
        "diversity": round(diversity, 4),
    }


def _phase_signature(raw: bytes) -> Dict[str, float]:
    """Return a lightweight phase/coherence signature for the payload."""

    if not raw:
        return {"coherence": 0.0, "phase": 0.0}
    total = len(raw)
    sin_sum = 0.0
    cos_sum = 0.0
    for index, value in enumerate(raw):
        angle = (value / 255.0) * math.pi * 2.0
        sin_sum += math.sin(angle)
        cos_sum += math.cos(angle)
    coherence = math.sqrt(sin_sum ** 2 + cos_sum ** 2) / max(1.0, float(total))
    phase = math.atan2(sin_sum, cos_sum) / math.pi
    return {"coherence": round(coherence, 4), "phase": round(phase, 4)}


def _stability_index(anchors: Sequence[Dict[str, object]]) -> float:
    """Return a synthetic stability index derived from anchor metadata."""

    if not anchors:
        return 0.0
    weighted = 0.0
    total_weight = 0.0
    for anchor in anchors:
        lum = float(anchor.get("lum", 0.0))
        bw = float(anchor.get("bw", 0.0))
        weighted += lum * (1.0 + bw)
        total_weight += 1.0 + bw
    if total_weight <= 0.0:
        return 0.0
    return round(weighted / total_weight, 4)


def _bandwidth_profile(
    layers: Sequence[Dict[str, object]],
    spectral: Dict[str, float],
    phase: Dict[str, float],
    payload_size: int,
) -> Dict[str, float]:
    """Derive a lightweight bandwidth profile for diagnostics."""

    layer_sizes = [float(layer.get("size", 0)) for layer in layers]
    total = sum(layer_sizes) or 1.0
    peak_layer = max(layer_sizes) if layer_sizes else 0.0
    average_layer = total / len(layer_sizes) if layer_sizes else 0.0
    entropy = spectral.get("entropy", 0.0)
    coherence = phase.get("coherence", 0.0)
    return {
        "payload_bytes": float(payload_size),
        "peak_layer": round(peak_layer, 2),
        "average_layer": round(average_layer, 2),
        "entropy": round(float(entropy), 4),
        "coherence": round(float(coherence), 4),
    }


def _telemetry_signature(
    layers: Sequence[Dict[str, object]],
    spectral: Dict[str, float],
    phase: Dict[str, float],
) -> Dict[str, object]:
    """Return concise telemetry for holographic monitoring."""

    hashes = tuple(layer.get("hash") for layer in layers)
    density = sum(layer.get("density", 0.0) for layer in layers)
    average_density = round(density / max(len(layers), 1), 4)
    return {
        "layer_hashes": hashes,
        "average_density": average_density,
        "entropy": spectral.get("entropy", 0.0),
        "phase": phase.get("phase", 0.0),
    }


def _rle_encode(data: bytes) -> bytes:
    """Return simple run-length encoding of ``data``."""
    if not data:
        return b""
    out = bytearray()
    last = data[0]
    count = 1
    for b in data[1:]:
        if b == last and count < 255:
            count += 1
        else:
            out.extend((count, last))
            last = b
            count = 1
    out.extend((count, last))
    return bytes(out)


def _rle_decode(data: bytes) -> bytes:
    """Decode bytes produced by :func:`_rle_encode`."""
    out = bytearray()
    it = iter(data)
    for count, b in zip(it, it):
        out.extend([b] * count)
    return bytes(out)


def _pointcloud_encode(
    data: bytes,
    buffer_size: int = BUFFER_SIZE,
    level: int = 6,
    algorithm: str = "zlib",
) -> Tuple[str, str, str]:
    """Compress ``data`` and split it into two base64 fragments.

    ``level`` controls compression strength. ``algorithm`` may be ``"zlib"``
    (default), ``"bz2"``, ``"lzma"`` or ``"auto"``. ``auto`` selects the
    smallest result between zlib and lzma to keep bandwidth and CPU usage low.
    Returns the two fragments and the algorithm actually used.
    """
    used = algorithm
    if algorithm == "lzma":
        compressed = lzma.compress(data, preset=level)
    elif algorithm == "bz2":
        compressed = bz2.compress(data, compresslevel=level)
    elif algorithm == "auto":
        z = zlib.compress(data, level)
        l = lzma.compress(data, preset=level)
        if len(z) <= len(l):
            compressed = z
            used = "zlib"
        else:
            compressed = l
            used = "lzma"
    else:
        compressed = zlib.compress(data, level)
        used = "zlib"
    b64 = base64.b64encode(compressed).decode("ascii")
    mid = len(b64) // 2
    return ANCHOR + b64[:mid], ANCHOR + b64[mid:], used


def _pointcloud_decode(
    part1: str,
    part2: str,
    buffer_size: int = BUFFER_SIZE,
    algorithm: str = "zlib",
) -> bytes:
    """Recombine the base64 fragments and decompress the bytes."""
    if part1.startswith(ANCHOR):
        part1 = part1[len(ANCHOR) :]
    if part2.startswith(ANCHOR):
        part2 = part2[len(ANCHOR) :]
    b64 = part1 + part2
    compressed = base64.b64decode(b64.encode("ascii"))
    mv = memoryview(compressed)
    result = bytearray()
    if algorithm == "lzma":
        decomp = lzma.LZMADecompressor()
    elif algorithm == "bz2":
        decomp = bz2.BZ2Decompressor()
    else:
        decomp = zlib.decompressobj()
    for i in range(0, len(compressed), buffer_size):
        result += decomp.decompress(mv[i : i + buffer_size])
    if hasattr(decomp, "flush"):
        result += decomp.flush()  # type: ignore[arg-type]
    return bytes(result)


def _xor(data: bytes, key: bytes) -> bytes:
    """XOR helper for lightweight encryption."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def compress_packet(
    msg: Dict[str, Any],
    key: bytes | None = None,
    level: int = 6,
    algorithm: str = "zlib",
    sign_key: ed25519.Ed25519PrivateKey | None = None,
) -> bytes:
    """Return a compressed packet using holographic lithography style encoding.

    Packets are converted to a pointcloud represented by two base64 strings.
    Four color-coded anchor points describing the cube corners are included so
    the receiver can properly size the pointcloud when decoding. When ``key`` is
    provided the payload is XOR encrypted with a nonce-derived key and a
    keyed BLAKE2s digest is included for verification. ``level`` sets the zlib
    or bz2 compression level and maps to the LZMA preset when that algorithm is
    selected. ``algorithm`` may also be ``"auto"`` to select the smallest result
    between zlib and lzma.
    """
    raw = json.dumps(msg, separators=(",", ":")).encode("utf-8")
    rle = _rle_encode(raw)
    use_rle = len(rle) < len(raw)
    payload = rle if use_rle else raw
    nonce = None
    if key is not None:
        nonce = os.urandom(8).hex()
        derived = hashlib.blake2s(key + nonce.encode("ascii")).digest()
        payload = _xor(payload, derived)  # Love you, Alex
        digest = hashlib.blake2s(raw, key=key).hexdigest()
    else:
        digest = hashlib.blake2s(raw).hexdigest()
    p1, p2, used_alg = _pointcloud_encode(payload, level=level, algorithm=algorithm)
    pub_b64 = None
    sig_b64 = None
    client_id = None
    layers = _layer_metadata(raw)
    spectral = _spectral_hint(raw)
    phase = _phase_signature(raw)
    if sign_key is not None:
        pub_bytes = sign_key.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw
        )
        signature = sign_key.sign(raw)
        pub_b64 = ANCHOR + base64.b64encode(pub_bytes).decode("ascii")
        sig_b64 = base64.b64encode(signature).decode("ascii")
        client_id = hashlib.sha256(pub_bytes).hexdigest()[:16]
    anchors = []
    for idx, ap in enumerate(ANCHOR_POINTS):
        anchors.append(
            {
                **ap,
                "vparam": len(raw) + idx,
                "size": idx + 1,
                "lum": 1.0 - idx * 0.1,
                "bw": idx * 3,
            }
        )
    triangulation = _triangulation_profile(anchors)
    anchor_quality = round(
        sum(anchor["lum"] for anchor in anchors) / max(1, len(anchors)), 3
    )
    stability_index = _stability_index(anchors)
    bandwidth_profile = _bandwidth_profile(layers, spectral, phase, len(raw))
    telemetry_signature = _telemetry_signature(layers, spectral, phase)
    wrapper = {
        "a": p1,
        "b": p2,
        "h": digest,
        "p": anchors,
        "alg": used_alg,
        "layers": layers,
        "spectral": spectral,
        "phase": phase,
        "anchor_quality": anchor_quality,
        "channel_map": {
            "layer_count": len(layers),
            "payload_bytes": len(raw),
            "compression": used_alg,
            "coherence": phase["coherence"],
            "stability_index": stability_index,
        },
        "channel_vectors": {
            "entropy": spectral["entropy"],
            "diversity": spectral["diversity"],
            "coherence": phase["coherence"],
        },
        "triangulation": triangulation,
        "anchor_vectors": triangulation.get("vectors", {}),
        "vparam_map": [anchor["vparam"] for anchor in anchors],
        "bandwidth_profile": bandwidth_profile,
        "telemetry_signature": telemetry_signature,
        "anchor_stability": stability_index,
    }
    if pub_b64 and sig_b64 and client_id:
        wrapper["c"] = pub_b64
        wrapper["s"] = sig_b64
        wrapper["id"] = client_id
    if use_rle:
        wrapper["rle"] = True
    if nonce is not None:
        wrapper["n"] = nonce
    return json.dumps(wrapper).encode("utf-8")


def decompress_packet(
    packet: bytes, key: bytes | None = None
) -> Dict[str, Any] | None:
    """Decode a packet produced by ``compress_packet``.

    Returns ``None`` if verification fails.
    """
    try:
        wrapper = json.loads(packet.decode("utf-8"))
        p1 = wrapper["a"]
        p2 = wrapper["b"]
        algorithm = wrapper.get("alg", "zlib")
        payload = _pointcloud_decode(p1, p2, algorithm=algorithm)
        if key is not None:
            nonce = wrapper.get("n", "")
            derived = hashlib.blake2s(key + nonce.encode("ascii")).digest()
            payload = _xor(payload, derived)
        raw = _rle_decode(payload) if wrapper.get("rle") else payload
        if "c" in wrapper and "s" in wrapper:
            try:
                pub = base64.b64decode(wrapper["c"][len(ANCHOR) :])
                sig = base64.b64decode(wrapper["s"])
                ed25519.Ed25519PublicKey.from_public_bytes(pub).verify(sig, raw)
            except Exception:
                return None
        if key is not None:
            expected = hashlib.blake2s(raw, key=key).hexdigest()
        else:
            expected = hashlib.blake2s(raw).hexdigest()
        if expected != wrapper.get("h"):
            return None
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return None
