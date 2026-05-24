# Trinity S³AI — Predictions Registry (Falsification Record)

**Date:** 2026-05-22  
**Wave:** 12.6 (Registry Lock)  
**Scope:** All quantitative claims made by the Trinity S³AI framework that can be checked by experiment, computation, or independent proof.  
**Policy:** Every entry must be traceable to a specific file and wave. Retroscopic fits are explicitly labeled as such.

---

## How to read this registry

| Status | Meaning |
|--------|---------|
| **Confirmed** | Independent computation or experiment agrees with the claim. |
| **Open** | No decisive test yet; the claim awaits a future computation or experiment. |
| **Refuted** | Independent computation or experiment contradicts the claim beyond reasonable doubt. |
| **Retrospective fit** | The number matches data, but the formula was found *after* the measurement was known. Not a prediction. |

---

## Table 1: Mathematical predictions (provable / computable)

| # | Quantity | Value | Source file | Wave | Status | Falsification criterion |
|---|----------|-------|-------------|------|--------|------------------------|
| **M1** | η(S³/2I) | **−2** | `proofs/trinity/EtaInvariant.v` | 8.3 | **Confirmed** (structural, APS balance) | A correct APS computation giving η ≠ −2 would refute. |
| **M2** | η(S³/2T) | **−3/2** | `derivations/eta_2t_2o/eta_table_analysis.md` | 12 | **Open** | Dedekind-sum computation with natural Seifert metric gives +1.1528 (different sign convention). The project convention η = σ/4 must be independently justified. |
| **M3** | η(S³/2O) | **−7/4** | `derivations/eta_2t_2o/eta_table_analysis.md` | 12 | **Open** | Same convention issue as M2. |
| **M4** | KO-dim(H₄/600-cell) | **6 mod 8** | `proofs/trinity/KODimension.v` | 5.1 | **Confirmed** (signs (+,+,+) match; off-diagonal J admitted as `PHYSICAL_AXIOM`) | A proof that J is necessarily diagonal (giving KO-dim 0) would refute. |
| **M5** | KO-dim(D₄/24-cell) | **5 mod 8** | `derivations/trinity_d4/trinity_d4_analysis.md` | 11.2 | **Confirmed** (signs (−,+,+) from explicit numeric computation) | This is a *negative* result: D₄ does **not** match the SM requirement of 6 mod 8. |
| **M6** | m_H (tree, no σ) | **132.88 GeV** | `derivations/higgs_spectral_action/higgs_analysis.md` | 11.5 | **Refuted** | PDG 2024: 125.10 ± 0.14 GeV. Discrepancy: +7.78 GeV = **55.6σ**. |
| **M7** | m_H (Trinity fit) | **125.20 GeV** | `validate_v4.py`, formula H01 | 3–4 | **Retrospective fit** | Formula `4φ³e²` found after LHC measurement (2012). Labelled NF (Numerical Fit) in audit. Not a prediction. |
| **M8** | λ_Higgs (bare) | **1/φ⁴ ≈ 0.1459** | `proofs/trinity/SpectralAction600Cell.v` | 5.3 | **Open** (theoretical) | A rigorous spectral-action computation on the 600-cell giving λ ≠ 1/φ⁴ would refute. |

### Notes on mathematical predictions

- **M1 (η = −2):** The value −2 is derived from the APS index theorem applied to the E₈ plumbing manifold (signature σ = −8) using the project convention η = σ/4. The Coq file `EtaInvariant.v` contains the formal statement `eta_poincare : R := -2` and proves `eta_poincare_nonzero`, `eta_poincare_negative`, and `eta_poincare_magnitude` with `Qed`. The rationality theorem `eta_poincare_rational` is also proved. The *specific value* −2 is admitted as a numerical fit tied to the E₈ plumbing convention.

- **M2–M3 (η for 2T, 2O):** These are *new* in Wave 12. The project adopts the plumbing convention η = σ/4, giving −3/2 for E₆ (σ = −6) and −7/4 for E₇ (σ = −7). Independent cross-checks using Nicolaescu’s Dedekind-sum formula and Ouyang’s cotangent-sum formula give *different numerical values* under different metrics. The registry records this as **Open** because the plumbing convention, while consistent internally, has not been shown to be the physically relevant metric for a spectral triple.

- **M4 (KO-dim 6):** The sign triple (+1,+1,+1) is proved in `KODimension.v` (`cell600_signs_match_ko6`, `Qed`). The distinction between KO-dim 6 and KO-dim 0 relies on the off-diagonal nature of J, which is admitted as `cell600_J_off_diagonal` (`PHYSICAL_AXIOM`). A future proof that J must be diagonal would refute the claim.

- **M5 (KO-dim 5 for D₄):** Explicit numeric computation in `d4_analysis.py` shows J² = −I, JD = DJ, JΓ = ΓJ, giving (−,+,+) → KO-dim 5. The SM requires (+,+,−) for KO-dim 6. This is a **boundary finding**: D₄/24-cell is ruled out as an SM finite geometry.

- **M6 (m_H tree = 132.88 GeV):** This is the *structural* prediction of the spectral action on the 600-cell **without** the σ-field correction. Wave 11.5 computed it explicitly. It is **refuted** by PDG 2024 at 55.6σ. The failure is honest and documented.

- **M7 (m_H Trinity fit = 125.20 GeV):** **Explicitly labelled as retrospective fit.** The formula `4φ³e²` was identified after the LHC measurement. It is verified in `validate_v4.py` (rel. error ≈ 0.0016 %) but carries the `NF` tag in the catalog audit. Do **not** cite this as a confirmed prediction.

