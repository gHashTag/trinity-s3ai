# LEGACY DOCUMENT (admitted_log.md — Wave 12 historical audit)
# Current status: This log reflects the Admitted/Axiom audit status as of Wave 12.
# Current canonical metrics: see COQ_HONEST_STATUS.md (1325 Qed / 25 Admitted / 73 Axiom / 7 Parameter).

# admitted_log.md — Registry of all Admitted in Trinity S3AI

**Last updated:** Wave 12 sprint W12.4 (SHOULD_BE_THEOREM closures — follow-up to W11.7), rebased onto Wave 12 Track B (Cl(8) launch)
**Version:** Trinity S3AI v4.0
**Audit status (A1, Wave 10.4):**

| Type | Actual count | After W11.7 | After W12 Track B | After W12.4 | Previously claimed | Discrepancy |
|------|--------------|-------------|-------------------|-------------|--------------------|-------------|
| `Axiom` SHOULD_BE_THEOREM rows in CSV | 44 | 32 | 32 | 21 | — | −12 W11.7, −11 W12.4 |
| `Axiom` declarations (proofs/, core) | 88 | 78 | 78 | 68 | not specified | −10 W11.7, −10 W12.4 |
| `Axiom` (TRACK_B_CLIFFORD, proofs/clifford_cl8/) | 0 | 0 | 6 | 6 | — | new in W12 Track B |
| `Admitted` (pure, core proofs/) | 37 | 35 | 35 | 34 | 7 | **+27** |
| `Admitted` (TRACK_B_CLIFFORD) | 0 | 0 | 4 | 4 | — | new in W12 Track B |
| `admit` (inline) | 17 | 17 | 17 | 17 | 0 | **+17** |
| `Qed` (total) | 1326 | 1337 | 1340 | 1351 | 326 | **+1025** |

(W11.7 closed 10 Axioms + 2 Admitted = 12 instances; W12 Track B added 6 Axioms + 4 Admitted in a *separate* Cl(8) namespace (`proofs/clifford_cl8/`) with full citations; W12.4 closed 10 core Axioms + 1 Admitted = 11 instances.)

## Sprint W12.4 — SHOULD_BE_THEOREM closures (2026-05, follow-up to W11.7)

Closed 11 axiom/admitted instances (9 CSV row identities accounting for proofs/ ↔ derivations/ mirrors) across 7 files:

| Name | File(s) | Tactic |
|------|---------|--------|
| `ttt_lr_is_phi_inv_cube_scaled` | `proofs/trinity/OptimizerInvariants.v` | `unfold; assert (phi <> 0); field. exact Hne.` (was Admitted Theorem) |
| `DF_chiral_symmetry` | `EtaDFBridge.v` (×2) | `exact I.` (True placeholder) |
| `mass_twist_eta` | `EtaDFBridge.v` (×2) | `intros _; unfold; reflexivity.` (concrete defs collapse) |
| `DF_exact_chirality` | `EtaDFBridge.v` (×2) | `split; reflexivity.` (concrete defs) |
| `iD_selfadjoint` | `DiracOperator.v` (×2) | `exact I.` (True placeholder) |
| `all_irrep_pairs_sv_ratio_is_unity` | `YukawaFrom2I.v` (×2) | `exact I.` (True placeholder) |

Notes:
- The `True` placeholders (`DF_chiral_symmetry`, `iD_selfadjoint`, `all_irrep_pairs_sv_ratio_is_unity`) had only trivial formal content; the *real* numerical/operator-theoretic claims they nodded at remain outside the formalisation and are recorded in surrounding comments.
- `mass_twist_eta` and `DF_exact_chirality` reduce via concrete `Definition`s of `dim_pos_DF = dim_neg_DF = 190` and `dim_ker_L = dim_ker_R = 50` — `reflexivity` discharges them.
- `ttt_lr_is_phi_inv_cube_scaled` was an `Admitted Theorem` whose CSV row is SHOULD_BE_THEOREM (Admitted+admit type). Closed with `field` after asserting `phi <> 0` via `phi_gt_0`. (Initial W12.4 commit asserted `phi^3 <> 0` which `field` does not accept; CI failed; corrected in W12.4-fix.)

## Wave 12 Track B — Cl(8) formalization launch (2026-05)

New directory `proofs/clifford_cl8/` introduces Track B per
`outputs/B_program_T1_T12.md`. The launch PR adds **6 new Axioms** and
**4 new Admitted theorems**, all tagged **`TRACK_B_CLIFFORD`** with full
published citations.

