# Trinity S³AI — Hardware Documentation

This directory contains the proof basis for the hardware claims made in the
root [`README.md`](../README.md) §"Why $TRI Is Mined Only on TTSKY26b".

## Verified Artifacts (from t27 repo)

| File | Source | What it proves |
|------|--------|----------------|
| [`gf16_spec.md`](gf16_spec.md) | `t27/docs/arxiv-trinity-gf16-draft.md` §2 | GF16 format: 1/6/9 layout, bias 31, phi-distance 0.049 vs f16 0.118 |
| [`gf16_benchmarks.json`](gf16_benchmarks.json) | `t27/conformance/gf16_bench_results.json` | MSE 0.000234, latency 4.5–7.2 ns/op, 35/35 RTL tests pass |
| [`gf16_ref.py`](gf16_ref.py) | `t27/conformance/gf16_ref.py` | Reference encode/decode/dot4 implementation |
| [`gf16_vectors.json`](gf16_vectors.json) | `t27/conformance/gf16_vectors.json` | Conformance test vectors |
| [`bpb_benchmark.py`](bpb_benchmark.py) | **This repo** | BPB compression benchmark: GF16 vs bf16/fp16 on phi-structured data |
| [`gf16_mathematics.md`](gf16_mathematics.md) | **This repo** | Derivation of φ-structured step, 0.694-bit reduction, optimal field size |
| [`silicon_anchor.md`](silicon_anchor.md) | **This repo** | 0x47C0 anchor design, Three Crowns mapping, TinyTapeout submission status |

## Honest Status Summary

| Claim | Status | Evidence Location |
|-------|--------|-------------------|
| GF16 format specified | `verified` | `gf16_spec.md` §2.1–2.4 |
| GF16 phi-distance < f16 | `verified` | `gf16_spec.md` §2.5 |
| FPGA 323 MHz, 35/35 RTL tests | `verified` | `gf16_benchmarks.json` |
| BPB (bits-per-byte) advantage | `empirical_fit` | `bpb_benchmark.py` — run to reproduce |
| φ-structured step (0.694-bit) | `verified` | `gf16_mathematics.md` §3 |
| Optimal field size GF(2⁴) | `verified` | `gf16_mathematics.md` §2 |
| 0x47C0 silicon anchor | `open_conjecture` | `silicon_anchor.md` §4 — design documented, silicon pending |
| TinyTapeout TTSKY26b | `open_conjecture` | `silicon_anchor.md` §5 — TTSKY26a submitted, awaiting results |
| ~1 GOPS @ ~50 MHz @ ~1 W | `open_conjecture` | `silicon_anchor.md` §6 — projection, not measurement |

## Reproducing Benchmarks

```bash
cd docs/hardware

# GF16 conformance tests
python3 gf16_ref.py

# BPB compression benchmark
python3 bpb_benchmark.py

# Verify against published JSON
cat gf16_benchmarks.json | python3 -m json.tool
```

## Provenance

All artifacts copied from the `t27` hardware repository are attributed with
commit SHA. Run `git log -1` in the t27 repo to get the current SHA.
