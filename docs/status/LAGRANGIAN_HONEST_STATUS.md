# Lagrangian Status — Honest Reclassification

**Status**: Canonical (supersedes `SM_LAGRANGIAN_STATUS_v43.md` 92.3% claim)
**Date**: 2026-05-23
**Reason**: Internal audit (see `lagrangian_roadmap.md`, `HARSH_REVIEW_v49.md`) showed the previously advertised "92.3% PROVEN" completeness conflated three distinct epistemic categories. This document restates each of the 13 SM Lagrangian sectors using the actual proof status in the Coq sources.

---

## TL;DR

| Category | Count | What it means |
|---|---|---|
| ✅ **PROVEN** | **3 / 13** | Closed Coq theorem, no `Axiom`/`Admitted` on the critical path, prediction matches data |
| 📊 **PHENOMENOLOGICAL** | **9 / 13** | Numerical fit reproduces the observable, but the Lagrangian term itself is *postulated*, not *derived* from H4 / Cl(8) / Spectral Triple first principles |
| 🟡 **OPEN** | **1 / 13** | Acknowledged unfinished (RG running) |

**The previous headline "92.3% of the SM Lagrangian is proven" is withdrawn.** A more accurate statement is: *3 out of 13 sectors are formally derived from first principles; the remaining 10 are either parameter fits or open work.*

---

## ✅ PROVEN (3 sectors)

These sectors have a closed Coq theorem deriving the result from project first principles (H4 root system, Clifford Cl(8) structure, or Connes spectral triple), with no `Axiom`/`Admitted` on the critical path.

### 1. Higgs mass m_H
- **File**: `proofs/HiggsPrediction.v`
- **Result**: m_H = 125.1 ± 0.1 GeV (prediction) vs 125.20 ± 0.11 GeV (PDG 2024)
- **Deviation**: 0.09%
- **Derivation**: From H4 → E8 → Coleman-Weinberg potential. Closed chain.

### 2. Gauge couplings (α₁, α₂, α₃ at M_Z)
- **File**: `proofs/GaugeCouplings.v`
- **Result**: g₁, g₂, g₃ reproduced within 0.024%
- **Derivation**: From E8 → SU(3)×SU(2)×U(1) branching with H4 normalization. Closed chain.
- **Caveat**: The *branching itself* (which subgroup of E8 maps to which SM factor) is the open gauge-assignment problem flagged in `lagrangian_roadmap.md` §3.

### 3. Higgs self-coupling λ
- **File**: `proofs/HiggsSelfCoupling.v`
- **Result**: λ ≈ 0.129 (predicted) vs 0.1291 (PDG 2024)
- **Deviation**: 0.4%
- **Derivation**: From m_H prediction + tree-level relation λ = m_H² / (2v²). Closed.

---

## 📊 PHENOMENOLOGICAL (9 sectors)

These are **numerical successes**, not derivations. The Lagrangian term is *written down*, fitted parameters are adjusted, and the result agrees with data. They do **not** constitute a derivation of the SM Lagrangian from first principles.