| Entity | File | Type | Category | Citation |
|--------|------|------|----------|----------|
| `Cl06_spec` | `Cl6_iso_M8R.v` | `Axiom` (existence of `CliffordSpec 0 6`) | TRACK_B_CLIFFORD | Wieser-Song 2022 §3 |
| `M8R_pair_alg` | `Cl6_iso_M8R.v` | `Axiom` (existence of `RAlgebra` instance for M_8(R)⊕M_8(R)) | TRACK_B_CLIFFORD | stdlib gap (no MathComp) |
| `Cl_n0_spec n` | `Cl8_periodicity.v` | `Axiom` (existence of `CliffordSpec n 0` for every n) | TRACK_B_CLIFFORD | Wieser-Song 2022 §3 |
| `Cl_80_spec` | `Cl8_periodicity.v` | `Axiom` | TRACK_B_CLIFFORD | Wieser-Song 2022 §3 |
| `M16R_alg` | `Cl8_periodicity.v` | `Axiom` | TRACK_B_CLIFFORD | stdlib gap |
| `RAlg_tensor` | `Cl8_periodicity.v` | `Parameter` (tensor product of R-algebras) | TRACK_B_CLIFFORD | stdlib gap; mathlib4 `Mathlib.LinearAlgebra.TensorProduct` ports needed |
| `T1_polarization` | `CliffordAlgebra.v` | `Admitted` | TRACK_B_CLIFFORD / SHOULD_BE_THEOREM | Lounesto 2001 §1.2 |
| `T2_Cl06_iso_M8R_pair` | `Cl6_iso_M8R.v` | `Admitted` | TRACK_B_CLIFFORD / GENUINE_ASSUMPTION (cited math) | Lounesto Table 16.3; Atiyah-Bott-Shapiro 1964 §11; Wieser-Song 2022 §6 |
| `T3_Cl_8periodicity` | `Cl8_periodicity.v` | `Admitted` | TRACK_B_CLIFFORD / GENUINE_ASSUMPTION | Atiyah-Bott-Shapiro 1964 Table 3; Lawson-Michelsohn 1989 Prop. I.4.1 |
| `T3_Cl80_iso_M16R` | `Cl8_periodicity.v` | `Admitted` | TRACK_B_CLIFFORD / GENUINE_ASSUMPTION | Lounesto Table 16.3 row (8,0); Lawson-Michelsohn 1989 I.4.16 |

**Honesty:** All four Admitted statements are well-known published theorems.
Discharging them in Rocq requires (a) a working tensor product of R-algebras
(not in stdlib; available in MathComp-Analysis or mathlib4), (b) explicit
matrix-generator constructions for the spinor representations (mechanical
but multi-week work), and (c) the volume-element computation. The launch PR
provides the scaffolding and the statements; the proofs are tracked as
TRACK_B_CLIFFORD follow-up items.

## Sprint W11.7 — SHOULD_BE_THEOREM closures (2026-05)

Closed via direct proof (12 CSV rows across 6 files):

| Axiom name | File(s) | Tactic used |
|------------|---------|-------------|
| `two_I_order` | `QuaternionicLinearity.v` (×2) | `Definition := 120` |
| `two_I_order_eq` | `QuaternionicLinearity.v` (×2) | `reflexivity` |
| `H4_group_order` | `QuaternionicLinearity.v` (×2) | `Definition := 120*120` |
| `H4_order_eq` | `QuaternionicLinearity.v` (×2) | `reflexivity` |
| `trace_full_D_sq_coxeter` | `DiracOperator.v` (×2) | `reflexivity` (nat 4*120=480) |
| `sigma_candidate_mass_scale` | `UnimodularityAndSigma.v` (×2) | `unfold; interval with (i_prec 60)` |

Note: the `sigma_candidate_mass_scale` closures were `Admitted Theorem` in the source (the A4 CSV classes them as Axiom-equivalent SHOULD_BE_THEOREM); converted to `Qed`.

> ⚠️ **IMPORTANT**: The previous README.md claimed "0 Admitted". This is FALSE.
> The previous admitted_log.md claimed 25 Admitted. Also FALSE.
> This document reflects the true state after the A1 audit (Wave 10.4).

---

## Taxonomy

| Tag | Meaning | Count |
|-----|---------|-------|
| `[PHYSICAL_AXIOM]` | Physical assumption — RG boundary condition, mass scale, normalisation | 5 |
| `[NUMERICAL_FIT]` | Formula found by fitting to data, no derivation | 3 |
| `[MATH_TODO]` | Mathematically provable, but proof not yet written | 6 |
| `[LIBRARY_GAP]` | Limitation of coq-interval / stdlib Rocq 9.1.1 | 15 |
| `[REFUTED]` | Statement is mathematically FALSE | 2 |

