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

## Module Structure (post Wave 24+ cleanup)

### Default `lake build` target (pure Lean 4 core)

All modules under `TrinityLean/TrinityLean/` — resolved by lake via the root file
`TrinityLean.lean`:

| Module | File | Status |
|--------|------|--------|
| `KODimension` | `TrinityLean/TrinityLean/KODimension.lean` | Pure-Lean KO-signs (95 lines) |
| `QuaternionicLinearity` | `TrinityLean/TrinityLean/QuaternionicLinearity.lean` | Pure-Lean quaternions (Float), 11 axioms |
| `Spectrum600Cell` | `TrinityLean/TrinityLean/Spectrum600Cell.lean` | 0 sorry |
| `EtaInvariant` | `TrinityLean/TrinityLean/EtaInvariant.lean` | Pure definitions |
| `DiracOperator` | `TrinityLean/TrinityLean/DiracOperator.lean` | 1 structural axiom |
| `H4RootSystem` | `TrinityLean/TrinityLean/H4RootSystem.lean` | 1 sorry (icosian embedding) |
| `HamiltonFano` | `TrinityLean/TrinityLean/HamiltonFano.lean` | Fano-plane Hamilton cycle |
| `Snub24Z3` | `TrinityLean/TrinityLean/Snub24Z3.lean` | Z₃ partition of snub 24-cell |

### Mathlib-based extended versions (NOT in default target)

These files require Mathlib and are **not** imported by the root file. They exist as
extended formalizations with richer mathematical content:

| Module | File | Notes |
|--------|------|-------|
| `KODimensionMathlib` | `TrinityLean/KODimensionMathlib.lean` | 281 lines; uses `Mathlib.Algebra.Quaternion` |
| `QuaternionicLinearityMathlib` | `TrinityLean/QuaternionicLinearityMathlib.lean` | 326 lines; uses `Mathlib.Analysis.InnerProductSpace` |
| `CorePhi` | `TrinityLean/CorePhi.lean` | Requires Mathlib; 14 lemmas |

## Toolchain

`leanprover/lean4:v4.13.0`
