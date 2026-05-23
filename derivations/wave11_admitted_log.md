# Wave 11 Admitted Closure Log

| File | Theorem | Result | Notes |
|------|---------|--------|-------|
| UniquenessStructural.v | invariant_720_refuted | **CLOSED** | Converted false lemma to refutation; proved with `simpl` + `discriminate` |
| UniquenessStructural.v | invariant_120_refuted | **CLOSED** | Converted false lemma to refutation; proved with `simpl` + `discriminate` |
| UniquenessStructural.v | phi_squared_nat_refuted | REMAINS ADMITTED | Theorem is false (1618*1618=2617924≠2618724), but Rocq 9.1.1's `Nat.of_num_uint` representation prevents `vm_compute`/`lia`/`discriminate` from terminating on large nat literals. Refutation left Admitted with detailed comment. |
| RGRunning.v | alpha_i_inv_pos_at_mZ | REMAINS ADMITTED | File imports `Interval.Tactic`. Inconsistent coq-interval installation (compiled with different Coq version) prevents any compilation. Cannot verify proof changes. |
| RGRunning.v | alpha_from_H4 | REMAINS ADMITTED | Same interval obstruction. Numerical bound involving free parameter `g_unif`. |
| RGRunning.v | alpha_s_from_H4 | REMAINS ADMITTED | Same interval obstruction. Numerical bound involving free parameter `g_unif`. |
| A4Conversion.v | conversion_exact | REMAINS ADMITTED | File imports `Interval.Tactic`. Verified a purely algebraic proof in isolation (field_simplify + Rsqr_sqrt + lra), but cannot be injected without breaking compilation due to interval dependency. |
| Bounds_Mixing.v | N04_within_experimental_range | REMAINS ADMITTED | File imports `Interval.Tactic`. Numerical bound requiring interval or explicit sqrt bounds. |
| Catalog42.v | Q02_is_m_s_over_m_u | REMAINS ADMITTED | File imports `Interval.Tactic`. Numerical bound. |
| Catalog42.v | N03_is_sin2_theta_23 | REMAINS ADMITTED | File imports `Interval.Tactic`. Numerical bound. |
| Catalog42.v | C01_is_V_us | REMAINS ADMITTED | File imports `Interval.Tactic`. Numerical bound. |
| E6vsH4.v | sqrt_5_not_rational | REMAINS ADMITTED | File imports `Interval.Tactic`. Requires number-theory library for irrationality proof. |
| E6vsH4.v | phi_irrational | REMAINS ADMITTED | File imports `Interval.Tactic`. Depends on sqrt_5_not_rational. |
| E6vsH4.v | E6_no_phi | REMAINS ADMITTED | File imports `Interval.Tactic`. Depends on phi_irrational. |
| E6vsH4.v | cos_pi_5_quadratic | REMAINS ADMITTED | File imports `Interval.Tactic`. Trigonometric identity potentially provable with standard Coq Reals, but file cannot compile to verify. |
| H4GaugeEmbedding.v | phi_irrational_over_Q | REMAINS ADMITTED | File imports `Interval.Tactic`. Requires number-theory library for irrationality proof. |
| H4Lagrangian.v | L01_lagrangian_order_of_magnitude | REMAINS ADMITTED | File imports `Interval.Tactic`. Numerical bound. |
| H4Lagrangian.v | Koide_H4_test | REMAINS ADMITTED | File imports `Interval.Tactic`. Numerical bound. |
| Koide.v | Koide_correct_forms_equal | REMAINS ADMITTED | File imports `Interval.Tactic`. Verified algebraic proof in isolation (sqrt_one_div + field), but cannot inject without breaking compilation. |
| OptimizerInvariants.v | ttt_lr_is_phi_inv_cube_scaled | REMAINS ADMITTED | File imports `Interval.Tactic`. Verified algebraic proof in isolation (unfold Rdiv + rewrite Rmult_1_l + reflexivity), but cannot inject without breaking compilation. |

## Summary

- **Files modified**: 1 (`UniquenessStructural.v`)
- **Admitted closed**: 2 (both in `UniquenessStructural.v`)
- **Admitted remaining**: 18 across 9 files
- **Primary obstruction**: Inconsistent/broken `coq-interval` installation prevents compilation of all files that import `Interval.Tactic`. Without compilation, proof changes cannot be verified per instructions.
- **Secondary obstruction**: Rocq 9.1.1's `Nat.of_num_uint` representation prevents computation on large nat literals (affecting `phi_squared_nat_refuted`).

# Wave 12.2 Admitted Closure Log

| File | Theorem | Result | Notes |
|------|---------|--------|-------|
| OptimizerInvariants.v | ttt_lr_is_phi_inv_cube_scaled | **CLOSED** | Pure algebraic identity; proved with `unfold Rdiv; rewrite Rmult_1_l; reflexivity`. |
| Bounds_Mixing.v | N04_within_experimental_range | **CLOSED** | Numerical bound; proved with `unfold` + `interval with (i_prec 60)`. |
| A4Conversion.v | conversion_exact | **CLOSED** | Algebraic identity with sqrt(5); proved by clearing denominators (`Rmult_eq_reg_r`) + `field_simplify` + `ring_simplify` + `pow2_sqrt`. |
| H4Lagrangian.v | L01_lagrangian_order_of_magnitude | **CLOSED** | Numerical bound; proved with `unfold` + `interval with (i_prec 100)`. |
| H4Lagrangian.v | Koide_H4_test | **CLOSED** | Numerical bound with nested sqrt; proved with `unfold Koide_H4` + `interval with (i_prec 100)`. |
| Koide.v | Koide_correct_forms_equal | **CLOSED** | Algebraic identity; proved with `unfold` + `repeat rewrite Rdiv_1_l` + `repeat rewrite sqrt_inv` + `reflexivity`. |
| Catalog42.v | Q02_is_m_s_over_m_u | **REFUTED** | Theorem is mathematically false (relative error ~0.138% > V_bound 0.1%). Converted to `Q02_is_m_s_over_m_u_refuted` and proved with `interval` + `lra`. |
| Catalog42.v | N03_is_sin2_theta_23 | **REFUTED** | Theorem is mathematically false (relative error ~0.42% > V_bound 0.1%). Converted to `N03_is_sin2_theta_23_refuted` and proved with `interval` + `lra`. |
| Catalog42.v | C01_is_V_us | **REFUTED** | Theorem is mathematically false (relative error ~0.96% > V_bound 0.1%). Converted to `C01_is_V_us_refuted` and proved with `interval` + `lra`. |
| RGRunning.v | alpha_from_H4 | REMAINS ADMITTED | Mathematically false under current definitions (refutation exists in `RGRunningExtras.v` as `alpha_from_H4_refuted`). Left Admitted with existing honest documentation. |
| RGRunning.v | alpha_s_from_H4 | REMAINS ADMITTED | Mathematically false under current definitions. Left Admitted with existing honest documentation. |

## Summary

- **Files modified**: 6 (`OptimizerInvariants.v`, `Bounds_Mixing.v`, `A4Conversion.v`, `H4Lagrangian.v`, `Koide.v`, `Catalog42.v`)
- **Admitted closed**: 6 (all provable)
- **Admitted converted to refutations**: 3 (Q02, N03, C01 in `Catalog42.v` — all mathematically false)
- **Admitted remaining**: 13 across 8 files (including 2 documented false theorems in `RGRunning.v`)
- **Final project compile status**: exit code 0 (full project compiles)
- **coq-interval**: Installed and functional (version 4.11.4) in `coq-8.20` switch.

