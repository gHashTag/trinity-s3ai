# PREDICTIONS_PREREGISTERED.md — Frozen Predictions (Wave 20 Honesty Refresh)

**Wave 4 of the honesty pass, refreshed in Wave 20.** Companion to [`EPISTEMOLOGY.md`](./EPISTEMOLOGY.md).

**CRITICAL HONESTY DISCLAIMER (Wave 20):** This document pre-registers predictions, but *none* of them are derived from first principles. The Coq theorems listed prove **interval bounds** (`|formula - value| < ε`), not physical derivations. "Confirmed" means "numerical coincidence matches experiment within the stated window" — it does **not** mean the H4 framework predicted the value. See [`audit_report.md`](derivations/catalog_audit/audit_report.md) for the canonical classification: **0/26 formulas are rigorous derivations.**

This document formally pre-registers Trinity S³AI's open predictions — those that cannot yet be adjudicated against a model-clean measurement. Each entry includes the predicted value, the Coq theorem (where applicable), the falsification threshold, and the freeze commit hash.

**Freeze commit (Wave 4 baseline)**: see this PR's merge commit. Once merged into `main`, the predictions below are temporally pre-registered: any future measurement is being compared against numbers that existed in a public commit before the experimental result.

---

## How To Read This Document

Each prediction has five fields:

| Field | Meaning |
|---|---|
| **Predicted value** | The exact number fitted from H4 invariants + φ/π/e, with zero free parameters after the fit |
| **Coq theorem** | The Coq identifier proving an **interval bound** on the formula's numerical accuracy, not a physical derivation |
| **Current extraction** | What model-dependent extractions currently report, with the model assumed |
| **Falsification threshold** | What experimental result, at what σ, in what experiment, would kill the prediction |
| **Status** | OPEN (not yet adjudicated) / WITHDRAWN / FALSIFIED / NUMERICALLY VERIFIED (not "confirmed" in the theoretical sense) |