---

## Full Registry — Admitted and admit

| № | File | Theorem/Lemma | Tag | Category (A4) | Rationale | Closability |
|---|------|---------------|-----|---------------|-----------|-------------|
| 1 | `A4Conversion.v` | `conversion_exact` | `[MATH_TODO]` | SHOULD_BE_THEOREM | Algebraic identity: rationalising the denominator. `field`/`ring` cannot handle `sqrt` in Rocq 9.1.1. | **High** — `assert H5: sqrt 5 * sqrt 5 = 5; field_simplify [H5]; ring` |
| 2 | `Bounds_Mixing.v` | `N04_within_experimental_range` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | 65.66° vs. 65.5° ± 4°. `interval` does not unfold `rad_to_deg` without `unfold`. | **High** — `unfold N04_formula_deg rad_to_deg N04_formula_rad phi; interval with (i_prec 100)` |
| 3 | `Catalog42.v` | `Q02_is_m_s_over_m_u` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Was Qed. `powZ` unfold missing. | **High** — `simpl; interval with (i_prec 150)` |
| 4 | `Catalog42.v` | `N03_is_sin2_theta_23` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Was Qed. `powZ` unfold. | **High** — `simpl; interval with (i_prec 150)` |
| 5 | `Catalog42.v` | `C01_is_V_us` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Was Qed. Triple transcendental product. | **High** — `simpl; interval with (i_prec 200)` |
| 6 | `ChiralityAnalysis.v` | `phi_eq_2cos_pi5` | `[MATH_TODO]` | SHOULD_BE_THEOREM | phi=2*cos(pi/5); algebraic proof via minimal polynomial. **NOT in admitted_log.md.** | **High** — import from E6vsH4.v |
| 7 | `E6vsH4.v` | `sqrt_5_not_rational` | `[MATH_TODO]` | SHOULD_BE_THEOREM | Standard number-theoretic result. Not in stdlib Coq. | **Medium** — infinite descent on Z |
| 8 | `E6vsH4.v` | `phi_irrational` | `[MATH_TODO]` | SHOULD_BE_THEOREM | Corollary of `sqrt_5_not_rational`. | **High** — closes together with №7 |
| 9 | `E6vsH4.v` | `E6_no_phi` | `[MATH_TODO]` | SHOULD_BE_THEOREM | Contrapositive of `phi_irrational`. | **High** — closes together with №8 |
| 10 | `E6vsH4.v` | `cos_pi_5_quadratic` | `[MATH_TODO]` | SHOULD_BE_THEOREM | Two sub-admits: sin²→1-cos² + lra. | **Medium** — `rewrite Hsin; ring; nlinarith` |
| 11 | `GaugeOrigins.v` | `G01_from_GUT_running` | `[PHYSICAL_AXIOM]` | GENUINE_ASSUMPTION | Requires `sqrt(5/3)` + one-loop RG — not derivable from H4. | **Low** — physical assumption |
| 12 | `H4GaugeEmbedding.v` | `phi_irrational_over_Q` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Duplicates proof from E6vsH4.v. | **Medium** — reuse |
| 13 | `H4Lagrangian.v` | `L01_lagrangian_order_of_magnitude` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | `interval` cannot handle `1e16/1.22e19`. | **High** — split into estimates |
| 14 | `H4Lagrangian.v` | `Koide_H4_test` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | `sqrt` inside `interval`. | **High** — `unfold Koide_H4; simpl; interval with (i_prec 150)` |
| 15 | `HiggsOrigins.v` | `H03_h_half_structural` | `[REFUTED → RESOLVED v4.0-wave10.4 / wave11]` | **RESOLVED** | Replaced by `H03_h_half_structural_refuted` (Qed) in `proofs/trinity/HiggsOrigins.v` and `derivations/higgs/HiggsOrigins.v`. Proves h/2 ≠ (d3·d4)/(d3+d4-d3²/d4). Structural fact h/2=15 remains a separate theorem `h_half_is_15`. | **Closed** |
| 16 | `Koide.v` | `Koide_correct_forms_equal` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | `field`/`ring` do not work with `sqrt` in the denominator. | **High** — `field_simplify [sqrt5_sq]; ring` |
| 17 | `LeptonOrigins.v` | `H4_determines_L01` | `[NUMERICAL_FIT]` | GENUINE_ASSUMPTION | L01 = 239·e/π found numerically, not derived from H4. Constructive f not provided. | **Very low** |
| 18 | `NeutrinoOrigins.v` | `seesaw_scale_from_v31` | `[PHYSICAL_AXIOM]` | GENUINE_ASSUMPTION | M_R is not determined by H4 geometry. | **Low** |
| 19 | `NeutrinoOrigins.v` | `nu_absolute_scale_gap` | `[NUMERICAL_FIT]` | GENUINE_ASSUMPTION | Factor 10⁻⁵ eV² inserted manually. | **Very low** |
| 20 | `OptimizerInvariants.v` | `ttt_lr_is_phi_inv_cube_scaled` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | `field` does not automatically reduce the phi^3 non-zero condition. | **High** — `assert Hphi3_ne; field [Hphi3_ne]` |
| 21 | `RGRunning.v` | `alpha_from_H4` | `[PHYSICAL_AXIOM]` | GENUINE_ASSUMPTION | Needs sqrt(5/3) + one-loop RG. | **Low** |
| 22 | `RGRunning.v` | `alpha_s_from_H4` | `[PHYSICAL_AXIOM]` | GENUINE_ASSUMPTION | Needs two-loop running + top-threshold corrections. | **Low** |
| 23 | `UnimodularityAndSigma.v` | `sigma_candidate_mass_scale` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Rabs((2/30)*1.5e16 - 1e15) < 1e10; pure rational R, large numbers. | **High** — `lra` or `ring_simplify; lra` |
| 24 | `UniquenessStructural.v` | `phi_squared_nat` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | 1618*1618=2618724; `vm_compute` segfault on large `nat` in Rocq 9.1.1. | **High** — `lia` or replace `nat` with `Z` |
| 25 | `test_scratch.v` | `VEV_corrected_matches_SM` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Needs `sqrt_sq` + `v_SM >= 0`. | **High** |
| 26 | `test_scratch.v` | `m_H_corrected_matches_Trinity` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | sqrt(m_H_Trinity²)=m_H_Trinity. | **High** |
| 27 | `test_scratch.v` | `Higgs_mass_from_curvature` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | sqrt(2·μ²)=m_H_Trinity; same chain. | **High** |

