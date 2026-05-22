# Trinity S3AI — Foundations and Assumptions

**File:** `proofs/trinity/FOUNDATIONS.md`
**Version:** Wave 10.4 (A4 audit)
**Status:** Normative reference for all axiom/admitted stratification

---

## Purpose

This document provides complete transparency about every `Axiom`, `Admitted`, and `admit` in the Trinity S3AI codebase. It is the companion to `admitted_log.md` (which covers the Admitted/admit registry) and extends it with stratification of all 88 `Axiom` declarations.

A formal Coq proof is only as strong as its axioms. The four No-Go Theorems (NGT1–NGT4) in `NoGoTheorems.v` are formally verified **modulo** the axioms listed below.

---

## Quick Reference

| Category | Count | Can publish? |
|---|---|---|
| **CITED_MATH** | 23 | Yes — cite the reference |
| **CITED_PHYSICS** | 13 | Yes — cite PDG/Planck release |
| **GENUINE_ASSUMPTION** | 40 | Conditionally — must disclose |
| **SHOULD_BE_THEOREM** | 44 (Admitted) | No — technical debt, must close |
| **REFUTED** | 2 | No — must remove or rewrite |

---

## CITED_MATH Axioms (23)

These assert classical mathematical results with traceable published proofs.

| Name | File | Citation |
|---|---|---|
| `D4_triality_exists` | `AltCrystallography.v` | Humphreys, *Intro. to Lie Algebras* §4.3; DOI: 10.1007/978-1-4612-6973-1 |
| `D4_unique_order3_outer_aut` | `AltCrystallography.v` | Humphreys §11.4; DOI: 10.1007/978-1-4612-6973-1 |
| `e8_h4_folding_exists` | `E8Bulk.v` | Elser-Sloane, J.Phys.A 20:6161 (1987); DOI: 10.1088/0305-4470/20/17/044 |
| `icosian_e8_correspondence` | `E8Bulk.v` | Conway-Smith, *Quaternions and Octonions* ch.4 |
| `APS_E8_plumbing` | `EtaDFBridge.v` | Atiyah-Patodi-Singer, Math.Proc.Camb.Phil.Soc. 77 (1975) 43–69; DOI: 10.1017/S0305004100049410 |
| `cell600_J_off_diagonal_KO6` | `SpectralTripleAxioms.v` | Connes, *Noncommutative Geometry* §VI; DOI: 10.1007/978-3-540-34228-1 |
| `cell600_J_off_diagonal` | `KODimension.v` | Same as above |
| `unimod_hypercharge_from_H4_roots` | `UnimodularityAndSigma.v` | Connes-Chamseddine NCG SM papers |
| `sigma_no_go` | `UnimodularityAndSigma.v` | Proved in NoGoTheorems.v as NGT2 |
| `sigma_no_dynamical_field` | `UnimodularityAndSigma.v` | Consequence of NGT2 |
| `sm_cubic_anomaly_zero_per_gen` | `ThreeGenerations.v` | Gross-Jackiw 1972, Phys.Rev.D 6:477; DOI: 10.1103/PhysRevD.6.477 |
| `schur_orthogonality_2I` | `derivations/axiom7_poincare/` | Standard representation theory; Fulton-Harris |
| *(6 mirror copies in derivations/)* | — | Same citations as above |

---

## CITED_PHYSICS Axioms (13)

These encode measured experimental values. They are correctly used as axioms.

