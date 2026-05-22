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
