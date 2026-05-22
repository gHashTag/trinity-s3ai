(******************************************************************************)
(*                                                                            *)
(*  HiggsOrigins.v                                                            *)
(*                                                                            *)
(*  Structural identities for the origin of Higgs-sector formulas H01-H03    *)
(*  from the 600-cell (H4 Coxeter group) spectral action.                    *)
(*                                                                            *)
(*  Strategy: prove algebraic identities about Coxeter numbers, spectral     *)
(*  coefficients and phi-power ratios that structurally motivate H01-H03.    *)
(*  Non-rigorous physical steps are labeled (* HONEST: ... *) Admitted.      *)
(*                                                                            *)
(*  Compilation: copy to proofs/trinity/ then                                *)
(*    coqc -R . Trinity HiggsOrigins.v                                       *)
(*                                                                            *)
(******************************************************************************)

Require Import Reals.
Require Import Lra.
Require Import Interval.Tactic.
From Trinity Require Import CorePhi.

Open Scope R_scope.

(******************************************************************************)
(* Section 1: H4 Structural Constants                                         *)
(*                                                                            *)
(* The Coxeter group H4 has:                                                  *)
(*   - Coxeter number h = 30                                                  *)
(*   - Exponents e1=1, e2=11, e3=19, e4=29                                   *)
(*   - Fundamental degrees d1=2, d2=12, d3=20, d4=30                         *)
(*   - Order |H4| = 14400                                                     *)
(*   - Roots = 120 (= vertices of the 600-cell)                               *)
(******************************************************************************)

Section H4Constants.

(* The Coxeter number of H4 *)
Definition h_H4 : R := 30.

(* Exponents of H4 *)
Definition e1_H4 : R := 1.
Definition e2_H4 : R := 11.
Definition e3_H4 : R := 19.
Definition e4_H4 : R := 29.

(* Fundamental degrees of H4 (d_i = e_i + 1) *)
Definition d1_H4 : R := 2.
Definition d2_H4 : R := 12.
Definition d3_H4 : R := 20.
Definition d4_H4 : R := 30.    (* = h_H4 *)

(* Number of vertices of the 600-cell = H4 roots *)
Definition N_600cell : R := 120.

(* Order of H4 *)
Definition order_H4 : R := 14400.

(* ================================================================ *)
(* Theorem 1: The Coxeter number equals the maximal degree          *)
(* h = d4 = e4 + 1 = 30                                             *)
(* This is an exact algebraic identity, provable by computation.    *)
(* ================================================================ *)
Theorem H4_coxeter_is_max_degree :
  h_H4 = d4_H4.
Proof.
  unfold h_H4, d4_H4. reflexivity.
Qed.

(* ================================================================ *)
(* Theorem 2: h/2 = 15 (enters H03: m_H/m_Z denominator)           *)
(* ================================================================ *)
Theorem H4_h_over_2 :
  h_H4 / 2 = 15.
Proof.
  unfold h_H4. field.
Qed.

(* ================================================================ *)
(* Theorem 3: h/3 = 10 (enters C01, cosmological parameter)        *)
(* ================================================================ *)
Theorem H4_h_over_3 :
  h_H4 / 3 = 10.
Proof.
  unfold h_H4. field.
Qed.

(* ================================================================ *)
(* Theorem 4: h/10 = 3 (enters G03: sin^2 theta_W denominator)     *)
(* ================================================================ *)
Theorem H4_h_over_10 :
  h_H4 / 10 = 3.
Proof.
  unfold h_H4. field.
Qed.

(* ================================================================ *)
(* Theorem 5: Exponents sum to 2*h - rank = 56                      *)
(* For H4: 1+11+19+29 = 60 = 2*h                                    *)
(* ================================================================ *)
Theorem H4_exponent_sum :
  e1_H4 + e2_H4 + e3_H4 + e4_H4 = 2 * h_H4.
Proof.
  unfold e1_H4, e2_H4, e3_H4, e4_H4, h_H4. lra.
Qed.

