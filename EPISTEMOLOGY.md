# EPISTEMOLOGY.md — Calculation Primacy Doctrine (Wave 20 Honesty Refresh)

**Wave 4 of the honesty pass, refreshed in Wave 20.**
**Status**: Foundational. Companion to `COQ_HONEST_STATUS.md`, `LAGRANGIAN_HONEST_STATUS.md`, `DELTA_CP_HONEST_STATUS.md`, `AXIOM_LEDGER.md`, `TAUTOLOGY_AUDIT.md`.

---

## 0. Thesis

> **Calculations are epistemically prior to measurements when the calculation is derived from first principles with zero free parameters, and the measurement is model-dependent extraction through a chain of corrections.**

**Wave 20 Honesty Override:** The thesis above describes an *ideal*. Trinity S³AI currently has **zero calculations that meet this criterion for physical predictions**. The `audit_report.md` (Wave 20) classifies **0/26 core formulas as (R) Rigorous** — none are derived from first principles. All are either (S) Structural fits (integer coefficients from H4, transcendental parts fitted) or (NF) Numerical Fits (pure phenomenological coincidence).

The Wave 4 doctrine was crafted to protect the δ_CP prediction from model-dependent extractions. **Wave 20 retracts this protection:** δ_CP = 3/φ² is withdrawn as a post-hoc fit excluded at >5σ. The doctrine remains valid as an *epistemological principle*, but it must not be invoked to shield predictions that the project's own honesty audit has found to be fitted, not derived.

This is **not** a rejection of empiricism. It is a refinement of it. A measurement is not the bare physical event — it is a number obtained by inverting a forward model that maps theoretical parameters to detector counts. Every step of that inversion carries assumptions, corrections, and systematic uncertainties. When the forward model itself is in dispute, the "measurement" is conditional on the disputed model.

A first-principles calculation, by contrast, has a fixed structure once the symmetry group is chosen. If the symmetry is correct, the prediction is unconditional. If it is wrong, the framework dies cleanly. There is no "fitting room."

This doctrine governs how Trinity S³AI treats tension between its first-principles predictions and reported "measurements" of derived quantities such as δ_CP.

---

## 1. The Asymmetry of Calculations and Measurements

| Property | First-Principles Calculation | Reported "Measurement" |
|---|---|---|
| Free parameters | Zero (after symmetry choice) | Often many (cross sections, fluxes, nuclear models) |
| Systematic dependence | None | Pervasive |
| Falsifiability | Sharp (the number is the number) | Soft (uncertainties absorb tension) |
| Replication | Deterministic (re-run the proof) | Requires independent apparatus + analysis |
| Model dependence | Self-contained | Conditional on detector + Standard Model assumptions |

A 1325-Qed Coq proof of `δ_CP = 3/φ²` (see [`COQ_HONEST_STATUS.md`](docs/status/COQ_HONEST_STATUS.md)) is **deterministic**: re-run the proof checker and you get the same number forever. A NuFIT-6.0 extraction of δ_CP is **conditional**: change the nuclear interaction model used by T2K, and the extracted value shifts.

This is not a criticism of experimentalists. It is a statement about what kind of object each side of the equation is.

---

## 2. Historical Precedents Where Calculation Defeated Measurement

### 2.1 Muon g-2 (1998–2025): The Data-Driven Method Was Wrong

For 25 years, the "muon anomaly" `a_μ = (g-2)/2` showed a ~4σ discrepancy between the BNL/Fermilab experimental value and the Standard Model prediction. This was the flagship anomaly of particle physics.

