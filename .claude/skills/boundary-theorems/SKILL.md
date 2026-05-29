---
name: boundary-theorems
description: Boundary Theorems BT-1 through BT-4 — formal obstruction results and how to cite them correctly
trigger:
  paths:
    - "proofs/trinity/BoundaryTheorems.v"
    - "docs/TECH_TREE.md"
    - "paper/**/*.md"
---

# Boundary Theorems Reference

## What Boundary Theorems Are

Boundary Theorems (BT) are **formally proven impossibility results** in Coq. They prove that *certain direct constructions* from H4 geometry do not reproduce Standard Model parameters. They are **guideposts** that narrow the search space, not tombstones that end exploration.

## BT-1 — φ^a π^b e^c Monomial Obstruction

**Statement:** No monomial of the form φ^a π^b e^c can reproduce Λ (cosmological constant) or Ω_b (baryon density).

**File:** `proofs/trinity/BoundaryTheorems.v`  
**Status:** `verified` (Coq `Qed.`)  
**Meaning:** Direct algebraic fits from the three fundamental constants alone are insufficient for cosmological parameters. This does **not** rule out more complex constructions or additional physical input.

## BT-2 — NCG σ-Field Obstruction

**Statement:** No noncommutative geometry (NCG) σ-field can be constructed from H4 root structure alone.

**File:** `proofs/trinity/BoundaryTheorems.v`  
**Status:** `verified` (Coq `Qed.`)  
**Meaning:** The H4 root system does not directly yield the scalar field structure needed for spectral action models. Track B (Cl(8) / J₃(𝕆)) explores alternative algebraic structures.

## BT-3 — 600-Cell Dirac Operator is Vector-Like

**Statement:** The 600-cell Dirac operator constructed from antipodal symmetry is vector-like (not chiral).

**File:** `proofs/trinity/BoundaryTheorems.v`  
**Status:** `verified` (Coq `Qed.`)  
**Meaning:** The natural Dirac operator on the 600-cell does not reproduce the chiral structure of the Standard Model fermions. The chirality problem remains open and is documented in `derivations/chirality/`.

## BT-4 — 2I-Equivariant D_F Cannot Reproduce Lepton Mass Ratios

**Statement:** The 2I-equivariant Dirac operator D_F does not reproduce lepton mass ratios (e, μ, τ).

**File:** `proofs/trinity/BoundaryTheorems.v`  
**Status:** `verified` (Coq `Qed.`)  
**Meaning:** The simplest equivariant construction fails for lepton masses. This motivates more sophisticated spectral triple constructions or additional symmetry breaking.

## Paper-Level BT-5–BT-7

These are documented in `paper/CHANGELOG_v1_to_v2.md` and `ROADMAP_WAVE17_PLUS.md`:

- **BT-5:** E8 plumbing eta discrepancy does not converge to -2 → `high_risk_or_falsified`
- **BT-6:** No known string / heterotic / F-theory / orbifold compactification rescues the SM hierarchy from H4 or F4 → `high_risk_or_falsified`
- **BT-7:** (Wave 17 addition) Documented obstruction in the spectral action expansion

## How to Cite Boundary Theorems

**Correct:** "BT-2 proves that NCG σ-fields from H4 root structure alone are obstructed, directing exploration toward Cl(8) constructions (Track B)."

**Incorrect:** "BT-2 kills the NCG approach." — BTs only obstruct *specific direct constructions*, not entire research programs.

## Related Files

- `proofs/trinity/BoundaryTheorems.v` — Formal Coq proofs
- `docs/TECH_TREE.md` — Layered status including BT impact
- `ROADMAP_WAVE17_PLUS.md` — Track A/B/C strategy post-BT
- `paper/CHANGELOG_v1_to_v2.md` — BT-5, BT-6, BT-7 documentation
