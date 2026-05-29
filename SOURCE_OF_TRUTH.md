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

### `gHashTag/trios-mcp-rag`
- GOLDEN CHAIN Compendium PDF (PhD-style brochure)
- Postgres SSOT (`ssot_brochure.chapters`) for compendium chapters
- Rust `trios-mcp-rag` build pipeline (pandoc + tectonic)
- Forensic audit ledger (`docs/audits/build-*.md`) and migration runbooks
  (`docs/migrations/*-runbook.md`)
- Brochure-specific Lua filters and chapter LaTeX template
- Latest pinned snapshot in this repo: `releases/GOLDEN_CHAIN_compendium_v11.pdf`
  (sha256 `25dd2b18...`, upstream commit `5e19773`)

---

## Critical boundary — GF16 number type

`trios-trainer-igla` contains a **local** `gf16.rs` that is **not yet imported**
from the canonical `trios-golden-float` crate, but its numeric parameters
are now aligned with hardware.

| Property | trios-trainer-igla (local) | Canonical (trinity-s3ai / zig-golden-float) |
|---|---|---|
| Exponent bias | **31** (fixed 2026-05-25) | **31** |
| 1.0 encoding | exp=31 | exp=31 |
| Dynamic range | ~9.31×10⁻¹⁰ – ~4.29×10⁹ | ~9.31×10⁻¹⁰ – ~4.29×10⁹ |
| Special values | No subnormals; Inf/NaN clamped | Preserved per DLFloat16 spec |
| Status | Aligned but **still local** — migration pending | **SSOT** |

**Bias fix history:**
- 2026-05-25 — bias changed from 15 → 31 in `trios-trainer-igla` commit `042c2b5`
  (branch `fix/509-qat-v2`) and nested railway submodule commit `9830432`
  (branch `revert-pr-71-regression`).
- Pre-fix trainer BPB results (bias=15) are **invalid** for hardware attestation.
- Post-fix results are **valid** but should still be cross-checked against
  `zig-golden-float` BENCH-001–006 before claiming hardware equivalence.

The canonical GoldenFloat16 type lives in `gHashTag/trios-golden-float`
(Rust crate) and `gHashTag/zig-golden-float` (Zig impl).
`trios-trainer-igla` should eventually consume it as a versioned dependency,
not re-implement.

---

## Migration plan

| File path inside `trios-trainer-igla` | Outcome | Where canonical |
|---|---|---|
| `src/gf16.rs` (local, bias=31) | **DELETE**; import from `trios-golden-float` | `trios-golden-float` crate |
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