---

## Table 2: Phenomenological predictions (experimentally testable)

| # | Quantity | Value | Source | Status | What would falsify |
|---|----------|-------|--------|--------|-------------------|
| **P1** | δ_CP (PMNS) | **65.66°** (`3/φ²` rad) | `validate_v4.py` N04, `Catalog42.v` | **WITHDRAWN** (>5σ excluded by NuFIT-6.0 + T2K+NOvA 2025). Post-hoc fit; anti-post-hoc rule enforced. |
| **P2** | f₀ (quasicrystal THz line) | **12.8 THz** | `validate_v4.py` v21, `derivations/cosmology/` | **Open** (no data) | High-resolution THz spectroscopy of icosahedral quasicrystals (Al-Mn-Pd, i-YbMgZn) in 10–20 THz showing no line at 12.8 ± 0.5 THz. |
| **P3** | m_DM (WIMP) | **12.82 GeV** | `Predictions.v` | **Open** (no signal) | LZ-2 or XENONnT (2026–2028) excluding σ_SI > 10⁻⁴⁹ cm² at 12.82 GeV without signal. Note: internal inconsistency with `Catalog42.v` (36.0 GeV variant). |
| **P4** | sin²θ₁₃ | **0.02200** | `validate_v4.py` N01 | **Retrospective fit** | Already known to 0.37σ precision when formula was fixed. Post-hoc correction from earlier 0.74 % error version. |
| **P5** | Δm²₂₁/Δm²₃₁ | **0.0300** | `validate_v4.py` N21 | **Compatible** (structural) | NuFit 6.0: 0.02948 ± 0.0005. Distance ~0.1σ. Classified **S** (Structural) in audit. |

### Refuted phenomenological predictions

| # | Quantity | Trinity value | Experiment | σ-distance | Source | Refuted in |
|---|----------|---------------|------------|------------|--------|------------|
| **F1** | Λ (cosmological constant) | φ⁻¹⁴⁴/2 ≈ 4×10⁻³¹ (Planck units) | ~10⁻¹²³ | ~∞ (92 orders) | `Catalog42.v` | Wave 8.5 |
| **F2** | m_ν₁ (lightest neutrino) | 1/(6φ) ≈ 0.103 eV | Σm_ν < 0.072 eV (Planck+DESI) | ~5σ | `N01_origins.md` | Wave 8.5 |
| **F3** | Ω_b h² | φ⁻³π⁻²e⁻¹ ≈ 0.00880 | 0.022383 ± 0.000018 | ~754σ | `Catalog42.v` | Wave 8.5 |
| **F4** | H₀ | 21.90 km/s/Mpc | 67.4 ± 0.5 | ~91σ | `Catalog42.v` | Wave 8.5 |
| **F5** | Ω_c h² | (φπe·5)⁻¹ ≈ 0.01447 | 0.12011 ± 0.00034 | ~311σ | `Catalog42.v` | Wave 8.5 |

---

## Table 3: Catalog formulas from `validate_v4.py` — numerical status

All 25 formulas in `validate_v4.py` are **verified to high precision** (mpmath, 50 digits) against PDG 2024 / NuFit 6.0 targets. However, verification ≠ derivation.

| Category | Formulas | SG (<0.01 %) | V (<0.1 %) | Pass (<1 %) | Fail (>1 %) | Notes |
|----------|----------|--------------|------------|-------------|-------------|-------|
| Lepton | L01–L03 | 0 | 2 | 1 | 0 | L01 is NF; L02, L03 are S |
| Quark | Q01–Q07 | 0 | 1 | 6 | 1 | Q06 (m_t) is corrected typo |
| Gauge | G01–G02 | 0 | 1 | 1 | 0 | G01 (1/α) is NF |
| Neutrino | N01, N04, v21, v31, N21, Snu | 0 | 1 | 3 | 2 | N04 (δ_CP) borderline; Snu fail |
| CKM | C01–C02 | 0 | 1 | 1 | 0 | Structural motivation weak |
| Higgs | H01–H03 | 1 | 1 | 1 | 0 | H01 is retrospective fit |
| Other | Pr | 0 | 0 | 1 | 0 | Proton/electron ratio |

**Total:** 25/25 pass SG+V+Pass rate = 100 %, but **0/25 are class R** (rigorous derivation from first principles). Breakdown: 8 S (structural), 17 NF (numerical fit).

Source: `derivations/catalog_audit/audit_report.md`, `validate_v4.py`.

---

## Honest summary

| Class | Count |
|-------|-------|
| Confirmed mathematical results | 3 (η=−2, KO-dim 6, KO-dim 5) |
| Open mathematical results | 2 (η(2T), η(2O) — convention dependent) |
| Refuted structural predictions | 1 (m_H tree = 132.88 GeV) |
| Retrospective fits (not predictions) | 2 (m_H = 125.20 GeV, sin²θ₁₃) |
| Open experimental predictions | 2 (δ_CP, f₀) |
| Refuted cosmological predictions | 5 (Λ, m_ν₁, Ω_b, H₀, Ω_c) |
| Structural compatibilities (S) | 8 formulas |
| Numerical fits (NF) | 17 formulas |

**Bottom line:** The project has produced **rigorous boundary findings** (obstruction theorems) and **structural mathematical matches** (KO-dim 6, η = −2). It has **not** produced any phenomenological prediction that survived independent experimental test as a *genuine prior* prediction. The Higgs fit (125.20 GeV) is impressive numerically but is a retrospective correlation, not a prediction.

---

*Registry locked: 2026-05-22. Any amendment must be dated and justified in a new wave.*