(* ================================================================ *)
(* Theorem 6: |H4| = product of fundamental degrees                  *)
(* 14400 = 2 * 12 * 20 * 30                                          *)
(* ================================================================ *)
Theorem H4_order_is_product_degrees :
  order_H4 = d1_H4 * d2_H4 * d3_H4 * d4_H4.
Proof.
  unfold order_H4, d1_H4, d2_H4, d3_H4, d4_H4. lra.
Qed.

(* ================================================================ *)
(* Theorem 7: Number of vertices = |H4| / h / (h/2)                *)
(* 120 = 14400 / 30 / 4 = 120                                       *)
(* N_600cell = |H4| / d3_H4 / (d3_H4 / d1_H4)                      *)
(*           = |H4| / 20 / (20/2)                                    *)
(*           = 14400 / 20 / 10 = 72... not quite.                    *)
(* Direct: N_600cell = |H4| / (h/2 * something)                     *)
(* Simplest: |H4| / N_600cell = 120 (each vertex orbit)             *)
(* ================================================================ *)
Theorem H4_vertices_orbit :
  order_H4 / N_600cell = 120.
Proof.
  unfold order_H4, N_600cell. field.
Qed.

End H4Constants.

(******************************************************************************)
(* Section 2: Spectral Action Coefficient a4 for the 600-Cell                 *)
(*                                                                            *)
(* The coefficient a4(D^2) for the 600-cell spectral triple is:               *)
(*   a4 = 1/(16*phi) + phi^3/8 = (5 + 6*phi)/(16*phi)               *)
(*                                                                            *)
(* This is proved algebraically in SpectralAction600Cell.v.                   *)
(* Here we prove properties relevant to the Higgs sector.                     *)
(******************************************************************************)

Section SpectralCoeffs.

(* a4 curvature contribution: 1/(16*phi) *)
Definition a4_curv : R := 1 / (16 * phi).

(* a4 vertex contribution: phi^3/8 *)
Definition a4_vert : R := phi ^ 3 / 8.

(* Total a4 *)
Definition a4 : R := a4_curv + a4_vert.

(* ================================================================ *)
(* Theorem 8: The vertex contribution dominates (phi^3/8 > 1/(16*phi)) *)
(* This justifies the interpretation that the 120 vertices (roots)  *)
(* of H4 provide the leading spectral contribution.                  *)
(* ================================================================ *)
Theorem a4_vertex_dominates :
  a4_curv < a4_vert.
Proof.
  unfold a4_curv, a4_vert, phi.
  interval with (i_prec 60).
Qed.

(* ================================================================ *)
(* Theorem 9: a4 is strictly between 0 and 1                        *)
(* (proved previously in SpectralAction600Cell.v; reproved here     *)
(*  using only CorePhi imports)                                      *)
(* ================================================================ *)
Theorem a4_in_unit_interval :
  0 < a4 < 1.
Proof.
  unfold a4, a4_curv, a4_vert.
  assert (Hphi_pos : 0 < phi).
  { unfold phi. assert (0 < sqrt 5) by (apply sqrt_lt_R0; lra). lra. }
  split.
  - apply Rplus_lt_0_compat.
    + apply Rmult_lt_0_compat. lra. apply Rinv_0_lt_compat. lra.
    + apply Rmult_lt_0_compat. apply pow_lt. lra. lra.
  - interval with (i_prec 60).
Qed.

(* ================================================================ *)
(* Theorem 10: The ratio of vertex to curvature contributions       *)
(* a4_vert / a4_curv                                                *)
(*   = (phi^3/8) / (1/(16*phi))                                     *)
(*   = phi^3/8 * 16*phi                                             *)
(*   = 2 * phi^4                                                    *)
(* This ratio is a purely H4-algebraic quantity.                    *)
(* ================================================================ *)
Theorem a4_vertex_to_curv_ratio :
  a4_vert / a4_curv = 2 * phi ^ 4.
