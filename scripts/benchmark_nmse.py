#!/usr/bin/env python3
"""
benchmark_nmse.py — NMSE harness for GF16 vs bfloat16 (fake-quant pattern)

Protocol: GF16_BFLOAT16_NMSE/1.0 (see tt-trinity-phi/GF16_BFLOAT16_NMSE.md)
Seed: 0x47C0  |  N = 1_048_576
Distributions: D-1 .. D-6
Output: bench/nmse/<git_sha>.json
"""

import json
import math
import os
import struct
import subprocess
import sys
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Import GF16 reference (docs/hardware/gf16_ref.py)
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
GF16_REF_PATH = REPO_ROOT / "docs" / "hardware" / "gf16_ref.py"

if not GF16_REF_PATH.exists():
    print(f"ERROR: GF16 reference not found at {GF16_REF_PATH}", file=sys.stderr)
    sys.exit(1)

# Import gf16_ref as a module
import importlib.util
spec = importlib.util.spec_from_file_location("gf16_ref", GF16_REF_PATH)
gf16_ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gf16_ref)

# ---------------------------------------------------------------------------
# Fake-quant helpers (pattern from trios-trainer-igla/src/fake_quant.rs)
# ---------------------------------------------------------------------------

def fake_quantize_f32(val: float, mantissa_bits: int) -> float:
    """Simulate reduced-precision float by masking lower mantissa bits."""
    if not math.isfinite(val):
        return val
    if mantissa_bits >= 23:
        return val
    if mantissa_bits <= 0:
        return val

    bits = struct.unpack(">I", struct.pack(">f", float(val)))[0]
    drop_bits = 23 - mantissa_bits
    mask = ~((1 << drop_bits) - 1)
    masked_bits = bits & mask
    rounding_bit = 1 << (drop_bits - 1)
    rounded_bits = masked_bits + rounding_bit
    return struct.unpack(">f", struct.pack(">I", rounded_bits))[0]


def bfloat16_roundtrip(val: float) -> float:
    """bfloat16 has 1 sign + 8 exponent + 7 mantissa => mantissa_bits = 7."""
    return fake_quantize_f32(val, mantissa_bits=7)


def fp16_roundtrip(val: float) -> float:
    """IEEE fp16 has 10 mantissa bits."""
    return fake_quantize_f32(val, mantissa_bits=10)


def fp8e4m3_roundtrip(val: float) -> float:
    """FP8 E4M3 has 3 mantissa bits."""
    return fake_quantize_f32(val, mantissa_bits=3)


def fp8e5m2_roundtrip(val: float) -> float:
    """FP8 E5M2 has 2 mantissa bits."""
    return fake_quantize_f32(val, mantissa_bits=2)


def gf16_roundtrip(val: float) -> float:
    """Full GF16 encode→decode round-trip via gf16_ref.py (1-6-9 bias 31)."""
    try:
        raw = gf16_ref.encode(val)
        return gf16_ref.decode(raw)
    except Exception:
        # On any encoding failure (overflow, etc.), fall back to clamped value
        if val > 0:
            return gf16_ref.decode(gf16_ref.POS_INF)
        elif val < 0:
            return gf16_ref.decode(gf16_ref.NEG_INF)
        return gf16_ref.decode(gf16_ref.POS_ZERO)


# ---------------------------------------------------------------------------
# Sacred constants D-6 (from tt-trinity-phi/src/sacred_constants_rom.v)
# Q3.5 unsigned: value = raw / 32.0
# ---------------------------------------------------------------------------

SACRED_CONSTANTS_75 = [
    # addr 0..10
    51/32, 20/32, 84/32, 12/32, 101/32,  # 0-4
    127/32,                               # 5  clamp
    87/32, 18/32, 22/32, 35/32, 96/32,  # 6-10
    # addr 11..15 clamp
    127/32, 127/32, 127/32, 127/32, 127/32,
    # addr 16
    71/32,
    # addr 17 clamp
    127/32,
    # addr 18..20 clamp
    127/32, 127/32, 127/32,
    # addr 21-22
    8/32, 5/32,
    # addr 23-24 clamp
    127/32, 127/32,
    # addr 25-31
    10/32, 12/32, 28/32, 16/32, 45/32, 55/32, 72/32,
    # addr 32-44
    24/32, 15/32, 37/32, 32/32, 46/32, 73/32, 19/32,
    16/32, 28/32, 37/32, 30/32, 58/32, 50/32,
    # addr 45-49
    23/32, 18/32, 14/32, 73/32, 90/32,
    # addr 50-59
    16/32, 23/32, 23/32, 28/32, 32/32, 55/32,
    32/32, 72/32, 72/32, 96/32,
    # addr 60 clamp
    127/32,
    # addr 61-72
    35/32, 14/32, 49/32, 12/32, 14/32, 7/32,
    16/32, 31/32, 3/32, 25/32, 22/32, 26/32,
    # addr 73-74 clamp
    127/32, 127/32,
]