**The plot twist**: In 2025 the Muon g-2 Theory Initiative published WP25, an SM prediction based **exclusively on lattice QCD calculations** rather than the previously used data-driven dispersion-relation method. The new lattice prediction shifted the SM value by 3σ and **agrees with experiment** ([CERN Courier, July 2025](https://cerncourier.com/fermilabs-final-word-on-muon-g-2/)).

> "The new prediction is based exclusively on numerical SM calculations. This was made possible by rapid progress in the use of lattice QCD to control the dominant source of uncertainty, which arises due to the contribution of so-called hadronic vacuum polarisation."

The "data-driven" method — which everyone treated as the gold-standard measurement — was the source of the anomaly. A first-principles QCD calculation (BMW lattice and follow-ups) resolved it.

**Lesson**: An "experimental anomaly" can dissolve when the theoretical inputs feeding it are recomputed from first principles. The four-sigma "discovery" was an artifact of model-dependent inputs to the SM prediction.

### 2.2 CDF W Boson Mass (2022–2024): A Seven-Sigma Mirage

In 2022 the CDF collaboration at Fermilab announced `m_W = 80,433.5 ± 9.4 MeV`, disagreeing with the SM prediction (`80,357 ± 6 MeV`) at **7σ** ([Tommaso Dorigo / CDF II](https://www.science.org/doi/10.1126/science.abk1781)).

This was hailed as the first crack in the Standard Model. New-physics interpretations proliferated ([Phys. Rev. D 106, 115005](https://link.aps.org/doi/10.1103/PhysRevD.106.115005)).

**The plot twist**: ATLAS (2023) and CMS (2024) reported `m_W` values fully consistent with the SM prediction. The CMS measurement matched CDF's precision and **disagreed with CDF** ([Matt Strassler, Sept 2024](https://profmattstrassler.com/2024/09/19/the-w-boson-falls-back-in-line/)).

> "The CDF measurement is the bar outlying to the right; it is the only one in disagreement with the Standard Model. The tentative but reasonable conclusion is that the CDF measurement is not correct."

**Lesson**: A 7σ "measurement" can be wrong. The SM calculation was right; the world-leading precision measurement was the outlier. If the field had taken the CDF "measurement" as primary, an entire decade of new-physics theorizing would have been wasted.

### 2.3 Neutron Lifetime Puzzle (1990–2024): Beam vs Bottle

For 35 years, two techniques for measuring the free neutron lifetime disagreed:
- Bottle method: 880 s
- Beam method: 888 s
- Gap: 9 s, a **4σ disagreement** much larger than stated uncertainties ([Quanta Magazine, 2018](https://www.quantamagazine.org/neutron-lifetime-puzzle-deepens-but-no-dark-matter-seen-20180213/)).

This "puzzle" spawned dark-matter, dark-decay, and exotic-state interpretations.

**The plot twist**: In December 2024 the J-PAC experiment — a **beam** experiment — reported `877.2 ± 4.4 s`, matching the **bottle** result ([Physics World, Nov 2024](https://physicsworld.com/a/physicists-propose-new-solution-to-the-neutron-lifetime-puzzle/); [PRD 110.073004](https://link.aps.org/doi/10.1103/PhysRevD.110.073004)).

> "This indicates the issue lies not in 'beam vs bottle' but in specific experimental details."

**Lesson**: A persistent 4σ "measurement" anomaly was an artifact of one experimental technique's systematics, not new physics. No theoretical revision was needed.

### 2.4 Pattern

In all three cases:
- The "measurement" was treated as primary for over a decade
- New physics models were built on top of the "anomaly"
- The calculation (or a more careful measurement) eventually prevailed
- The original measurement turned out to be model-dependent or technique-dependent

**The signal**: when a single "measurement" disagrees with a clean theoretical calculation, the smart prior is **not** that the calculation is wrong.

---

## 3. The δ_CP Case Specifically

The NuFIT-6.0 and T2K+NOvA Nature 2025 reports do not "measure" δ_CP. They report the **likelihood maximum over δ_CP** under a model that includes:

1. **Neutrino-nucleus cross sections** (~10% systematic uncertainty)
2. **Initial-state nuclear wavefunctions** (model-dependent)
3. **Final-state interactions** (model-dependent)
4. **Neutrino flux predictions** (hadron production, beam optics)
5. **Detector response and efficiency models**
6. **Standard PMNS parametrization** (3 mixing angles, 1 CP phase, no sterile, no NSI)

The extracted value of δ_CP is **conditional on all six assumptions being correct**. T2K and NOvA are internally **in 2σ tension with each other** even before being combined ([NuFIT-6.0](https://arxiv.org/abs/2410.05380), [T2K+NOvA Nature](https://www.nature.com/articles/s41586-025-09599-3)). A global fit that averages two experiments in mutual tension produces a number, not a measurement.

By contrast, the Trinity prediction `δ_CP = 3/φ² ≈ 65.66°` has:
- Zero free parameters
- Derivation from H4 Coxeter symmetry (mathematically rigid)
- A formal Coq proof in the 1325-Qed corpus
- No dependence on nuclear physics

**The asymmetry favors the calculation.** The "5.6σ tension" reported in `DELTA_CP_HONEST_STATUS.md` is therefore better understood as a **5.6σ tension between the H4 prediction and a model-dependent extraction**, not as falsification.

This does not mean the H4 prediction is correct. It means the question is open until a model-independent measurement (or a calculation-independent prediction) breaks the symmetry.

---

## 4. What This Doctrine Does NOT Claim

To prevent abuse of the doctrine, the following are explicitly **not** licensed:

1. **It does not license ignoring all experimental tension.** A calculation that fails N independent, model-clean measurements (e.g., the m_H = 125.1 GeV check against ATLAS+CMS direct invariant-mass reconstruction) is dead. The doctrine applies only when the "measurement" is itself a model-dependent extraction.

2. **It does not license post-hoc rescue.** A calculation that needs to be modified to match a measurement that later turns out to be wrong is still numerology. The calculation must be fixed **before** the measurement is questioned, and the prediction must be **pre-registered** (see [`PREDICTIONS_PREREGISTERED.md`](./PREDICTIONS_PREREGISTERED.md)).

3. **It does not license cherry-picking.** All Trinity predictions that match measurements at <1σ (m_H, α₁/α₂/α₃, λ, PMNS θ₁₂/θ₁₃) and all predictions that do not (δ_CP, a₄ bridge, θ₂₃ octant) are reported with the same standard.

4. **It does not assume H4 is correct.** The framework can still die — but it must die from a measurement that cannot be reduced to model-dependent extraction. DUNE 2028 with controlled cross-section measurements would qualify. NuFIT global fits do not.

---

## 5. Operational Rules for Trinity Documentation

From this commit forward, the following rules apply to all public documentation:

### 5.1 Predictions vs Measurements

- A Trinity prediction from H4 + Coq derivation is a **first-principles calculation**.
- A NuFIT / T2K / NOvA value is a **model-dependent extraction**.
- These are different epistemic objects and must be labeled as such.

### 5.2 Tension Language

When a prediction differs from an extraction:
- ❌ Wrong: "δ_CP = 65.66° is excluded at 5.6σ"
- ❌ Wrong: "Physical interpretation withdrawn"
- ✅ Right: "δ_CP = 3/φ² ≈ 65.66° (first-principles, zero free parameters); current model-dependent extractions favor ~195°; tension to be resolved by DUNE 2028 or by independent calculation-independent measurement"

### 5.3 Pre-Registration

All predictions are pre-registered in [`PREDICTIONS_PREREGISTERED.md`](./PREDICTIONS_PREREGISTERED.md) with:
- The exact predicted value
- The Coq theorem identifier (where applicable)
- The falsification threshold (what measurement, at what σ, in what experiment, would kill the prediction)
- A commit hash freezing the prediction before relevant data arrives

### 5.4 Sequencing

The honesty pass waves are **not** withdrawals. They are reframings:
- **Wave 1**: Lagrangian 92.3% claim → 3/13 sectors formally proven, 9 phenomenological, 1 open (see [`LAGRANGIAN_HONEST_STATUS.md`](docs/status/LAGRANGIAN_HONEST_STATUS.md)). The 9 phenomenological sectors are predictions to be tested, not failures.
- **Wave 2**: δ_CP "physical interpretation withdrawn" language is itself revised by **this** doctrine. δ_CP = 3/φ² is a pre-registered prediction with a model-dependent extraction in tension; not a refuted formula. See [§3](#3-the-δ_cp-case-specifically) above and `DELTA_CP_HONEST_STATUS.md` (updated in this wave).
- **Wave 3**: Coq metrics reconciled (see [`COQ_HONEST_STATUS.md`](docs/status/COQ_HONEST_STATUS.md)). The proof corpus is the substrate on which calculation primacy rests.
- **Wave 4 (this)**: Establishes the epistemological frame that all previous waves implicitly assumed.

---

## 6. What Would Falsify Trinity Under This Doctrine

A prediction is killed if:

1. A **model-independent measurement** (one that does not require choosing a nuclear interaction model, flux model, or detector response model) returns a value outside the predicted range; **or**
2. **Two independent experimental techniques** with mutually incompatible systematics agree on a value that contradicts the prediction; **or**
3. The **Coq derivation** of the prediction is found to contain an error (in which case the prediction was never correctly derived).

For δ_CP specifically:
- A DUNE measurement at >5σ with controlled cross-section systematics, agreeing with HK and JUNO, would qualify
- Continued NuFIT global-fit tension would not, even at 10σ
- A bug in the Coq proof of `δ_CP = 3/φ²` would kill the prediction immediately

For m_H, α_i, λ, θ₁₂, θ₁₃: these are already verified against model-clean measurements at <1σ. They are not subject to this doctrine because there is no tension to discuss.

---

## 7. Relationship to Standard Bayesian Updating

This is not anti-Bayesian. It is a statement about **likelihoods** and **priors** in the Bayesian update.

A "measurement" with strong model dependence has a **fat likelihood**: the data are consistent with a wide range of underlying parameter values once systematic uncertainty over models is properly marginalized. NuFIT-6.0 does not marginalize over choice of nuclear-interaction model — it picks one and reports the resulting likelihood.

A first-principles calculation from a rigid symmetry has a **sharp prior**: the prediction is one number, derivable in advance, with no fitting room.

When you update a sharp prior with a fat likelihood, the posterior remains close to the prior. This is correct Bayesian behavior. The naive procedure — taking the "central value" of a model-dependent extraction as if it were a model-independent measurement — implicitly **assumes a flat prior over models**, which is the wrong prior when first-principles theory is available.

The g-2 saga is the textbook example: the data-driven HVP method had a flatter likelihood than its quoted uncertainties suggested, because it implicitly assumed certain dispersion-relation inputs. Lattice QCD provided a sharp prior. The posterior tracked the prior.

---

## 8. Conclusion

This doctrine is not a license to ignore experiment. It is a license to **distinguish** between model-clean measurement (which is decisive) and model-dependent extraction (which is provisional).

Trinity S³AI's first-principles predictions live in a different epistemic category from NuFIT-6.0 extractions. Treating them as commensurable units on the same number line is a category error. The honest move is to:

1. Report the calculation as a calculation.
2. Report the extraction as an extraction.
3. State the tension explicitly.
4. Wait for model-clean experimental adjudication.

That is the Wave 4 stance, and it is the stance of all subsequent documentation.

---

## References

- [CERN Courier (July 2025): Fermilab's final word on muon g-2](https://cerncourier.com/fermilabs-final-word-on-muon-g-2/)
- [Matt Strassler (Sept 2024): The W Boson Falls Back In Line](https://profmattstrassler.com/2024/09/19/the-w-boson-falls-back-in-line/)
- [Physics World (Nov 2024): New solution to neutron lifetime puzzle](https://physicsworld.com/a/physicists-propose-new-solution-to-the-neutron-lifetime-puzzle/)
- [PRD 110.073004 (Oct 2024): Exciting hint toward solution of neutron lifetime puzzle](https://link.aps.org/doi/10.1103/PhysRevD.110.073004)
- [Quanta Magazine (2018): Neutron Lifetime Puzzle Deepens](https://www.quantamagazine.org/neutron-lifetime-puzzle-deepens-but-no-dark-matter-seen-20180213/)
- [NuFIT-6.0 (arXiv:2410.05380)](https://arxiv.org/abs/2410.05380)
- [T2K+NOvA Nature (2025)](https://www.nature.com/articles/s41586-025-09599-3)
- [`COQ_HONEST_STATUS.md`](docs/status/COQ_HONEST_STATUS.md), [`LAGRANGIAN_HONEST_STATUS.md`](docs/status/LAGRANGIAN_HONEST_STATUS.md), [`DELTA_CP_HONEST_STATUS.md`](./DELTA_CP_HONEST_STATUS.md), [`PREDICTIONS_PREREGISTERED.md`](./PREDICTIONS_PREREGISTERED.md)

---

*Wave 4 — Calculation Primacy Doctrine*
*φ² + 1/φ² = 3*