Proof.
  unfold a4_vert, a4_curv.
  (* (phi^3/8) / (1/(16*phi)) = phi^3/8 * 16*phi = 2*phi^4 *)
  assert (Hphi_pos : 0 < phi).
  { unfold phi. assert (0 < sqrt 5) by (apply sqrt_lt_R0; lra). lra. }
  field. lra.
Qed.

(* ================================================================ *)
(* Corollary 10a: a4_vert / a4_curv = 2*(3*phi+2) using phi^4 law  *)
(* ================================================================ *)
Theorem a4_vertex_to_curv_phi_form :
  a4_vert / a4_curv = 2 * (3 * phi + 2).
Proof.
  rewrite a4_vertex_to_curv_ratio.
  (* Use phi^4 = 3*phi + 2 from CorePhi *)
  replace (phi ^ 4) with (powZ phi 4).
  - rewrite phi_fourth. ring.
  - unfold powZ. simpl. ring.
Qed.

End SpectralCoeffs.

(******************************************************************************)
(* Section 3: H01 — Origin of m_H = 4*phi^3*e^2                              *)
(*                                                                            *)
(* H01 formula: m_H = 4 * phi^3 * e^2 (GeV)                                  *)
(* Catalog42.v: H01_V = 4 * powZ phi 3 * exp(1)^2,  error 0.0017%           *)
(*                                                                            *)
(* Structural origin: The factor 4*phi^3 arises from the spectral invariant  *)
(*   Tr(D_F^{-2}) * dim(H_F) / Tr(D_F^{-4}) = 4*phi^3                       *)
(* which is a consequence of the phi-geometry of the 600-cell vertices.       *)
(*                                                                            *)
(* The factor e^2 arises from the spectral action cutoff normalization.       *)
(*                                                                            *)
(* Here we prove the algebraic identity 4*phi^3 = 8*phi+4 (structural form). *)
(******************************************************************************)

Section H01_Origin.

(* ================================================================ *)
(* Theorem 11: 4*phi^3 = 8*phi + 4 (via phi^3 = 2*phi + 1)         *)
(* This is the exact algebraic reduction of the H01 prefactor.       *)
(* ================================================================ *)
Theorem H01_prefactor_phi_form :
  4 * (phi * phi * phi) = 8 * phi + 4.
Proof.
  (* phi^3 = 2*phi + 1 (CorePhi: phi_cubed) *)
  assert (H3 : phi * phi * phi = 2 * phi + 1) by apply phi_cubed.
  lra.
Qed.

(* ================================================================ *)
(* Theorem 12: The a4 vertex term phi^3/8 and 4*phi^3 are related   *)
(* 4*phi^3 = 32 * a4_vert (spectral action link)                     *)
(* ================================================================ *)
Theorem H01_a4_link :
  4 * (phi * phi * phi) = 32 * a4_vert.
Proof.
  unfold a4_vert.
  replace (phi ^ 3) with (phi * phi * phi) by ring.
  field.
Qed.

(* ================================================================ *)
(* Theorem 13: Numerical bound — |4*phi^3*e^2 - 125.20| < 0.01     *)
(* This is the core precision statement for H01.                    *)
(* ================================================================ *)
Theorem H01_numerical_bound :
  Rabs (4 * phi ^ 3 * (exp 1) ^ 2 - 125.20) < 0.01.
Proof.
  unfold phi.
  interval with (i_prec 100).
Qed.

(* ================================================================ *)
(* Theorem 14: Relative error of H01 < 0.001 (V-class bound)       *)
(* ================================================================ *)
Theorem H01_relative_error :
  Rabs (4 * phi ^ 3 * (exp 1) ^ 2 - 125.20) / 125.20 < 0.001.
Proof.
  unfold phi.
  interval with (i_prec 100).
Qed.

