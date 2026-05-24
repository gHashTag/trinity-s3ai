# Hardware Claims Attestation

**Date:** 2026-05-25
**Scope:** All GF16 / TTSKY / 0x47C0 / Three Crowns claims appearing in README.md and docs/hardware/
**Method:** Cross-reference against `t27` hardware repository and local reproducible benchmarks.

---

## 1. Verified Claims (evidence present)

| Claim | Evidence | Location |
|-------|----------|----------|
| **GF16 format specified** (DLFloat-6:9, bias 31) | Spec document + RTL | `docs/hardware/gf16_spec.md` §2 |
| **phi-distance 0.049 < fp16 0.118** | Encoding tables | `docs/hardware/gf16_spec.md` §2.4 |
| **FPGA 323 MHz, 35/35 RTL tests** | Benchmark JSON | `docs/hardware/gf16_bench_results.json` |
| **phi-structured step = log₂(φ) ≈ 0.694 bits** | Mathematical derivation | `docs/hardware/gf16_mathematics.md` §3 |
| **Optimal field size GF(2⁴)** | Quantization argument | `docs/hardware/gf16_mathematics.md` §2 |

**Reproduce:**
```bash
cd docs/hardware
python3 gf16_ref.py              # 35 RTL consistency tests + roundtrip
python3 bpb_benchmark.py         # BPB compression benchmark
```

---

## 2. Empirical-Fit Claims (numerical evidence, not physical derivation)

| Claim | Evidence | Caveat |
|-------|----------|--------|
| **BPB advantage on phi-structured data** | `bpb_benchmark.py` output | Synthetic data only; real physics datasets (PDG vectors, MNIST weights) not yet tested |

**Results (2026-05-25, n=10,000):**

| Format | Raw BPB | Effective BPB (phi ladder) | Effective BPB (normal control) |
|--------|---------|---------------------------|------------------------------|
| float32 | 1.0000 | — | — |
| fp16 | 0.5000 | 0.1277 | 0.3880 |
| bfloat16 | 0.5000 | 0.1277 | 0.3209 |
| GF16 | 0.5000 | 0.1277 | 0.3705 |
| **phi-4Q** | **0.1250** | **0.1238** | **0.0923** |

*Interpretation:* phi-4Q (4-bit phi-ladder quantizer) achieves 0.125 raw BPB = 8× compression vs float32. The effective BPB is competitive with 16-bit formats on phi-structured data and substantially lower on normal data, but the latter comes from aggressive quantization error rather than information preservation.

---

## 3. Open-Conjecture Claims (design documented, silicon pending)

| Claim | Status | Blocking Gap |
|-------|--------|--------------|
| **TTSKY26a tapeout** | Submitted, awaiting silicon | GDS-II signoff confirmation; post-silicon test results expected ~Aug 2026 |
| **0x47C0 silicon anchor** | RTL design only | No reset-witness module in t27 RTL yet; no testbench; no logic-analyzer trace |
| **Three Crowns (Phi/Euler/Gamma)** | Two submitted, one pending | Need at least one crown validated on real silicon before upgrade |
| **~1 GOPS @ ~50 MHz @ ~1 W** | RTL simulation only | Post-silicon clock sweep and power measurement required |

**Honest note on TTSKY26b:** README.md mentions "TTSKY26b". The t27 draft says **TTSKY26a** (May 2026). TTSKY26b is a *planned* follow-up for Gamma and any respins. The "26b" claim should be read as "the 26b generation of the chip", not "already fabricated on 26b".

---

## 4. What Is NOT Claimed (preventing misrepresentation)

1. **GF16 is not a standard float format.** It is a research format with non-standard bias=31 and no IEEE-754 conformance.
2. **BPB advantage is data-dependent.** It holds for phi-structured synthetic data; generic Gaussian data shows no special GF16 advantage.
3. **0x47C0 is not a mathematical theorem.** It is a *design choice* — a reset-time byte pattern chosen to echo the Lucas chain L₂=3. The mapping is metaphorical, not derived.
4. **Three Crowns are milestones, not necessities.** They are sequential validation gates, not mathematical requirements for the Trinity framework.

---

## 5. Provenance and Reproducibility

All artifacts copied from the `t27` hardware repository are attributed in `docs/hardware/README.md`.

| Artifact | Source (t27) | Local Copy |
|----------|-------------|------------|
| GF16 spec | `docs/arxiv-trinity-gf16-draft.md` §2 | `docs/hardware/gf16_spec.md` |
| Benchmark results | `conformance/gf16_bench_results.json` | `docs/hardware/gf16_bench_results.json` |
| Reference Python | `conformance/gf16_ref.py` | `docs/hardware/gf16_ref.py` |
| Test vectors | `conformance/gf16_vectors.json` | `docs/hardware/gf16_vectors.json` |

To verify t27 commit SHA:
```bash
cd ../t27  # or wherever your t27 clone lives
git log -1 --format="%H %ad %s"
```

---

## 6. References

- `docs/hardware/README.md` — index of all hardware docs
- `docs/hardware/gf16_spec.md` — format specification
- `docs/hardware/gf16_mathematics.md` — derivations (φ-step, optimal field size)
- `docs/hardware/silicon_anchor.md` — 0x47C0 design + Three Crowns + TinyTapeout status
- `docs/claims.yaml` — canonical claim ledger (SSOT)
- `scripts/generate_claims.py` — regenerates README table and game cards from claims.yaml
