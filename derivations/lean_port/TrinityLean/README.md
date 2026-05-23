# TrinityLean — Lean 4 Port

This directory contains the Lean 4 port of the Trinity S³AI formalization.

## Build instructions

```bash
lake build
```

## Mathlib decision (Wave 14.2)

**Status: Mathlib NOT used as default.**

- We tested adding `mathlib` (`v4.13.0`) to `lakefile.toml`.
- `lake update` alone exceeded 5 minutes without completing package download.
- Mathlib full build is documented to take 30+ minutes on first run, far exceeding our 10-minute threshold.
- **Decision:** Reverted to `lakefile-pure.toml` as the active `lakefile.toml`.
- The pure build completes successfully in ~2 seconds.

## Modules

| File | Status |
|------|--------|
| `TrinityLean/KODimension.lean` | Fully proved |
| `TrinityLean/QuaternionicLinearity.lean` | Fully proved (11 Float axioms) |
| `TrinityLean/Spectrum600Cell.lean` | 1 honest `sorry` (chiral_symmetry — needs Mathlib `List.Pairwise`) |
| `TrinityLean/EtaInvariant.lean` | Fully proved |
| `TrinityLean/DiracOperator.lean` | Definitions solid |

## Toolchain

`leanprover/lean4:v4.13.0`
