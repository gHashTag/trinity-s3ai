# Source-of-Truth Mandate — Trinity S³AI Hardware

> Effective: 2026-05-25.  
> Anchor: φ² + φ⁻² = 3.  
> Scope: GF16 / GoldenFloat number format, silicon binding, and hardware claims.

---

## Statement

`gHashTag/trinity-s3ai` is the **single source of truth** for:

- The GF16 (GoldenFloat 16) format specification (1-6-9, bias 31, DLFloat16 compatible)
- The GoldenFloat family (GF4–GF32) bit-allocation rules derived from φ
- FPGA / RTL evidence (`docs/hardware/rtl/` — Verilog mul/add/dot4)
- TinyTapeout silicon tapeout claims (TTSKY26a / TTSKY26b)
- The 0x47C0 reset-time anchor design
- The Three Crowns (Phi / Euler / Gamma) milestone specification
- Hardware BPB benchmarks (`docs/hardware/bpb_benchmark.py`, `bpb_results.json`)
- Coq hardware-attestation models (`proofs/trinity/coq_models/`)
- The HARDWARE_ATTESTATION.md honest proof inventory
- RELATED_WORK.md prior-art catalog
- `docs/claims.yaml` hardware claim ledger entries

---

## What this repo does NOT own

These remain canonical in their respective repositories:

### `gHashTag/zig-golden-float`
- Zig reference implementation of the GoldenFloat family
- BENCH-001–006 accuracy / compiler-stability / energy benchmarks
- The `u16`-backed integer encoding (avoids native `f16` compiler bugs)
- Cross-language bindings (Rust / C++ via Zig `export`)

### `gHashTag/trios-trainer-igla`
- Transformer + HybridAttn training architecture
- AdamW + Muon + φ-LR optimizer schedule
- T-JEPA loss + EMA target predictor
- BPE tokenizer + dataloader pipeline
- IGLA RACE ledger (`assertions/seed_results.jsonl`)
- TOML run-config schema (`champion`, `gate2-attempt`, `needle-v1-mup`)

### `gHashTag/t27`
- TinyTapeout RTL shuttle source (`tt_um_ghtag_trinity_gf16` etc.)
- Sky130 GDS-II hardening flow
- OpenROAD + Yosys synthesis scripts
- Post-silicon validation testbenches (pending)

---

## Critical boundary — GF16 number type

`trios-trainer-igla` contains a **temporary** `gf16.rs` (bias=15, IEEE-like range) that is **not canonical**.

| Property | trios-trainer-igla (temporary) | Canonical (trinity-s3ai / zig-golden-float) |
|---|---|---|
| Exponent bias | **15** | **31** |
| 1.0 encoding | exp=15 | exp=31 |
| Dynamic range | 4.66×10⁻⁵ – 6.55×10⁴ | ~9.31×10⁻¹⁰ – ~4.29×10⁹ |
| Special values | No subnormals; Inf/NaN clamped | Preserved per DLFloat16 spec |
| Status | DELETE pending (SOURCE_OF_TRUTH.md line 51) | **SSOT** |

**Impact:** Any BPB or accuracy benchmark run with `trios-trainer-igla/src/gf16.rs` produces **different numeric results** than the hardware GF16 (bias=31). Trinity hardware claims are **only valid** for bias=31. Trainer results with bias=15 must not be cited for hardware attestation.

The canonical GoldenFloat16 type lives in `gHashTag/trios-golden-float` (Rust crate) and `gHashTag/zig-golden-float` (Zig impl). `trios-trainer-igla` should consume it as a versioned dependency, not re-implement.

---

## Migration plan

| File path inside `trios-trainer-igla` | Outcome | Where canonical |
|---|---|---|
| `src/gf16.rs` (bias=15) | **DELETE**; import from `trios-golden-float` | `trios-golden-float` crate |
| `src/fake_quant.rs` | Keep (65+ format enum); reference canonical GF16 | `trios-trainer-igla` |
| `src/bench.rs` BPB formula | Keep; cite `trinity-s3ai` as downstream consumer | `trios-trainer-igla` |
| BENCH-001–006 results | Reference as upstream evidence | `zig-golden-float` |
| TTSKY26a/b silicon claims | **Never claim** in trainer repo | `trinity-s3ai` only |

---

## Forking / reuse policy

External forks of `trinity-s3ai` hardware documentation are welcome. Any publication or silicon tapeout that cites GF16 / GoldenFloat MUST:

- Reference `docs/hardware/gf16_spec.md` as the canonical spec
- Use bias=31 for hardware claims
- Cite IBM DLFloat16 (ARITH 2019) as the layout predecessor
- Not cite `trios-trainer-igla/src/gf16.rs` (bias=15) as evidence for GF16 hardware behavior

---

## Ownership

- Anchor: `φ² + φ⁻² = 3`
- Maintainer: [@gHashTag](https://github.com/gHashTag)
- License: Apache-2.0
