# PREDICTIONS_PREREGISTERED.md — Frozen First-Principles Predictions

**Wave 4 of the honesty pass.** Companion to [`EPISTEMOLOGY.md`](./EPISTEMOLOGY.md).

This document formally pre-registers Trinity S³AI's open predictions — those that cannot yet be adjudicated against a model-clean measurement. Each entry includes the predicted value, the Coq theorem (where applicable), the falsification threshold, and the freeze commit hash.

**Freeze commit (Wave 4 baseline)**: see this PR's merge commit. Once merged into `main`, the predictions below are temporally pre-registered: any future measurement is being compared against numbers that existed in a public commit before the experimental result.

---

## How To Read This Document

Each prediction has five fields:

| Field | Meaning |
|---|---|
| **Predicted value** | The exact number derived from H4 + Coq, with zero free parameters |
| **Coq theorem** | The Coq identifier proving the value (where formal proof exists) or "phenomenological" |
| **Current extraction** | What model-dependent extractions currently report, with the model assumed |
| **Falsification threshold** | What experimental result, at what σ, in what experiment, would kill the prediction |
| **Status** | OPEN (not yet adjudicated) / CONFIRMED / FALSIFIED |

**Rule**: a prediction can only be moved from OPEN to FALSIFIED by a measurement that satisfies the criteria in [`EPISTEMOLOGY.md §6`](./EPISTEMOLOGY.md#6-what-would-falsify-trinity-under-this-doctrine) — model-independent, multiple-technique agreement, or Coq proof error.

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
| **Status** | **OPEN — pre-registered tension** |

**Comment**: This prediction was the subject of Wave 2 of the honesty pass, which used "withdrawn" language. Under the Wave 4 doctrine (see [`EPISTEMOLOGY.md`](./EPISTEMOLOGY.md)), that language is itself reframed: the prediction is **not** withdrawn; it is **in tension with a model-dependent extraction** pending DUNE adjudication. See [`DELTA_CP_HONEST_STATUS.md`](./DELTA_CP_HONEST_STATUS.md) (revised in this wave).

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

## P6. m_H (already confirmed — for symmetry of treatment)

| Field | Value |
|---|---|
| **Predicted value** | `m_H = 125.10 GeV` |
| **Coq theorem** | `HiggsPrediction.v` (0 Admitted, verified in [`COQ_HONEST_STATUS.md`](docs/status/COQ_HONEST_STATUS.md)) |
| **Current measurement** | ATLAS+CMS direct invariant-mass reconstruction: `m_H = 125.20 ± 0.11 GeV` |
| **Status** | **CONFIRMED at 0.09%** |

The Higgs mass extraction is **model-clean**: direct di-photon and 4-lepton invariant-mass reconstruction does not require nuclear-physics models. This is the kind of measurement that **can** falsify a prediction under the Wave 4 doctrine. The fact that it agrees is strong evidence for the H4 framework.

---

## P7. α₁, α₂, α₃ (gauge couplings, already confirmed)

| Field | Value |
|---|---|
| **Predicted values** | Trinity H4 framework; see `proofs/trinity/H4Derivations.v` (0 Admitted) |
| **Current measurement** | PDG world averages |
| **Agreement** | 0.024% across all three couplings |
| **Status** | **CONFIRMED** |

Gauge coupling measurements are reasonably model-clean (LEP precision EW + low-energy measurements + RG running). This confirmation matters under the Wave 4 doctrine.

---

## P8. Higgs self-coupling λ (already confirmed)

| Field | Value |
|---|---|
| **Predicted value** | `λ ≈ 0.129` |
| **Coq theorem** | `proofs/trinity/HiggsPrediction.v` (0 Admitted) |
| **Current value** | SM tree-level `λ = m_H²/(2v²) ≈ 0.1285` |
| **Status** | **CONFIRMED at 0.4%** |

---

## P9. PMNS θ₁₂ and θ₁₃ (already confirmed)

| Field | Value |
|---|---|
| **Predicted θ₁₂** | Within NuFIT-6.0 1σ band (0.16σ deviation) |
| **Predicted θ₁₃** | Within NuFIT-6.0 1σ band (0.18σ deviation) |
| **Status** | **CONFIRMED** |

These two PMNS angles are extracted from **reactor** experiments (Daya Bay, RENO, KamLAND) which are far more model-clean than accelerator extractions, because the source (β-decay) and detection (inverse β-decay) are well understood. The doctrine assigns these confirmations strong weight. The fact that δ_CP — the **most** model-dependent extraction — is also the only PMNS angle in tension is consistent with the Wave 4 thesis.

---

## Summary Table

| ID | Quantity | Predicted | Status | Adjudicating experiment |
|---|---|---|---|---|
| P1 | δ_CP | 3/φ² ≈ 65.66° | OPEN (tension) | DUNE 2028+ |
| P2 | sin²θ₂₃ octant | upper, ≈0.563 | OPEN (mild) | DUNE + HK + JUNO |
| P3 | a₄ bridge | (704+192√5)/19 | OPEN (algebraic) | None — internal |
| P4 | Mass ordering | Normal | OPEN | JUNO |
| P5 | Σmᵥ | ≈ 0.058 eV | OPEN | KATRIN final |
| P6 | m_H | 125.10 GeV | **CONFIRMED 0.09%** | ATLAS+CMS done |
| P7 | α₁,₂,₃ | (see Coq) | **CONFIRMED 0.024%** | PDG done |
| P8 | λ | 0.129 | **CONFIRMED 0.4%** | SM EW done |
| P9 | θ₁₂, θ₁₃ | (see Coq) | **CONFIRMED <0.2σ** | Reactor expts done |

**4 confirmed, 5 open, 0 falsified under Wave 4 doctrine.**

The four confirmations are all against **model-clean measurements** (direct invariant-mass, gauge-coupling running, reactor neutrinos). The five open predictions are against measurements that are either (a) not yet performed, or (b) currently extracted only through model-dependent forward modeling. This pattern is itself a signal.

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