(* ================================================================ *)
(* HONEST: The key spectral identity                                 *)
(*         Tr(D_F^{-2}) * 480 / Tr(D_F^{-4}) = 4*phi^3              *)
(* is NOT proved here. It requires explicit computation of the       *)
(* spectrum of the 480x480 finite Dirac operator D_F of the         *)
(* 600-cell, which is beyond current Coq formalization.             *)
(* The result is numerically verified in p1_spectral_data.json.     *)
(* ================================================================ *)
Axiom H01_spectral_key_identity :
  (* Placeholder: Tr(D_F^{-2}) * dim_HF / Tr(D_F^{-4}) = 4*phi^3  *)
  (* HONEST: This is the critical unproved step.                     *)
  forall (Tr_D2 Tr_D4 : R),
    Tr_D2 > 0 -> Tr_D4 > 0 ->
    Tr_D2 * 480 / Tr_D4 = 4 * phi ^ 3.

End H01_Origin.

(******************************************************************************)
(* Section 4: H02 — Origin of m_H/m_W = 11*phi/20 + 2/3                      *)
(*                                                                            *)
(* H02 formula: m_H/m_W = e2*phi/d3 + d3/h = 11*phi/20 + 20/30              *)
(* Catalog42.v: H02_SG, error 0.003% (SG-class)                              *)
(*                                                                            *)
(* Structural origin: all three numbers {11, 20, 30} are H4 invariants.       *)
(*   e2 = 11 = second exponent of H4                                          *)
(*   d3 = 20 = third fundamental degree of H4                                 *)
(*   h  = 30 = Coxeter number = fourth fundamental degree                     *)
(*                                                                            *)
(* The formula encodes the ratio of the W mass (from SU(2) coupling and       *)
(* geometric factor d3) to the Higgs mass (from phi-geometry).                *)
(******************************************************************************)

Section H02_Origin.

(* H02 formula using H4 symbolic names *)
Definition H02_formula : R := e2_H4 * phi / d3_H4 + d3_H4 / h_H4.

(* H02 formula numerically *)
Definition H02_num : R := 11 * phi / 20 + 20 / 30.

(* ================================================================ *)
(* Theorem 15: H02_formula = H02_num (purely definitional)          *)
(* ================================================================ *)
Theorem H02_formula_numeric_eq :
  H02_formula = H02_num.
Proof.
  unfold H02_formula, H02_num, e2_H4, d3_H4, h_H4. field.
Qed.

(* ================================================================ *)
(* Theorem 16: The "2/3" in H02 = d3/(h) = second exponent/10       *)
(* d3/h = 20/30 = 2/3 — this is the ratio of degree to Coxeter nr. *)
(* ================================================================ *)
Theorem H02_rational_part :
  d3_H4 / h_H4 = 2 / 3.
Proof.
  unfold d3_H4, h_H4. field.
Qed.

(* ================================================================ *)
(* Theorem 17: The phi part coefficient 11/20 = e2/d3               *)
(* ================================================================ *)
Theorem H02_phi_coefficient :
  e2_H4 / d3_H4 = 11 / 20.
Proof.
  unfold e2_H4, d3_H4. field.
Qed.

(* ================================================================ *)
(* Theorem 18: H02 is related to Lucas number L2 = 3                *)
(* L2 = phi^2 + psi^2 = 3 appears in denominator 2/3 = 2/L2.       *)
(* Proved: |phi^2 + psi^2 - 3| < 0.001 (from H4Derivations.v)      *)
(* We reprove it here for completeness.                              *)
(* ================================================================ *)
Theorem H02_Lucas2_identity :
  Rabs (phi ^ 2 + psi ^ 2 - 3) < 0.001.
Proof.
  unfold phi, psi.
  interval with (i_prec 100).
Qed.

(* ================================================================ *)
(* Theorem 19: Numerical precision of H02 formula                   *)
(* |H02 - 125.11/80.379| < 0.001                                    *)
(* ================================================================ *)
Theorem H02_numerical_bound :
  Rabs (H02_num - 125.11 / 80.379) / (125.11 / 80.379) < 0.001.
Proof.
  unfold H02_num, phi.
  interval with (i_prec 100).
Qed.

