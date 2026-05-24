# Tautology Audit — Trinity S³AI Coq Codebase (Wave 20)

**Methodology:** Automated pattern search across all `.v` files in `proofs/` and `derivations/`.
**Date:** 2026-05-23

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total `Theorem` declarations | **1,040** |
| Tautological theorems | **210** (20.2%) |
| Non-trivial theorems | **830** (79.8%) |
| Axioms with `True` body | **28** |

**A tautological theorem** is defined as one whose proof consists solely of:
- `reflexivity` (proving `X = X` or computable ground equality)
- `unfold ... reflexivity` (proving a Definition equals its body)
- `trivial` / `exact I` (proving `True`)
- `lia` / `ring` / `lra` on ground terms with no variables (proving `3 = 3`)

These theorems add **zero derivational content**. They inflate the QED count without contributing to the project's scientific claims.

---

## Top Offenders

| File | Tautological | Total | % Trivial |
|------|------------|-------|-----------|
| `AltCrystallography.v` | 25 | 33 | **76%** |
| `ThreeGenerations.v` | 19 | 38 | **50%** |
| `SpectralTripleAxioms.v` | 15 | 25 | **60%** |
| `NeutrinoOrigins.v` | 10 | 35 | **29%** |
| `Axiom6Orientation.v` | 10 | 34 | **29%** |
| `UnimodularityAndSigma.v` | 9 | 19 | **47%** |
| `Catalog42.v` | 3 | 25 | **12%** |

---

## Patterns Found

### P1: `Definition = itself` (100 instances)

Example:
```coq
Definition H4_order : nat := 120.
Theorem H4_order_is_120 : H4_order = 120.
Proof. reflexivity. Qed.
```

This is not a theorem. It is a definition restated. The "proof" is computational reduction.

### P2: `True` proofs (20 instances)

Example:
```coq
Definition two_I_is_subgroup_of_SU2 : Prop := True.
Theorem SURV2_quaternionic_motivation : two_I_is_subgroup_of_SU2.
Proof. trivial. Qed.
```

These create the appearance of formalized structural results while proving nothing.

### P3: Ground arithmetic (90 instances)

Example:
```coq
Definition schur_degeneracy_dim3 : nat := 3.
Theorem schur_forces_degeneracy : schur_degeneracy_dim3 = 3.
Proof. lia. Qed.
```

`lia` proving `3 = 3` is not a proof of Schur's lemma. It is arithmetic on a hardcoded constant.

---

## Scientific Impact

The claimed **~1,800 Qed theorems** includes:
- ~210 tautologies (12%)
- ~28 `True` axioms
- Hundreds of interval bounds (`|formula - PDG| < ε`) that verify numerical coincidence, not derivation

**The genuine mathematical depth** is concentrated in:
- `CorePhi.v` — algebraic derivation of φ properties
- `Interval.Tactic` bounds in `Catalog42.v` — rigorous numerical verification
- `NoGoTheorems.v` — honest (if narrow) negative results

The rest is scaffolding.

---

## Recommendation

1. **Stop reporting raw QED counts** in promotional materials. Report: "~830 non-trivial theorems, ~210 definitional tautologies, 28 axioms."
2. **Add CI check**: `scripts/tautology_ratio.py` that fails if tautology fraction exceeds 25%.
3. **Refactor**: Move tautological theorems to `*_facts.v` files clearly labeled "definitional facts, not derivations."