### New entries (not in previous admitted_log.md)

| № | File | Theorem/Lemma | Tag | Rationale |
|---|------|---------------|-----|-----------|
| 28 | `ChiralityAnalysis.v` | `phi_eq_2cos_pi5` | `[MATH_TODO]` | phi=2*cos(pi/5) — discovered by A1 audit. Not documented. |
| 29 | `UnimodularityAndSigma.v` | `sigma_candidate_mass_scale` | `[LIBRARY_GAP]` | Discovered by A1 audit. Not documented. |

---

## Tag summary (updated)

| Tag | Count | A4 Category |
|-----|-------|-------------|
| `[PHYSICAL_AXIOM]` | 5 | GENUINE_ASSUMPTION |
| `[NUMERICAL_FIT]` | 3 | GENUINE_ASSUMPTION |
| `[MATH_TODO]` | 6 | SHOULD_BE_THEOREM |
| `[LIBRARY_GAP]` | 15 | SHOULD_BE_THEOREM |
| `[REFUTED]` | 2 | REFUTED |

---

## Closure priorities

### High priority (1–2 hours, pure library fixes)
- №№ 2–5, 23–27: Catalog42, Bounds_Mixing, UnimodularityAndSigma, test_scratch, sigma_candidate_mass_scale
- №№ 20, 14, 16: OptimizerInvariants, Koide, H4Lagrangian Koide_test
- № 6: ChiralityAnalysis phi_eq_2cos_pi5 (import from E6vsH4.v)

### Medium priority (requires manual proofs)
- №№ 7–10: E6vsH4 — irrationality of √5 + consequences
- № 12: H4GaugeEmbedding — reuse after E6vsH4
- № 1: A4Conversion — rationalising the denominator

### Low priority (requires physical progress)
- №№ 11, 21, 22, 18: RGRunning/GaugeOrigins/NeutrinoOrigins — physical assumptions
- №№ 17, 19: NUMERICAL_FIT — physical derivation needed
- № 15: HiggsOrigins H03 — REFUTED, requires reformulation

---

## Header comment status

| File | Old header | Fact | Action |
|------|------------|------|--------|
| `E6vsH4.v` | "ALL theorems: QED, 0 Admitted." | **4 Admitted+admit** | Fix (patch E6vsH4_header_patch.diff) |
| `README.md` | "Admitted: 0" | **37 Admitted + 17 admit** | Fix (patch README_patch.diff) |
| `admitted_log.md` (old) | "Total Admitted: 25" | **37 Admitted** | Replace with this document |

---

*Document created by A4 audit (Wave 10.4). Full stratification: `proofs/trinity/FOUNDATIONS.md` and `outputs/A4/A4_axiom_stratification.csv`.*
