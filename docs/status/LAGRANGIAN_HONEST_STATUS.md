# LEGACY DOCUMENT (historical Wave 20 Lagrangian status)
# Current status: Superseded by Wave 24+ canonical assessment. See RESEARCH_STATUS.md and
# TECH_TREE.md for current project state.

# Lagrangian Status — Honest Reclassification

**Status**: Canonical (supersedes `SM_LAGRANGIAN_STATUS_v43.md` 92.3% claim)
**Date**: 2026-05-23
**Reason**: Internal audit (see `lagrangian_roadmap.md`, `HARSH_REVIEW_v49.md`) showed the previously advertised "92.3% PROVEN" completeness conflated three distinct epistemic categories. This document restates each of the 13 SM Lagrangian sectors using the actual proof status in the Coq sources.

---

## TL;DR

| Category | Count | What it means |
|---|---|---|
| ✅ **FORMALLY VERIFIED** | **3 / 13** | Coq interval proof confirms fitted formula matches data; **NOT derived** from H₄ first principles |
| 📊 **PHENOMENOLOGICAL** | **9 / 13** | Numerical fit reproduces the observable, but the Lagrangian term itself is *postulated*, not *derived* from H4 / Cl(8) / Spectral Triple first principles |
| 🟡 **OPEN** | **1 / 13** | Acknowledged unfinished (RG running) |

**The previous headline "92.3% of the SM Lagrangian is proven" is withdrawn.** A more accurate statement is: *3 out of 13 sectors have Coq-verified numerical bounds on fitted formulas; none are derived from H₄ first principles. The remaining 10 are either parameter fits or open work.*

---

## ✅ INTERVAL-BOUND VERIFIED (3 sectors)

These sectors have closed Coq theorems verifying numerical bounds on fitted formulas. The formulas themselves are **not derived** from H₄ root system, Clifford Cl(8) structure, or Connes spectral triple first principles — they are phenomenological fits whose agreement with data is confirmed via the `interval` tactic.

### 1. Higgs mass m_H
- **File**: `proofs/HiggsPrediction.v`
- **Result**: m_H = 125.1 ± 0.1 GeV (retrospective fit / post-hoc coincidence) vs 125.20 ± 0.11 GeV (PDG 2024)
- **Deviation**: 0.09%
- **Coq verification**: Interval proof confirms the fitted formula matches PDG value. **NOT a derivation** from H₄ geometry.

### 2. Gauge couplings (α₁, α₂, α₃ at M_Z)
- **File**: `proofs/GaugeCouplings.v`
- **Result**: g₁, g₂, g₃ reproduced within 0.024%
- **Coq verification**: Interval proof confirms fitted couplings match PDG values. **NOT a derivation** from H₄ geometry. The branching itself is postulated.
- **Caveat**: The *branching itself* (which subgroup of E8 maps to which SM factor) is the open gauge-assignment problem flagged in `lagrangian_roadmap.md` §3.

### 3. Higgs self-coupling λ
- **File**: `proofs/HiggsSelfCoupling.v`
- **Result**: λ ≈ 0.129 (retrospective fit) vs 0.1291 (PDG 2024)
- **Deviation**: 0.4%
- **Coq verification**: Interval proof confirms λ from the fitted m_H formula via the tree-level relation. **NOT a derivation** from H₄ geometry.

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

From `COQ_HONEST_STATUS.md` (canonical):
- 73 `Axiom` + 25 `Admitted` + 18 `admit` + 7 `Parameter` = 123 unproven obligations across 79 Coq files.

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

The strongest results of the project — m_H, gauge couplings, λ as Coq-verified numerical fits — survive this pass intact. They are now stated without being diluted by 10 over-claims.

---

## Wave 8.3 Update: e^2 factor in Trinity formula — origin investigation

**Date**: 2026-06-23
**File**: `proofs/trinity/HiggsE2Origin.v`

### Finding

The "e" in `m_H = 4 * phi^3 * e^2` is `exp(1)` — Napier's mathematical constant (Euler's number, e = 2.71828...). This is confirmed by the `HiggsPrediction.v` definition:

```coq
Definition H01_theoretical : R := 4 * phi^3 * (exp 1)^2.
```

Three candidate derivations were investigated and rejected:

**PATH A — e^2 as H4 geometric invariant**: RULED OUT
- `phi^4 = 6.854` is 7.24% off from `exp(1)^2 = 7.389`
- Lucas identity `phi^4 + phi^{-4} = L(4) = 7` is 5.56% off
- `3*pi^2/4 = 7.402` is 0.18% off but has no H4 geometric origin
- No combination of H4 integers {2, 12, 20, 30, 1, 11, 19, 29, 120, 720, 1200, 600, 14400} produces 7.389

**PATH B — e^2 = 4*pi*alpha_QED at some scale**: RULED OUT
- Code explicitly uses `exp(1)`, not the elementary charge
- `4*pi*alpha_em(M_Z) = 4*pi/127.94 = 0.0982` — factor 75x too small
- Required alpha ~ 0.588 (i.e., 1/alpha ~ 1.70) has no physical meaning in this context

**PATH C — empirical fit**: ACCEPTED
- `exp(1)^2 = 7.38906`, required factor `= 125.20 / (4*phi^3) = 7.38893`
- Agreement within 0.001 is a numerical coincidence
- No H4 / Coxeter / spectral-triple mechanism selects `exp(1)` as the Higgs scale factor
- Formally declared in `e2_empirical_fit` theorem (Qed)

### Status update

The "e^2 Mystery" flagged in `lagrangian_roadmap.md` under cross-cutting issues is now **formally investigated and closed as unresolved**: the factor is confirmed empirical. It joins `delta_CP` falsification and the `a4` 60x discrepancy as documented open problems.

The numerical accuracy of the formula (0.02 sigma agreement with PDG 2024) is unaffected — it remains a verified numerical coincidence per `trinity_formula_accurate` (Qed).
