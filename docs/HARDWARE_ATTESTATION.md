# Hardware Claims Attestation

**Date:** 2026-05-25
**Scope:** All GF16 / TTSKY / 0x47C0 / Three Crowns claims appearing in README.md and docs/hardware/
**Method:** Cross-reference against `t27` hardware repository and local reproducible benchmarks.

---

## 1. Verified Claims (evidence present)

| Claim | Evidence | Location |
|-------|----------|----------|
| **GF16 format specified** (1-6-9, bias 31) | Spec document + RTL | `docs/hardware/gf16_spec.md` §2 |
| **phi-distance 0.049 < fp16 0.118** | Encoding tables | `docs/hardware/gf16_spec.md` §2.4 |
| **FPGA 323 MHz, 35/35 RTL tests** | Benchmark JSON | `docs/hardware/gf16_bench_results.json` |
| **phi-structured step = log₂(φ) ≈ 0.694 bits** | Mathematical derivation | `docs/hardware/gf16_mathematics.md` §3 |
| **Optimal field size GF(2⁴)** | Quantization argument | `docs/hardware/gf16_mathematics.md` §2 |
| **Golden Self-Similarity (Prop 1)** | Formal proof: φ is unique self-similar proportion for bit allocation | `docs/hardware/gf16_mathematics.md` §6.1 |
| **Optimal Integer Rounding (Prop 2)** | Formal proof: `round((N−1)/φ²)` minimizes φ-distance; 7/7 verified | `docs/hardware/gf16_mathematics.md` §6.2 |
| **Universal Attractor (Theorem 3)** | Formal proof: φ is unique fixed point of balancing recursion (Banach) | `docs/hardware/gf16_mathematics.md` §6.3 |
| **DLFloat16 relation** | Layout identical; 6 critical differences documented | `docs/hardware/gf16_spec.md` §2.5 |
| **GoldenFloat family** | 7 formats (GF4–GF32) with φ-derived bit splits | `docs/hardware/gf16_spec.md` §2.6 |
| **Coq phi identity (binary64)** | `phi_sq_f64 = phi_plus_one_f64` verified via Flocq | `proofs/trinity/PhiFloat.v` |
| **Zig reference implementation** | `zig-golden-float` — integer-backed GF16, MNIST MLP 97.67% (0.00% gap vs f32), compiler stability tests | `gHashTag/zig-golden-float` repo, BENCH-001–006 |

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
| **Three Crowns (Phi/Euler/Gamma)** | Submitted to TTSKY26b (May 2026) | Await silicon return ~Nov 2026; post-silicon validation required before upgrade |
| **~1 GOPS @ ~50 MHz @ ~1 W** | RTL simulation only | Post-silicon clock sweep and power measurement required |

**Honest note on TTSKY shuttles:**
- **TTSKY26a** (May 2026) — original single-chip GF16 (`tt-trinity-gf16`), PR #322.
- **TTSKY26b** (May 2026) — Three Crowns family (`tt-trinity-phi`, `tt-trinity-euler`, `tt-trinity-gamma`), 21 closed PRs.
Both shuttles were submitted. TTSKY26b carries the multi-chip family; TTSKY26a carries the original single-chip design. Chips expected back ~Aug (26a) and ~Nov (26b) 2026.

---

## 4. What Is NOT Claimed (preventing misrepresentation)

1. **GF16 is not a standard float format.** It is a research format with non-standard bias=31 and no IEEE-754 conformance.
2. **BPB advantage is data-dependent.** It holds for phi-structured synthetic data; generic Gaussian data shows no special GF16 advantage.
3. **0x47C0 is not a mathematical theorem.** It is a *design choice* — a reset-time byte pattern chosen to echo the Lucas chain L₂=3. The mapping is metaphorical, not derived.
4. **Three Crowns are milestones, not necessities.** They are sequential validation gates, not mathematical requirements for the Trinity framework.
5. **GF16 layout is not original.** The 1-6-9 bias 31 layout is identical to IBM's DLFloat16 (ARITH 2019). Trinity's contribution is the φ-semantic overlay (phi-distance, PHI_BIAS=60 rounding, hardware-silicon binding), not the bit encoding.
6. **Formal proofs apply to the φ-theory, not the hardware.** Propositions 1–2 and Theorem 3 prove properties of the golden ratio as a bit-allocation principle. They do not prove that the TTSKY26a chip will function correctly.
7. **Coq phi identity is for binary64, not GF16.** `PhiFloat.v` proves `fl(phi*phi) = fl(phi+1)` in IEEE double precision (Flocq). A GF16-specific extension is future work.
8. **Bias=15 in trios-trainer-igla is NOT canonical GF16.** The trainer repo contains a temporary `gf16.rs` with bias=15 (IEEE-like range). Canonical GF16 uses bias=31 (DLFloat16 compatible). Trainer benchmarks with bias=15 must not be cited for hardware attestation. See `SOURCE_OF_TRUTH.md` §Critical boundary.

---

## 5. Provenance and Reproducibility

All artifacts copied from the `t27` hardware repository are attributed in `docs/hardware/README.md`.

| Artifact | Source (t27) | Local Copy |
|----------|-------------|------------|
| GF16 spec | `docs/arxiv-trinity-gf16-draft.md` §2 | `docs/hardware/gf16_spec.md` |
| Benchmark results | `conformance/gf16_bench_results.json` | `docs/hardware/gf16_bench_results.json` |
| Reference Python | `conformance/gf16_ref.py` | `docs/hardware/gf16_ref.py` |
| Test vectors | `conformance/gf16_vectors.json` | `docs/hardware/gf16_vectors.json` |
| NeurIPS paper | `neurips/gf_paper.pdf` | `docs/hardware/RELATED_WORK.md` §6.5 |
| Coq phi identity | `coq/Kernel/PhiFloat.v` | `proofs/trinity/PhiFloat.v` |
| GoldenFloat family SSOT | `conformance/FORMAT-SPEC-001.json` | cited in `docs/hardware/gf16_spec.md` |
| Zig reference impl + BENCH-001–006 | `gHashTag/zig-golden-float` repo | cited in `docs/hardware/RELATED_WORK.md` §13 |
| Cross-repo boundary | `gHashTag/trios-trainer-igla` | `SOURCE_OF_TRUTH.md` §Critical boundary |

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