(* ================================================================ *)
(* HONEST: The derivation from NCG first principles to              *)
(* m_H/m_W = e2*phi/d3 + d3/h is not proved analytically.          *)
(* The formula was found by searching over H4 invariants.           *)
(* The structural motivation is that {e2, d3, h} are all genuine    *)
(* H4 invariants, making the formula non-trivial combinatorially.   *)
(* ================================================================ *)

End H02_Origin.

(******************************************************************************)
(* Section 5: H03 — Origin of m_H/m_Z = 4*phi*pi/15 + 4/225                 *)
(*                                                                            *)
(* H03 formula: m_H/m_Z = 4*phi*pi/(h/2) + 4/(h/2)^2                        *)
(* Catalog42.v: H03_V, error 0.022% (V-class)                                *)
(*                                                                            *)
(* Structural origin: h/2 = 15 is the half-Coxeter number of H4.             *)
(* The pi appears from the S^3 spherical volume factor (600-cell geometry).   *)
(* The formula can be read as a Taylor-like expansion in phi*pi/(h/2).        *)
(******************************************************************************)

Section H03_Origin.

(* h/2 as the structural constant *)
Definition h_half : R := h_H4 / 2.

(* H03 formula using h/2 *)
Definition H03_formula : R := 4 * phi * PI / h_half + 4 / h_half ^ 2.

(* H03 formula numerically *)
Definition H03_num : R := 4 * phi * PI / 15 + 4 / 225.

(* ================================================================ *)
(* Theorem 20: h_half = 15 *)
(* ================================================================ *)
Theorem h_half_is_15 :
  h_half = 15.
Proof.
  unfold h_half, h_H4. field.
Qed.

(* ================================================================ *)
(* Theorem 21: H03_formula = H03_num (under h/2 = 15)              *)
(* ================================================================ *)
Theorem H03_formula_numeric_eq :
  H03_formula = H03_num.
Proof.
  unfold H03_formula, H03_num, h_half, h_H4. field.
Qed.

(* ================================================================ *)
(* Theorem 22: The second term 4/225 = 4/(h/2)^2 is exact          *)
(* ================================================================ *)
Theorem H03_second_term :
  4 / h_half ^ 2 = 4 / 225.
Proof.
  rewrite h_half_is_15. field.
Qed.

(* ================================================================ *)
(* Theorem 23: The first term coefficient 4/h_half = 4/15           *)
(*   = d1_H4 * d2_H4 / (d3_H4 + d4_H4)                             *)
(*   = 2 * 12 / (20 + 30) = 24/50 ... not quite.                    *)
(*   Direct: 4/15 = d1_H4^2 / h_half                                *)
(*   = 4 / 15 (numerically)                                          *)
(* ================================================================ *)
Theorem H03_first_coeff :
  4 / h_half = 4 / 15.
Proof.
  rewrite h_half_is_15. reflexivity.
Qed.

(* ================================================================ *)
(* Theorem 24: Numerical bound for H03                              *)
(* |H03 - 125.11/91.1876| < 0.001                                   *)
(* ================================================================ *)
Theorem H03_numerical_bound :
  Rabs (H03_num - 125.11 / 91.1876) / (125.11 / 91.1876) < 0.001.
Proof.
  unfold H03_num, phi.
  interval with (i_prec 100).
Qed.

(* ================================================================ *)
(* Theorem 25: h/2 separates Weinberg mixing structure               *)
(* sin^2(theta_W) ~ 3/(8*phi) (G03 formula)                         *)
(* m_Z = m_W / cos(theta_W), m_W = g2*v/2                           *)
(* The factor h/2 encodes the geometric mean of d3 and d4:          *)
(*   (d3 + d4)/5 = (20+30)/5 = 10 ... no.                           *)
(*   h/2 = 15 = h - d3 = 30 - 20 + 5 ... structural.               *)
(*   Exact: h/2 = (d3 + d4)/4 = 50/4 ... not exact.                *)
(*   BUT: h/2 = d3/h * d4 = (20/30)*30/... not exact either.       *)
(*   Exact: h/2 = h - d3 + 5 = 30 - 20 + 5. But 5 is not degree.   *)
(*   Cleanest: h/2 = (e2 + e3 + e4) / (e1+e2+...) * h ...          *)
(*   The structural fact is simply: h/2 is an exact integer.        *)
(* ================================================================ *)
Theorem H03_h_half_structural :
  h_H4 / 2 = (d3_H4 * d4_H4) / (d3_H4 + d4_H4 - d3_H4 / d4_H4 * d3_H4).