| # | Sector | Status note |
|---|---|---|
| 4 | Higgs potential V(Φ) | Form postulated; minimum reproduces v=246 GeV after tuning. **No derivation of the Higgs mechanism from spectral triple — see `lagrangian_roadmap.md` Gap 3.** |
| 5 | Lepton & quark masses | 12 masses reproduced via H4-inspired ansatz. The ansatz has **as many free parameters as observables fit**. |
| 6 | CKM mixing | 4 angles fit. No proof that H4 *forces* this specific matrix vs the 10³ alternatives. |
| 7 | PMNS mixing | 4 angles fit. Same issue as CKM. **δ_CP = 65.66° prediction is excluded** by [NuFIT-6.0](https://arxiv.org/abs/2410.05380) (best fit 212°, 3σ window 124°-364°) and disfavored by [T2K+NOvA Nature Oct 2025](https://www.nature.com/articles/s41586-025-09599-3) (δ_CP ≈ 270°, IO preferred). |
| 8 | Yukawa couplings | Y_f = m_f √2 / v — i.e. *defined* from the fitted masses, not derived. **No first-principles Yukawa structure — see `lagrangian_roadmap.md` Gap 4.** |
| 9 | Gauge kinetic terms | Form `-¼ F^a_{μν} F^{aμν}` postulated for each factor; canonical kinetic structure assumed, not derived from spectral action expansion. |
| 10 | 3 generations | Multiplicity = 3 asserted as input from H4/E8 dimension counting. The **a_4 Bridge Problem** (`lagrangian_roadmap.md` Gap 1) shows the Coq value a_4 = 0.568 vs Trinity-claimed a_4 = 33.89 — a **60× discrepancy** that remains unresolved. The Snub 24-cell route (96 = 3×32) is **refuted** in `ThreeGenerations.v` Section 3 (Mechanism B failure). |
| 11 | Ghost terms | Faddeev-Popov ghosts documented as standard QFT ingredients; not derived from any deeper principle in this project. |
| 12 | Strong CP / θ_QCD | θ ≈ 0 imposed as boundary condition; no Peccei-Quinn or analog mechanism is derived in the formalism. |

### Cross-cutting issues flagged internally

From `lagrangian_roadmap.md` (project's own internal audit):
- **e² Mystery** — the electromagnetic coupling enters via an unexplained normalization factor.
- **Gauge group assignment** — which E8 subgroup maps to colour vs weak isospin vs hypercharge is not uniquely fixed by the construction.
- **Higgs mechanism not derived** from spectral triple data.
- **Yukawa structure not derived** from first principles.

From `HARSH_REVIEW_v49.md`:
- The "92.3% proven" framing was identified as **post-hoc fitting** dressed in derivation language.

From `admitted_log.md`:
- 68 `Axiom` + 34 `Admitted` + 17 `admit` declarations remain in the proof base, against an earlier advertised "0-25".

From `proofs/trinity/SpectralTripleAxioms.v`:
- 4 NCG axioms unclosed: `first_order`, `axiom4`, `orientation_hochschild`, `poincare_nondegeneracy`.

---

## 🟡 OPEN (1 sector)

### 13. RG running (one-loop & two-loop)
- **Status**: Recognized as unfinished. Numerical RGE integration is present but the formal proof of consistency with the predicted m_H and gauge couplings at M_Z is not closed.
- **Estimated effort to close**: 6-12 months (per `lagrangian_roadmap.md`).

---

## What was the "92.3%" actually counting?

The original figure came from **a weighted average of fractional deviations** between predicted and measured observables across the 13 sectors — a goodness-of-fit metric, not a measure of formal proof coverage. Calling that "92.3% of the SM Lagrangian proven" was a category error: a small χ² is not a derivation.

The honest restatement:
- **Numerical agreement**: high for the fitted observables (this is real, and remains the project's main empirical hook).
- **Formal derivation coverage**: 3/13 sectors.

---

## What changes downstream of this document

The following claims are **withdrawn or weakened** across the repository:

| Claim (old) | Claim (new) |
|---|---|
| "92.3% of the SM Lagrangian is proven" | "3 of 13 SM Lagrangian sectors are formally derived; 9 are phenomenological fits; 1 is open" |
| "Trinity > Connes NCG (92.3% vs ~70%)" | (claim removed — comparison was not apples-to-apples; Connes' coverage is over different structures) |
| "Lagrangian derivation complete to 92.3%" | "Lagrangian derivation partial; major gaps documented in `lagrangian_roadmap.md`" |

Files updated in this branch:
- `README_v46.md` (4 occurrences)
- `IMPROVEMENT_PLAN.md` (2 occurrences)
- `IMPACT_COMPARISON.md` (4 occurrences)
- `SM_LAGRANGIAN_STATUS_v43.md` (deprecation header added)

---

## Why this honesty pass

A theory's credibility depends more on what it *honestly says it has not yet proven* than on what it advertises as done. The internal documents `lagrangian_roadmap.md` and `HARSH_REVIEW_v49.md` were already saying the harder truth in the basement; this file lifts it to the front page.

The strongest results of the project — m_H, gauge couplings, λ — survive this pass intact. They are now stated without being diluted by 10 over-claims.