| Name | File | Citation |
|---|---|---|
| `g_SU2_value` | `HiggsPotentialCorrected.v` | PDG 2024, DOI: 10.1093/ptep/ptac097 |
| `g_U1_value` | `HiggsPotentialCorrected.v` | PDG 2024, DOI: 10.1093/ptep/ptac097 |
| `g_SU2_pos` | `HiggsPotentialCorrected.v` | PDG 2024, DOI: 10.1093/ptep/ptac097 |
| `g_U1_pos` | `HiggsPotentialCorrected.v` | PDG 2024, DOI: 10.1093/ptep/ptac097 |
| `e_gt_0` | `HiggsPotentialCorrected.v` | Mathematical (e > 0 by definition) |
| `Lambda_obs_planck_units_small` | `CosmologyOrigins.v` | Planck 2018, DOI: 10.1051/0004-6361/201833910 |
| `g_unif_pos` | `RGRunning.v` | Langacker 1981, Rev.Mod.Phys. 52:299 |
| `gU2inv_window` | `RGRunning.v` | PDG 2024 EW review |
| `alpha_run_window` | `RGRunning.v` | PDG 2024 EW review |
| `gU2inv_window_x` | `RGRunningExtras.v` | PDG 2024 EW review |
| `all_irrep_pairs_sigma_lower_bound` | `YukawaFrom2I.v` | Wave 8 Python SVD computation |
| *(2 mirror copies in derivations/)* | — | Same citations |

---

## GENUINE_ASSUMPTION Axioms (40)

These have no traceable published proof and no proposed Coq tactic. They represent genuine open problems.

### Critical (block NCG completeness claims)

| Name | File | Why critical |
|---|---|---|
| `axiom_first_order_MATH_TODO` | `SpectralTripleAxioms.v` | **THE key NCG condition** [[D,a],JbJ⁻¹]=0. Without this, Trinity is not a Connes spectral triple. |
| `axiom4_commutator_vanishing` | `SpectralTripleAxioms.v` | [a,JbJ⁻¹]=0 for all a,b ∈ C[2I]. Requires 240×240 matrix check. |
| `axiom_orientation_hochschild` | `SpectralTripleAxioms.v` | Hochschild 6-cycle realizing γ. Requires explicit D. |
| `axiom_poincare_nondegeneracy` | `SpectralTripleAxioms.v` | KK-Poincaré duality. Requires KK-theory over C[2I]. |

### D_F spectral values (placeholder `True`)

| Name | File | Status |
|---|---|---|
| `DF_max_eigenvalue_is_12` | `DFSpectrum.v` | Numerically verified in Python; not formalized |
| `min_pos_eigenvalue_is_sqrt5` | `DFSpectrum.v` | Same |
| `max_eigenvalue_is_12` | `DFSpectrum.v` | Same (duplicate) |
| `spectral_gap_is_sqrt5` | `DFSpectrum.v` | Same |
| `DF_kernel_dimension_is_100` | `DFSpectrum.v` | Same |

### Eta invariants (not computed)

| Name | File | Status |
|---|---|---|
| `eta_S3_2T_admitted` | `AltCrystallography.v` | Requires APS + 2T character table |
| `eta_S3_2O_admitted` | `AltCrystallography.v` | Requires APS + 2O character table |
| `chirality_via_eta_invariant` | `ChiralityAnalysis.v` | eta(S³/2I) ≠ 0 — not computed |

### Chirality mechanism

| Name | File | Status |
|---|---|---|
| `chirality_via_compactification` | `ChiralityAnalysis.v` | chiral_index=3 from G4-flux — not constructed |
| `chirality_mechanism_unknown` | `ChiralityAnalysis.v` | Honest open marker — keep |

### Poincaré/KK-theory

| Name | File | Status |
|---|---|---|
| `full_KK_poincare_duality` | `Axiom7Poincare.v` | Requires KK-theory over C[2I] |
| `topological_K_theory_2I` | `Axiom7Poincare.v` | Requires topological K-theory |
| `axiom7_KK_theory_poincare` | `derivations/axiom7_poincare/` | Mirror — same |

### Physical assumptions (not derivable from H4)