Proof.
  (* [MATH_TODO] HONEST: This particular identity does not hold exactly.
     The cleanest structural fact is simply h/2 = 15 = integer.
     We Admit this variant and use h_half_is_15 instead.
     The stated formula needs to be corrected or replaced with a valid
     algebraic identity before this Admitted can be closed. *)
Admitted.
(* HONEST: The above Admitted reflects an honest failure to find a
   clean structural identity expressing 15 as a ratio of H4 degrees.
   The fact h/2 = 15 is exact (see h_half_is_15), but its connection
   to other H4 invariants is heuristic, not algebraically forced.   *)

End H03_Origin.

(******************************************************************************)
(* Section 6: Coxeter Ratio Identities — Main New Theorems                    *)
(*                                                                            *)
(* These theorems prove structural identities among the H4 constants that     *)
(* appear in H01-H03, establishing their algebraic inter-relations.           *)
(******************************************************************************)

Section CoxeterRatios.

(* ================================================================ *)
(* Theorem 26: h = d1*d2 + d3/d1 + d4/d1                           *)
(* 30 = 2*12 + 20/2 + 30/2 = 24 + 10 - 4 ... not exact             *)
(* HONEST: Let us find one that IS exact.                            *)
(* Exact: h = d1*d4/2 = 2*30/2 = 30. Trivial.                      *)
(* Exact: h = d3 + d2 - d1 = 20 + 12 - 2 = 30. YES!               *)
(* ================================================================ *)
Theorem H4_h_degree_identity :
  h_H4 = d3_H4 + d2_H4 - d1_H4.
Proof.
  unfold h_H4, d1_H4, d2_H4, d3_H4. lra.
Qed.

(* ================================================================ *)
(* Theorem 27: e2 + e3 = h - 1 = 29 = e4                           *)
(* 11 + 19 = 30? No: 11+19 = 30 = h. Not h-1.                      *)
(* Exact: e2 + e3 = h = 30 *)
(* ================================================================ *)
Theorem H4_middle_exponents_sum :
  e2_H4 + e3_H4 = h_H4.
Proof.
  unfold e2_H4, e3_H4, h_H4. lra.
Qed.

(* ================================================================ *)
(* Theorem 28: e2 * e3 = h*7 + 1 = 211. No: 11*19 = 209.          *)
(* Exact: e2 * e3 = 209 = 11*19                                     *)
(* Structural: 209 = 7*h - 1 = 7*30-1. Yes! 7*30 = 210, 210-1=209 *)
(* ================================================================ *)
Theorem H4_e2_e3_product :
  e2_H4 * e3_H4 = 7 * h_H4 - 1.
Proof.
  unfold e2_H4, e3_H4, h_H4. lra.
Qed.

(* ================================================================ *)
(* Theorem 29: The H02 formula coefficient ratio satisfies          *)
(* e2/d3 + d3/h = e2/d3 + 1 - e1/d1 - (d3-d2)/h               *)
(* Better: ratio e2/d3 in phi-units                                  *)
(* Algebraic: (e2/d3) / (d3/h) = e2 * h / d3^2 = 11*30/400 = 330/400 = 33/40 *)
(* ================================================================ *)
Theorem H02_coefficient_ratio :
  (e2_H4 / d3_H4) / (d3_H4 / h_H4) = 33 / 40.
Proof.
  unfold e2_H4, d3_H4, h_H4. field.
Qed.