assert len(SACRED_CONSTANTS_75) == 75, "Expected 75 sacred constants"

# ---------------------------------------------------------------------------
# Distribution generators (N = 1_048_576, seed = 0x47C0)
# ---------------------------------------------------------------------------

N = 1_048_576
SEED = 0x47C0


def make_d1() -> np.ndarray:
    """D-1: Standard normal N(0, 1)."""
    rng = np.random.default_rng(SEED)
    return rng.standard_normal(N)


def make_d2() -> np.ndarray:
    """D-2: Lognormal exp(N(0, 1))."""
    rng = np.random.default_rng(SEED)
    return np.exp(rng.standard_normal(N))


def make_d3() -> np.ndarray:
    """D-3: Uniform on [-1, 1]."""
    rng = np.random.default_rng(SEED)
    return rng.uniform(-1.0, 1.0, N)


def make_d4() -> np.ndarray:
    """D-4: Mixture 95% N(0,1) + 5% N(0,16)."""
    rng = np.random.default_rng(SEED)
    mask = rng.random(N) < 0.05
    samples = rng.standard_normal(N)
    samples[mask] = rng.standard_normal(mask.sum()) * 4.0  # std=4 => var=16
    return samples


def make_d5() -> np.ndarray:
    """D-5: Powers of two from 2^-30 .. 2^30, uniform exponent."""
    rng = np.random.default_rng(SEED)
    exponents = rng.integers(-30, 31, N)
    return np.power(2.0, exponents)


def make_d6() -> np.ndarray:
    """D-6: The 75 sacred constants, tiled to N."""
    arr = np.array(SACRED_CONSTANTS_75, dtype=np.float32)
    repeats = int(math.ceil(N / len(arr)))
    tiled = np.tile(arr, repeats)
    return tiled[:N]


DISTRIBUTIONS = {
    "D-1": make_d1,
    "D-2": make_d2,
    "D-3": make_d3,
    "D-4": make_d4,
    "D-5": make_d5,
    "D-6": make_d6,
}

# ---------------------------------------------------------------------------
# NMSE computation
# ---------------------------------------------------------------------------

def nmse_db(x: np.ndarray, x_hat: np.ndarray) -> float:
    """NMSE in dB: 10 * log10( sum((x - x_hat)^2) / sum(x^2) )."""
    diff = x.astype(np.float64) - x_hat.astype(np.float64)
    num = float(np.sum(diff * diff))
    den = float(np.sum(x.astype(np.float64) * x.astype(np.float64)))
    if den == 0.0:
        return -120.0
    if num == 0.0:
        return -120.0
    return 10.0 * math.log10(num / den)


# ---------------------------------------------------------------------------
# Harness runner
# ---------------------------------------------------------------------------

FORMATS = {
    "f32":      {"rt": lambda v: float(v),           "mantissa": 23},
    "bfloat16": {"rt": bfloat16_roundtrip,            "mantissa": 7},
    "fp16":     {"rt": fp16_roundtrip,                "mantissa": 10},
    "gf16":     {"rt": gf16_roundtrip,                "mantissa": 9},
    "gf16_fq":  {"rt": lambda v: fake_quantize_f32(v, 9), "mantissa": 9},
    "fp8_e4m3": {"rt": fp8e4m3_roundtrip,              "mantissa": 3},
    "fp8_e5m2": {"rt": fp8e5m2_roundtrip,              "mantissa": 2},
}


def run_harness():
    results = []
    summary_lines = []

    for dist_id, dist_fn in DISTRIBUTIONS.items():
        x = dist_fn().astype(np.float32)
        for fmt_id, fmt_meta in FORMATS.items():
            x_hat = np.array([fmt_meta["rt"](float(v)) for v in x], dtype=np.float32)
            val = nmse_db(x, x_hat)
            results.append({
                "dist": dist_id,
                "format": fmt_id,
                "nmse_db": round(val, 2),
            })
            summary_lines.append(f"  {dist_id}  {fmt_id:10s}  NMSE = {val:+.2f} dB")

    # git SHA of trinity-s3ai
    try:
        git_sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
    except Exception:
        git_sha = "UNKNOWN"

    report = {
        "protocol": "GF16_BFLOAT16_NMSE/1.0",
        "git_sha": git_sha,
        "sample_count": N,
        "seed": hex(SEED),
        "results": results,
    }

    out_dir = REPO_ROOT / "bench" / "nmse"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{git_sha}.json"

    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print("=" * 60)
    print("NMSE Harness — GF16_BFLOAT16_NMSE/1.0")
    print(f"Seed: {hex(SEED)}  |  N: {N:,}  |  git_sha: {git_sha}")
    print("=" * 60)
    print("\n".join(summary_lines))
    print("=" * 60)
    print(f"Report written to: {out_path}")

    return report


if __name__ == "__main__":
    run_harness()