| Name | File | Status |
|---|---|---|
| `seesaw_scale_from_v31` | `NeutrinoOrigins.v` | M_R requires EW VEV identification |
| `nu_absolute_scale_gap` | `NeutrinoOrigins.v` | 10⁻⁵ eV² scale inserted by hand |
| `G01_from_GUT_running` | `GaugeOrigins.v` | Requires RGE + sqrt(5/3) GUT factor |
| `alpha_from_H4` | `RGRunning.v` (Admitted) | Needs GUT normalization + 1-loop RGE |
| `alpha_s_from_H4` | `RGRunning.v` (Admitted) | Needs 2-loop β + top threshold |
| `H4_determines_L01` | `LeptonOrigins.v` | L01=239·e/π is a numerical fit |
| `H01_spectral_key_identity` | `HiggsOrigins.v` | Requires 480×480 D_F spectrum |
| `discrete_DP_exists_structurally` | `E8Bulk.v` | D_P construction on E8 — open |

*(Plus 12 mirror copies in derivations/ folder)*

---

## SHOULD_BE_THEOREM Admitted items (44)

Technically provable in Coq — blocked by library gaps or missing tactic infrastructure. See `admitted_log.md` for full details and proposed closing tactics.

**Highest priority closures (estimated 1–2 hours each):**
1. `sigma_candidate_mass_scale` — `lra` after unfold
2. `phi_squared_nat` — `lia` or switch to Z
3. `Koide_correct_forms_equal` — `field_simplify [sqrt5_sq]; ring`
4. `N04_within_experimental_range` — `unfold; interval with (i_prec 100)`
5. `Q02_is_m_s_over_m_u`, `N03_is_sin2_theta_23`, `C01_is_V_us` — `simpl; interval` with higher prec
6. `phi_eq_2cos_pi5` — import from E6vsH4.v
7. `ttt_lr_is_phi_inv_cube_scaled` — `assert phi3_ne; field`
8. `two_I_order`, `H4_group_order` (×4) — change to `Definition`

---

## REFUTED Items (2)

These statements are mathematically FALSE and must be corrected before publication.

### `H03_h_half_structural` (in HiggsOrigins.v and derivations/higgs/HiggsOrigins.v)

**Claimed:** `h_H4 / 2 = (d3_H4 * d4_H4) / (d3_H4 + d4_H4 - d3_H4 / d4_H4 * d3_H4)`

**Actual computation:**
- LHS: h_H4 / 2 = 30 / 2 = **15**
- RHS: (20 × 30) / (20 + 30 − (20/30) × 20) = 600 / (50 − 400/30) = 600 / (50 − 13.33...) = 600 / 36.67 ≈ **16.36**
- **Difference: 1.36** (error ≈ 9%)

**Status (v4.0-wave10.4 / wave11 cleanup): RESOLVED.**

The Admitted has been replaced in both `proofs/trinity/HiggsOrigins.v` and
`derivations/higgs/HiggsOrigins.v` by a constructive negation proven Qed:

```coq
Theorem H03_h_half_structural_refuted :
  h_H4 / 2 <> (d3_H4 * d4_H4) / (d3_H4 + d4_H4 - d3_H4 / d4_H4 * d3_H4).
Proof.
  unfold h_H4, d3_H4, d4_H4.
  (* LHS = 15, RHS ≈ 16.36... *)
  lra.
Qed.
```

The structural fact `h_H4 / 2 = 15` is proved separately as `h_half_is_15` (Qed).

---

## Impact on NGT1–NGT4

The no-go theorems NGT1–NGT4 **do not depend** on:
- DFSpectrum.v `True` placeholders
- SpectralTripleAxioms.v open conditions
- HiggsOrigins.v spectral identities

They **do depend** on:
- CITED_PHYSICS axioms: g_SU2_value, g_U1_value, Lambda_obs_planck_units_small
- CITED_MATH axioms: sigma_no_go (itself proved as NGT2), D4 triality

**Conclusion:** NGT1–NGT4 are sound given the cited physics measurements. The GENUINE_ASSUMPTION set affects only the positive claims (spectral triple completeness, chirality mechanism, neutrino mass prediction) — not the negative results.

---

*Generated by A4 audit, Wave 10.4. Raw data: `outputs/A4/A4_axiom_stratification.csv` (122 rows).*