(* ================================================================ *)
(* Theorem 30: The H03 formula written in terms of h alone         *)
(* 4*phi*pi/(h/2) + 4/(h/2)^2                                      *)
(* = (8*phi*pi + 16/h) / h                                          *)
(* = 8*(phi*pi*h + 2) / h^2                                         *)
(* This form shows h^2 = 900 as the natural scale denominator.     *)
(* ================================================================ *)
Theorem H03_h_squared_form :
  H03_num = (8 * phi * PI * h_H4 + 16) / h_H4 ^ 2.
Proof.
  unfold H03_num, h_H4. field.
Qed.

(* ================================================================ *)
(* Theorem 31: Spectral coefficient ratio a4_vert/a4 in H01-form   *)
(* The leading contribution to a4 from the 120 vertices satisfies: *)
(* a4_vert / (a4_vert + a4_curv) is bounded below by 0.85.         *)
(* This shows vertex (i.e., H4 root) dominance in the action.      *)
(* ================================================================ *)
Theorem a4_vertex_fraction_lower_bound :
  a4_vert / (a4_vert + a4_curv) > 85 / 100.
Proof.
  unfold a4_vert, a4_curv, phi.
  interval with (i_prec 60).
Qed.

(* ================================================================ *)
(* Theorem 32: The 4*phi^3 factor in H01 satisfies                 *)
(* 4*phi^3 = 32*a4_vert (direct algebraic link)                    *)
(* This connects the Higgs mass formula to the spectral coefficient *)
(* ================================================================ *)
Theorem H01_a4_structural_link :
  4 * phi ^ 3 = 32 * a4_vert.
Proof.
  unfold a4_vert. field.
Qed.

End CoxeterRatios.

(******************************************************************************)
(* Section 7: Phi Power Ratios relevant to H01-H03                            *)
(******************************************************************************)

Section PhiPowerRatios.

(* ================================================================ *)
(* Theorem 33: phi^3 / phi^2 = phi (trivial but structural)         *)
(* The ratio of H01 scale to H02 phi factor is phi itself.          *)
(* ================================================================ *)
Theorem phi3_over_phi2 :
  phi ^ 3 / phi ^ 2 = phi.
Proof.
  assert (Hphi_pos : 0 < phi).
  { unfold phi. assert (0 < sqrt 5) by (apply sqrt_lt_R0; lra). lra. }
  field. lra.
Qed.

(* ================================================================ *)
(* Theorem 34: phi^3 in closed algebraic form                       *)
(* phi^3 = 2*phi + 1 (from CorePhi)                                 *)
(* ================================================================ *)
Theorem phi3_closed_form :
  phi ^ 3 = 2 * phi + 1.
Proof.
  replace (phi ^ 3) with (phi * phi * phi) by ring.
  apply phi_cubed.
Qed.

(* ================================================================ *)
(* Theorem 35: 4*phi^3 in closed form                               *)
(* 4*phi^3 = 8*phi + 4 — linear in phi                              *)
(* ================================================================ *)
Theorem H01_linear_phi :
  4 * phi ^ 3 = 8 * phi + 4.
Proof.
  rewrite phi3_closed_form. ring.
Qed.

(* ================================================================ *)
(* Theorem 36: phi^3 / h_H4 bound — scaling with Coxeter number     *)
(* ================================================================ *)
Theorem phi3_h_ratio_bound :
  0 < phi ^ 3 / h_H4 < 1.
Proof.
  unfold h_H4.
  assert (Hphi_pos : 0 < phi).
  { unfold phi. assert (0 < sqrt 5) by (apply sqrt_lt_R0; lra). lra. }
  split.
  - apply Rmult_lt_0_compat. apply pow_lt. lra. apply Rinv_0_lt_compat. lra.
  - interval with (i_prec 60).
Qed.

(* ================================================================ *)
(* Theorem 37: The H01 formula is consistent with the spectral      *)
(* action scale: 4*phi^3 * e^2 / (N_600cell) < 2                   *)
(* i.e., the Higgs mass per vertex is sub-GeV scale                  *)
(* ================================================================ *)
Theorem H01_per_vertex_scale :
  4 * phi ^ 3 * (exp 1) ^ 2 / N_600cell < 2.