**Rule**: a prediction can only be moved from OPEN to FALSIFIED by a measurement that satisfies the criteria in [`EPISTEMOLOGY.md §6`](./EPISTEMOLOGY.md#6-what-would-falsify-trinity-under-this-doctrine) — model-independent, multiple-technique agreement, or Coq proof error. However, **Wave 20 override**: δ_CP is withdrawn regardless of doctrine, because the project's own honesty audit (`DELTA_CP_HONEST_STATUS.md`) found it was a post-hoc fit excluded at >5σ.

---

## P1. δ_CP (Dirac CP-violating phase in PMNS)

| Field | Value |
|---|---|
| **Predicted value** | `δ_CP = 3/φ² ≈ 65.6620° ≈ 1.1461 rad` |
| **Derivation** | Phenomenological in `proofs/trinity/Predictions.v`; framework derivation from H4 Coxeter invariants |
| **Coq theorem** | `delta_cp_value` (Predictions.v) — value is `Definition`-level, not yet a derived theorem from H4 generators alone |
| **Current extraction** | NuFIT-6.0 favors `δ_CP ≈ 195° ± 25°` (NO ordering, model-dependent extraction); T2K-only and NOvA-only are in mutual 2σ tension |
| **Sources** | [NuFIT-6.0](https://arxiv.org/abs/2410.05380), [T2K+NOvA Nature 2025](https://www.nature.com/articles/s41586-025-09599-3), [arXiv:2510.19888](https://arxiv.org/abs/2510.19888) |
| **Falsification threshold** | DUNE 2028+ reporting `δ_CP` outside `[50°, 80°]` at ≥5σ **with explicit cross-section systematic budget bounded by independent measurements (MINERvA, T2K-NIR)**, **agreeing with Hyper-Kamiokande within 1σ on the same quantity** |
| **NOT falsification** | NuFIT global-fit central value drifting; T2K or NOvA in isolation; any extraction whose nuclear-model systematic is treated as gaussian |
| **Status** | **WITHDRAWN — post-hoc fit excluded at >5σ** |

**Comment (Wave 20 refresh):** This prediction was the subject of Wave 2 of the honesty pass, which used "withdrawn" language. Under the Wave 4 doctrine (see [`EPISTEMOLOGY.md`](./EPISTEMOLOGY.md)), that language was reframed as "in tension with model-dependent extraction." **Wave 20 overrides this reframing.** The project's own `DELTA_CP_HONEST_STATUS.md` documents that δ_CP = 3/φ² was found by **brute-force search over a·φ^b·π^c·e^d targeting an outdated PDG value** (65.5° ± 1.6°). Three formula revisions (90.2° → 77.87° → 65.66°) constitute the signature of post-hoc fitting. NuFit 6.0 + T2K+NOvA 2025 exclude 65.66° at >5σ. The physical interpretation is **withdrawn**; the Coq lemma `delta_cp_value` is preserved as a mathematical curiosity, not a prediction. See [`DELTA_CP_HONEST_STATUS.md`](./DELTA_CP_HONEST_STATUS.md).

---

## P2. θ₂₃ octant (atmospheric mixing angle)

| Field | Value |
|---|---|
| **Predicted value** | Trinity H4 derivation places `sin²θ₂₃` in the **upper octant** (>0.5), specifically near `sin²θ₂₃ ≈ 0.563` |
| **Coq theorem** | Phenomenological — see `proofs/trinity/Bounds_Mixing.v` and `proofs/trinity/Predictions.v` |
| **Current extraction** | NuFIT-6.0 has a slight upper-octant preference at ~1.7σ; T2K-only prefers maximal mixing; NOvA-only prefers upper octant |
| **Sources** | [NuFIT-6.0](https://arxiv.org/abs/2410.05380) |
| **Falsification threshold** | Combined DUNE + HK + JUNO reporting `sin²θ₂₃ < 0.45` at ≥5σ with reactor + accelerator agreement |
| **NOT falsification** | Single-experiment fluctuation; global fit central value crossing 0.5 |
| **Status** | **OPEN — mild tension, prediction in NuFIT 1σ range** |

---

## P3. a₄ bridge problem (H4 invariant ratio anomaly)

| Field | Value |
|---|---|
| **Predicted value** | Trinity computes `a₄ = (704 + 192√5)/19 ≈ 59.6487` |
| **Coq theorem** | Formalized in Coq (see `proofs/trinity/Catalog42.v`, [`README_v46.md` row 3](archive/legacy/README_v46.md)) |
| **Current extraction** | Phenomenological target is ~60; observed ratio is `≈ 1.0006 × predicted`, a 0.59% offset |
| **Falsification threshold** | A model-independent derivation (from H4 alone, no auxiliary input) producing a value outside `[59.5, 60.5]` and **matching observation** would falsify the H4 hypothesis; alternatively, exact-integer 60 emerging as the true target with no algebraic interpretation would weaken the H4 claim |
| **NOT falsification** | The 0.59% offset itself — Trinity is honest that this is not exactly 60 ([`README_v46.md` row 3](archive/legacy/README_v46.md)) |
| **Status** | **OPEN — formalized as exact algebraic number, phenomenological target unclear** |

---

## P4. Neutrino mass ordering

| Field | Value |
|---|---|
| **Predicted value** | Trinity H4 framework predicts **normal ordering** (NO): `m₁ < m₂ < m₃` |
| **Coq theorem** | Phenomenological — `proofs/trinity/NeutrinoOrigins.v` |
| **Current extraction** | NuFIT-6.0 favors NO at ~2.5σ; cosmological bounds (Planck + BAO + DESI) favor sum `Σmᵥ < 0.12 eV` consistent with NO |
| **Falsification threshold** | JUNO (reactor-based, model-clean) reporting **inverted ordering** at ≥5σ; or KATRIN reporting `m_β > 0.2 eV` at ≥5σ |
| **Status** | **OPEN — prediction consistent with current data** |

---

## P5. Sum of neutrino masses

| Field | Value |
|---|---|
| **Predicted value** | Trinity framework: `Σmᵥ ≈ 0.058 eV` (NO, smallest-mass scenario) |
| **Coq theorem** | Phenomenological |
| **Current extraction** | Planck+BAO+DESI 2024: `Σmᵥ < 0.072 eV` at 95% CL (cosmological, model-dependent on ΛCDM + neutrino-as-warm-DM assumptions) |
| **Falsification threshold** | KATRIN final report with `m_β < 0.05 eV` at ≥5σ ruling out the predicted scenario; cosmology cannot falsify alone due to model dependence (per [`EPISTEMOLOGY.md`](./EPISTEMOLOGY.md)) |
| **Status** | **OPEN — prediction inside current bounds** |

---

## P6. m_H (numerically verified coincidence)

| Field | Value |
|---|---|
| **Predicted value** | `m_H = 125.10 GeV` |
| **Coq theorem** | `HiggsPrediction.v` proves `Rabs(m_H_Trinity - m_H_measured) < 0.25` — an **interval bound**, not a derivation |
| **Current measurement** | ATLAS+CMS direct invariant-mass reconstruction: `m_H = 125.20 ± 0.11 GeV` |
| **Status** | **NUMERICALLY VERIFIED at 0.09%** |

**Honesty note:** The formula `m_H = 4φ³e²` was found **after** the LHC 2012 discovery. The Coq proof verifies that this fitted formula is close to the measured value; it does **not** derive the Higgs mass from H4 geometry. See `audit_report.md`: H01 is classified as NF (Numerical Fit), not R (Rigorous). Calling this "confirmed" would overstate the epistemic status.

---

## P7. α₁, α₂, α₃ (gauge couplings, numerically verified coincidence)

| Field | Value |
|---|---|
| **Predicted values** | Fitted formulas; see `proofs/trinity/H4Derivations.v` (0 Admitted) |
| **Current measurement** | PDG world averages |
| **Agreement** | 0.024% for 1/α(0); α_s has 0.1% error (above V-class threshold); sin²θ_W is a genuine 84σ failure (see G03) |
| **Status** | **NUMERICALLY VERIFIED (partial)** |

**Honesty note:** Only `1/α(0)` matches well. The strong coupling formula `α_s = (√5−2)/2` has 0.1% error and is absent from `Catalog42.v`. The weak mixing formula `sin²θ_W = 3/(8φ)` is **refuted at 84σ** (3.8% error, not an ultra-precision artifact). The "0.024% across all three couplings" figure cherry-picks the best match.

---

## P8. Higgs self-coupling λ (numerically verified coincidence)

| Field | Value |
|---|---|
| **Predicted value** | `λ ≈ 0.129` |
| **Coq theorem** | `proofs/trinity/HiggsPrediction.v` proves an interval bound |
| **Current value** | SM tree-level `λ = m_H²/(2v²) ≈ 0.1285`; experimental κ_λ = 1.02 ± 0.19 (ATLAS+CMS Run 2) |
| **Status** | **NUMERICALLY VERIFIED at 0.4%** |

**Honesty note:** The formula `λ = √φ/π²` was fitted, not derived. Experimental measurement of λ is weak (±15% uncertainty), so the "verification" is not stringent.

---

## P9. PMNS θ₁₂ and θ₁₃ (numerically verified coincidence)

| Field | Value |
|---|---|
| **Predicted θ₁₂** | Formula `8π/(φ⁵e²)` within NuFIT-6.0 1σ band (0.16σ deviation) |
| **Predicted θ₁₃** | Formula `π²/(25φ⁶)` within NuFIT-6.0 1σ band (0.18σ deviation) |
| **Status** | **NUMERICALLY VERIFIED** |

**Honesty note:** Both formulas were found by search over φ/π/e combinations, not derived from H4 geometry. The reactor-extraction argument is correct about model-cleanliness, but it does not turn a fitted coincidence into a prediction. The Wave 4 thesis that "model-dependent extractions are in tension while model-clean ones match" is a post-hoc pattern, not a pre-registered prediction.

---

## Summary Table

| ID | Quantity | Predicted | Status | Adjudicating experiment |
|---|---|---|---|---|
| P1 | δ_CP | 3/φ² ≈ 65.66° | **WITHDRAWN** (post-hoc fit, >5σ excluded) | N/A |
| P2 | sin²θ₂₃ octant | upper, ≈0.563 | OPEN (mild) | DUNE + HK + JUNO |
| P3 | a₄ bridge | (704+192√5)/19 | OPEN (algebraic) | None — internal |
| P4 | Mass ordering | Normal | OPEN | JUNO |
| P5 | Σmᵥ | ≈ 0.058 eV | OPEN | KATRIN final |
| P6 | m_H | 125.10 GeV | **NUMERICALLY VERIFIED 0.09%** | ATLAS+CMS done |
| P7 | α₁,₂,₃ | (see Coq) | **NUMERICALLY VERIFIED (partial)** | PDG done |
| P8 | λ | 0.129 | **NUMERICALLY VERIFIED 0.4%** | SM EW done |
| P9 | θ₁₂, θ₁₃ | (see Coq) | **NUMERICALLY VERIFIED <0.2σ** | Reactor expts done |

**0 confirmed (theoretical sense), 4 numerically verified, 4 open, 1 withdrawn under Wave 20 doctrine.**

The four numerical verifications are all against **model-clean measurements**, but they are verifications of fitted coincidences, not confirmations of theoretical predictions. The Wave 4 pattern thesis ("model-dependent extractions disagree, model-clean ones agree") is a post-hoc observation, not a pre-registered prediction. See [`DELTA_CP_HONEST_STATUS.md`](./DELTA_CP_HONEST_STATUS.md) and [`audit_report.md`](derivations/catalog_audit/audit_report.md) for the honest canonical status.

---

## Audit Trail

- **Freeze date**: 2026-05-23 (this PR merge)
- **Parent waves**:
  - Wave 1: [`LAGRANGIAN_HONEST_STATUS.md`](docs/status/LAGRANGIAN_HONEST_STATUS.md) (PR #21)
  - Wave 2: [`DELTA_CP_HONEST_STATUS.md`](./DELTA_CP_HONEST_STATUS.md) (PR #22; reframed by Wave 4)
  - Wave 3: [`COQ_HONEST_STATUS.md`](docs/status/COQ_HONEST_STATUS.md) (PR #23)
  - **Wave 4 (this)**: [`EPISTEMOLOGY.md`](./EPISTEMOLOGY.md) + this document
- **Modification policy**: predictions can be **added** but not **changed** after freeze. Any modification to an existing prediction must be a new entry P10+ with explicit cross-reference. Post-hoc parameter tuning would violate Wave 4 doctrine and be detectable in git history.

---

*φ² + 1/φ² = 3*
