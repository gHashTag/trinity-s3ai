# Wave 10.6: Attempts to Close Admitted (Goedel-Prover / Manual Tactics)

## Status: ATTEMPTS, nothing applied to main

Wave 10.6 did not have access to a real ML prover Goedel-Prover-V2. All attempts were made by the Sonnet subagent through manual Coq tactics (`lia`, `lra`, `nra`, `field`, `interval`, `nlinarith`, infinite descent).

## Current Number of Admitted

27 Admitted in the repository (unchanged after Wave 10.6).

| Tag | Count | Commented |
|---|---|---|
| LIBRARY_GAP | 13 | Not closed — needs a full library (Mathcomp / coq-interval extras) |
| MATH_TODO | ~6 | Not closed — requires KK-theory, η-convergence, discrete D_P |
| PHYSICAL_AXIOM | 4 | NOT closed on principle (external inputs) |
| NUMERICAL_FIT | ~2 | Not closed — interval tactic gave overflow in coefficients |

## Which Tactics Worked in /tmp/ (but require additional work for integration)

| # | File | Theorem | Tactic | Status |
|---|---|---|---|---|
| 1 | OptimizerInvariants.v | `ttt_lr_is_phi_inv_cube_scaled` | `field. apply Rgt_not_eq. apply phi_gt_0.` | works in /tmp, not applied |
| 2 | A4Conversion.v | `conversion_exact` | cross-mul + `nlinarith [Hs]` | partially — needs helper `div_eq` |
| 3 | E6vsH4.v | `phi_irrational` | infinite descent (~50 lines) | works locally |
| 4 | Bounds_Mixing.v | `N04_within_experimental_range` | `interval with (i_prec 100)` | works locally |
| 5 | Catalog42.v | `Q02_is_m_s_over_m_u` | `interval with (i_prec 150)` | works locally |
| 6 | H4Lagrangian.v | `L01_lagrangian_order_of_magnitude` | `interval` | works locally |
| 7 | Koide.v | `Koide_correct_forms_equal` | `sqrt_1_div_eq + reflexivity` | works locally |
| 8 | test_scratch.v | (3 theorems) | `sqrt_sq + field` | works locally |

**Potential for closure: 8 Admitted → 27 → 19** (if carefully ported with full project compilation).

## Mathematical Errors Found (DO NOT close — theorems are false)

| # | File | Theorem | Real Error | Action |
|---|---|---|---|---|
| 22 | (various) | `phi_squared_nat` | 1618² = 2 617 924, not 2 618 724 | delete or Refute |
| 4 | (Bounds_Mixing) | `N03_is_sin2_theta_23` | 0.42% > V_bound 0.1% | replace with refutation |
| 5 | (Catalog42) | `C01_is_V_us` | 0.96% > V_bound 0.1% | replace with refutation |

## Wave 11 Strategy

1. Apply 8 working tactics from the table above — should close LIBRARY_GAP from 13 to ~5
2. Convert 3 found false theorems into `Theorem X_refuted` (as `alpha_from_H4_refuted` in Wave 3)
3. Real Goedel-Prover-V2 / lean-proverbot when available out of the box

## Honestly

Without an ML prover or substantially longer attempts (several hours per Admitted), 13 LIBRARY_GAP will remain open. This is not a blocker for scientific publication — all Admitted are honestly tagged.