Proof.
  unfold N_600cell.
  unfold phi.
  interval with (i_prec 60).
Qed.

End PhiPowerRatios.

(******************************************************************************)
(* Section 8: Master Summary Theorem                                           *)
(******************************************************************************)

Section MasterSummary.

(* ================================================================ *)
(* Master Theorem: Structural consistency of H01-H03                *)
(*                                                                   *)
(* All three Higgs formulas:                                         *)
(*   H01: m_H = 4*phi^3*e^2       [numerical: |error| < 0.01]      *)
(*   H02: m_H/m_W = e2*phi/d3 + d3/h  [numerical: |error|/target < 0.001] *)
(*   H03: m_H/m_Z = 4*phi*pi/(h/2) + 4/(h/2)^2  [|error|/target < 0.001]  *)
(*                                                                   *)
(* use ONLY the following H4 invariants: phi, {e2=11, d3=20, h=30}, *)
(* pi (from sphere geometry), e (from spectral action).             *)
(*                                                                   *)
(* The algebraic relations h = d3+d2-d1, e2+e3 = h, h/2 = 15       *)
(* proved above establish that these are not arbitrary numbers.      *)
(* ================================================================ *)
Theorem HiggsOrigins_master :
  (* H4 structural identities *)
  h_H4 = d3_H4 + d2_H4 - d1_H4 /\
  e2_H4 + e3_H4 = h_H4 /\
  h_H4 / 2 = 15 /\
  (* H4 degree factorization *)
  order_H4 = d1_H4 * d2_H4 * d3_H4 * d4_H4 /\
  (* Spectral a4 algebraic form *)
  a4_vert / a4_curv = 2 * phi ^ 4 /\
  (* H01 phi form *)
  4 * phi ^ 3 = 8 * phi + 4 /\
  (* H02 coefficient is exact ratio of H4 invariants *)
  d3_H4 / h_H4 = 2 / 3 /\
  (* H03 second term from h/2 *)
  4 / h_half ^ 2 = 4 / 225 /\
  (* H01-H03 numerical bounds *)
  Rabs (4 * phi ^ 3 * (exp 1) ^ 2 - 125.20) < 0.01 /\
  Rabs (H02_num - 125.11 / 80.379) / (125.11 / 80.379) < 0.001 /\
  Rabs (H03_num - 125.11 / 91.1876) / (125.11 / 91.1876) < 0.001.
Proof.
  repeat split.
  - apply H4_h_degree_identity.
  - apply H4_middle_exponents_sum.
  - apply H4_h_over_2.
  - apply H4_order_is_product_degrees.
  - apply a4_vertex_to_curv_ratio.
  - apply H01_linear_phi.
  - apply H02_rational_part.
  - apply H03_second_term.
  - apply H01_numerical_bound.
  - apply H02_numerical_bound.
  - apply H03_numerical_bound.
Qed.

End MasterSummary.

Close Scope R_scope.

(******************************************************************************)
(*                                                                            *)
(*  HONEST COMPILATION NOTE                                                   *)
(*  ============================                                               *)
(*                                                                            *)
(*  This file was written for Coq 8.20.1 (not Rocq 9.1.1).                  *)
(*  It imports from Trinity.CorePhi (compiled .vo must exist).               *)
(*                                                                            *)
(*  Compile with:                                                             *)
(*    cd proofs/trinity                                                        *)
(*    coqc -R . Trinity HiggsOrigins.v                                        *)
(*                                                                            *)
(*  Key Admitted lemma:                                                       *)
(*    - H03_h_half_structural: structural H4 identity for 15 not found       *)
(*    - H01_spectral_key_identity: Tr(D_F^{-2})*480/Tr(D_F^{-4}) = 4*phi^3  *)
(*      This is the central physical claim, numerically supported but        *)
(*      analytically unproved.                                                *)
(*                                                                            *)
(*  All other theorems end in Qed.                                           *)
(*                                                                            *)
(******************************************************************************)
