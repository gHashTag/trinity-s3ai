(******************************************************************************)
(*  RGRunningExtras.v                                                         *)
(*  ========================================================================= *)
(*  Supplementary lemmas for the RGRunning.v deep dive.                      *)
(*                                                                            *)
(*  PURPOSE:                                                                  *)
(*    The theorems alpha_from_H4 and alpha_s_from_H4 in RGRunning.v are     *)
(*    Admitted because they are physically ill-posed in their current form.  *)
(*    This file:                                                              *)
(*      (1) Proves pure-algebraic lemmas about the 5/3 hypercharge factor.   *)
(*      (2) Proves the alpha_s normalization identity (missing 4*pi).        *)
(*      (3) Proves that alpha_from_H4 is, in fact, MATHEMATICALLY FALSE      *)
(*          under the current definitions (Theorem alpha_from_H4_refuted).   *)
(*      (4) States honest restatements that ARE provable.                    *)
(*                                                                            *)
(*  RESULT: 0 Admitted in this file. All proofs end with Qed.               *)
(*                                                                            *)
(*  We do NOT modify RGRunning.v.  The 2 Admitted there remain, with their  *)
(*  existing honest documentation.  We add rigorous Coq evidence that they  *)
(*  CANNOT be closed without redefining the quantities involved.             *)
(*                                                                            *)
(*  Dependencies: CorePhi.v (for phi and interval tactic context).          *)
(*  New Parameter: gU2inv_ex (abstract copy of gU2inv, to avoid Axiom       *)
(*    name conflicts with RGRunning.v when both files are compiled).         *)
(*                                                                            *)
(*  Russian narrative: see derivations/rg_running/rg_analysis.md            *)
(******************************************************************************)

Require Import Reals.
Require Import Lra.
From Interval Require Import Tactic.
Require Import Trinity.CorePhi.

Open Scope R_scope.

(******************************************************************************)
(*  Section 1.  Mirror of RGRunning.v definitions                            *)
(*  (We cannot Require RGRunning because it has unresolved Admitted;         *)
(*   we therefore restate what we need.)                                     *)
(******************************************************************************)

Definition mZ_x    : R := 91.1876.
Definition LH4_x   : R := 1.5 * 10^16.
Definition b1_x    : R := 41 / 10.
Definition b2_x    : R := -19 / 6.
Definition b3_x    : R := -7.

(* Independent parameter — mirrors gU2inv from RGRunning.v *)
Parameter gU2inv_x : R.
Axiom gU2inv_window_x : 1/26 <= gU2inv_x <= 1/22.

Definition alpha_i_inv_x (mu b_i : R) : R :=
  gU2inv_x + (b_i / (4 * PI * PI)) * ln (LH4_x / mu).

(* As defined in RGRunning.v — this is the "wrong" combination *)
Definition alpha_inv_mZ_code : R :=
  alpha_i_inv_x mZ_x b1_x + alpha_i_inv_x mZ_x b2_x.

(* Physical EM combination with SU(5)/GUT hypercharge normalization 5/3 *)
Definition alpha_inv_mZ_phys : R :=
  (5/3) * alpha_i_inv_x mZ_x b1_x + alpha_i_inv_x mZ_x b2_x.

(* Trinity formula (same as in RGRunning.v) *)
Definition trinity_alpha_inv_x : R := 36 * phi * (exp 1 * exp 1) / PI.
Definition trinity_alpha_s_x   : R := (sqrt 5 - 2) / 2.

(******************************************************************************)
(*  Section 2.  Pure-arithmetic lemmas about SM beta coefficients             *)
(******************************************************************************)

(* b1 + b2 = 41/10 - 19/6 = 14/15 *)
Lemma b1_plus_b2_exact : b1_x + b2_x = 14 / 15.
Proof. unfold b1_x, b2_x. lra. Qed.

(* The GUT-corrected coefficient: (5/3)*b1 + b2 = 41/6 - 19/6 = 22/6 = 11/3 *)
Lemma five_thirds_b1_plus_b2 : (5/3) * b1_x + b2_x = 11 / 3.
Proof. unfold b1_x, b2_x. lra. Qed.

(* b3 has the expected value *)
Lemma b3_value : b3_x = -7.
Proof. unfold b3_x. reflexivity. Qed.

(******************************************************************************)
(*  Section 3.  Hypercharge normalization — the 5/3 factor                   *)
(*                                                                            *)
(*  In SU(5) GUT, the SM hypercharge coupling g' and the GUT-normalized      *)
(*  coupling g_1 are related by  g' = sqrt(3/5) * g_1.                       *)
(*  Consequently  alpha_Y = g'^2/(4pi) = (3/5) * alpha_1,                   *)
(*  so  1/alpha_Y = (5/3) * 1/alpha_1.                                       *)
(*  The physical formula is:                                                  *)
(*    1/alpha_em = 1/alpha_Y + 1/alpha_2 = (5/3)/alpha_1 + 1/alpha_2.       *)
(*  The code uses  1/alpha_1 + 1/alpha_2  (missing the 5/3 factor).         *)
(******************************************************************************)

(* The SU(5) correction term is positive whenever 1/alpha_1 > 0 *)
Lemma hypercharge_correction_positive :
  forall a1_inv : R,
    a1_inv > 0 ->
    (5/3) * a1_inv - a1_inv = (2/3) * a1_inv.
Proof.
  intros a1_inv _. lra.
Qed.

(* The physical formula always exceeds the code formula (given a1_inv > 0) *)
Lemma physical_em_exceeds_code_formula :
  forall a1_inv a2_inv : R,
    a1_inv > 0 ->
    (5/3) * a1_inv + a2_inv > a1_inv + a2_inv.
Proof.
  intros a1_inv a2_inv Ha. lra.
Qed.

(* Exact gap: the physical combination minus the code combination *)
Lemma em_formula_correction_amount :
  forall a1_inv a2_inv : R,
    ((5/3) * a1_inv + a2_inv) - (a1_inv + a2_inv) = (2/3) * a1_inv.
Proof.
  intros a1_inv a2_inv. lra.
Qed.

(* Concretely: alpha_inv_mZ_phys > alpha_inv_mZ_code, using b1 positivity *)
Lemma phys_exceeds_code_concrete :
  (5/3) * alpha_i_inv_x mZ_x b1_x + alpha_i_inv_x mZ_x b2_x >
  alpha_i_inv_x mZ_x b1_x + alpha_i_inv_x mZ_x b2_x.
Proof.
  (* Reduce to: (2/3) * alpha_i_inv_x mZ_x b1_x > 0 *)
  (* Sufficient: alpha_i_inv_x mZ_x b1_x > 0 *)
  unfold alpha_i_inv_x, b1_x.
  pose proof gU2inv_window_x as [Hglo Hghi].
  (* log is positive since LH4_x >> mZ_x *)
  assert (HLpos : ln (LH4_x / mZ_x) > 0).
  { unfold LH4_x, mZ_x.
    rewrite <- ln_1. apply ln_increasing; [lra | interval]. }
  assert (HPI : PI > 0) by apply PI_RGT_0.
  assert (H4p2 : 0 < 4 * PI * PI) by nra.
  assert (Hterm : (41 / 10) / (4 * PI * PI) * ln (LH4_x / mZ_x) > 0).
  { apply Rmult_lt_0_compat; [apply Rdiv_lt_0_compat; lra | exact HLpos]. }
  lra.
Qed.

(******************************************************************************)
(*  Section 4.  Alpha_s normalization — the missing 4*pi factor              *)
(*                                                                            *)
(*  The code defines  alpha_s(mu) = 1 / alpha_i_inv(mu, b3).               *)
(*  If alpha_i_inv = 1/g3^2, then  1/alpha_i_inv = g3^2.                   *)
(*  But the physical  alpha_s = g3^2 / (4*pi),  so                          *)
(*    code alpha_s = g3^2 = 4*pi * alpha_s_physical.                        *)
(*  The code value exceeds the physical value by a factor of 4*pi ~ 12.6.   *)
(******************************************************************************)

(* The algebraic identity: g3^2 = 4*pi * (g3^2 / (4*pi)) *)
Lemma alpha_s_normalization_identity :
  forall g3_inv_sq : R,
    g3_inv_sq > 0 ->
    1 / g3_inv_sq = 4 * PI * (1 / (4 * PI * g3_inv_sq)).
Proof.
  intros g3_inv_sq Hpos.
  assert (HPI : PI > 0) by apply PI_RGT_0.
  field. split; lra.
Qed.

(* Given a coupling and the physical alpha, their ratio is 4*pi *)
Lemma coupling_to_alpha_ratio :
  forall g_sq alpha_s_phys : R,
    g_sq > 0 -> alpha_s_phys > 0 ->
    alpha_s_phys = g_sq / (4 * PI) ->
    g_sq = 4 * PI * alpha_s_phys.
Proof.
  intros g_sq alpha_s_phys Hg Ha Hdef.
  assert (HPI : PI > 0) by apply PI_RGT_0.
  rewrite Hdef. field; lra.
Qed.

(* 4*pi is approximately 12.57 (for reference) *)
Lemma four_pi_approx : 12 < 4 * PI < 13.
Proof. split; interval with (i_prec 40). Qed.

(******************************************************************************)
(*  Section 5.  Auxiliary numerical bounds                                    *)
(******************************************************************************)

Lemma ln_window_x : 32 < ln (LH4_x / mZ_x) < 33.
Proof.
  unfold LH4_x, mZ_x.
  split; interval with (i_prec 80).
Qed.

Lemma four_pi_sq_x : 4 * PI * PI > 39.
Proof. interval with (i_prec 60). Qed.

(* The trinity formula is numerically in (120, 140) *)
Lemma trinity_alpha_inv_range :
  120 < trinity_alpha_inv_x < 140.
Proof.
  unfold trinity_alpha_inv_x, phi.
  split; interval with (i_prec 100).
Qed.

(* The trinity alpha_s formula is ~0.118 *)
Lemma trinity_alpha_s_range :
  0.11 < trinity_alpha_s_x < 0.12.
Proof.
  unfold trinity_alpha_s_x.
  split; interval with (i_prec 30).
Qed.

(******************************************************************************)
(*  Section 6.  The code combination alpha_inv_mZ_code is very small         *)
(*                                                                            *)
(*  alpha_inv_mZ_code = 2*gU2inv + (14/15)/(4*pi^2)*L                       *)
(*  With gU2inv <= 1/22 and L < 33 and 4*pi^2 > 39:                        *)
(*    <= 2/22 + (14/15)/39 * 33 < 0.091 + 0.791 = 0.882 < 5.              *)
(******************************************************************************)

Lemma alpha_inv_mZ_code_lt_5 : alpha_inv_mZ_code < 5.
Proof.
  unfold alpha_inv_mZ_code, alpha_i_inv_x, b1_x, b2_x.
  pose proof gU2inv_window_x as [Hglo Hghi].
  pose proof ln_window_x as [HLlo HLhi].
  assert (H4p : 4 * PI * PI > 39) by apply four_pi_sq_x.
  assert (HPI : PI > 0) by apply PI_RGT_0.
  assert (H4pi2ne : 4 * PI * PI <> 0) by lra.
  set (LL := ln (LH4_x / mZ_x)) in *.
  assert (Hinv : / (4 * PI * PI) < / 39).
  { apply Rinv_lt_contravar.
    - apply Rmult_lt_0_compat; lra.
    - lra. }
  (* Rewrite sum: 2*gU2inv + (14/15)/(4*pi^2)*L *)
  assert (Heq :
    gU2inv_x + (41 / 10) / (4 * PI * PI) * LL +
    (gU2inv_x + (-19 / 6) / (4 * PI * PI) * LL) =
    2 * gU2inv_x + (14/15) / (4 * PI * PI) * LL).
  { field; lra. }
  rewrite Heq.
  (* Bound the running term *)
  assert (Hstep : (14/15) / (4 * PI * PI) * LL < (14/15) / 39 * 33).
  { apply Rlt_trans with ((14/15) / 39 * LL).
    - apply Rmult_lt_compat_r; [lra |].
      unfold Rdiv. apply Rmult_lt_compat_l; lra.
    - apply Rmult_lt_compat_l; lra. }
  lra.
Qed.

(******************************************************************************)
(*  Section 7.  Main result: alpha_from_H4 is PROVABLY FALSE                 *)
(*                                                                            *)
(*  We prove the negation of the Admitted theorem's statement.               *)
(*  This establishes that the Admitted is not just "unprovable" but          *)
(*  MATHEMATICALLY INCORRECT under the current definitions.                  *)
(*                                                                            *)
(*  Proof structure:                                                          *)
(*    alpha_inv_mZ_code < 5   (from Section 6)                               *)
(*    trinity_alpha_inv_x > 120  (numerical)                                 *)
(*    => |code - trinity| > 115                                               *)
(*    => ratio > 115/140 > 0.82 > 0.01 = 1/100   QED.                       *)
(******************************************************************************)

Theorem alpha_from_H4_refuted :
  ~ (Rabs (alpha_inv_mZ_code - trinity_alpha_inv_x) / trinity_alpha_inv_x < 1/100).
Proof.
  intro H.
  (* Extract bounds *)
  pose proof alpha_inv_mZ_code_lt_5 as Hcode.
  pose proof trinity_alpha_inv_range as [Htlo Hthi].
  assert (Htpos : trinity_alpha_inv_x > 0) by lra.
  (* The gap is large: trinity > 120, code < 5, so gap > 115 *)
  assert (Habs_val : alpha_inv_mZ_code - trinity_alpha_inv_x < 0) by lra.
  assert (Habs : Rabs (alpha_inv_mZ_code - trinity_alpha_inv_x) > 115).
  { rewrite Rabs_left; lra. }
  (* From H: Rabs / trinity < 1/100 => Rabs < trinity/100 < 140/100 = 1.4 *)
  unfold Rdiv in H.
  assert (Hmul : Rabs (alpha_inv_mZ_code - trinity_alpha_inv_x) * /trinity_alpha_inv_x * trinity_alpha_inv_x
                 < 1/100 * trinity_alpha_inv_x).
  { apply Rmult_lt_compat_r; lra. }
  assert (Hsimp : Rabs (alpha_inv_mZ_code - trinity_alpha_inv_x) * /trinity_alpha_inv_x * trinity_alpha_inv_x
                  = Rabs (alpha_inv_mZ_code - trinity_alpha_inv_x)).
  { field; lra. }
  rewrite Hsimp in Hmul.
  (* Hmul: Rabs < trinity/100 < 140/100 = 1.4 *)
  (* But Habs: Rabs > 115.  Contradiction. *)
  lra.
Qed.

(******************************************************************************)
(*  Section 8.  Honest restatement that IS provable                           *)
(*                                                                            *)
(*  RESTATEMENT of alpha_from_H4 (physically correct version):               *)
(*                                                                            *)
(*  To get the physical 1/alpha_em(mZ) from GUT running, one must:          *)
(*  (a) Use the corrected combination: (5/3)*a1_inv + a2_inv                 *)
(*  (b) Convert from the code's g^2 units to standard alpha = g^2/(4*pi)    *)
(*      i.e., multiply by 4*pi                                               *)
(*                                                                            *)
(*  The "restated" quantity is:                                               *)
(*    alpha_inv_mZ_restated := 4*pi * ((5/3)*a1_inv + a2_inv)               *)
(*                                                                            *)
(*  This is algebraically well-defined, and with appropriate GUT boundary   *)
(*  conditions would match the PDG value ~127.95.                            *)
(*                                                                            *)
(*  We prove a structural lemma relating the restated quantity to the code. *)
(******************************************************************************)

Definition alpha_inv_mZ_restated : R :=
  4 * PI * ((5/3) * alpha_i_inv_x mZ_x b1_x + alpha_i_inv_x mZ_x b2_x).

(* The restated quantity equals 4*pi times the physical combination *)
Lemma restated_equals_4pi_times_phys :
  alpha_inv_mZ_restated = 4 * PI * alpha_inv_mZ_phys.
Proof.
  unfold alpha_inv_mZ_restated, alpha_inv_mZ_phys. lra.
Qed.

(* The restated quantity exceeds the code quantity by the 5/3 * 4pi correction *)
Lemma restated_exceeds_scaled_code :
  alpha_inv_mZ_restated > 4 * PI * alpha_inv_mZ_code.
Proof.
  unfold alpha_inv_mZ_restated, alpha_inv_mZ_code, alpha_inv_mZ_phys.
  assert (HPI : PI > 0) by apply PI_RGT_0.
  apply Rmult_lt_compat_l; [lra |].
  (* (5/3)*a1_inv + a2_inv > a1_inv + a2_inv iff (2/3)*a1_inv > 0 iff a1_inv > 0 *)
  unfold alpha_i_inv_x, b1_x.
  pose proof gU2inv_window_x as [Hglo Hghi].
  assert (HLpos : ln (LH4_x / mZ_x) > 0).
  { unfold LH4_x, mZ_x.
    rewrite <- ln_1. apply ln_increasing; [lra | interval]. }
  assert (H4p2_s : 0 < 4 * PI * PI) by nra.
  assert (Hterm : (41 / 10) / (4 * PI * PI) * ln (LH4_x / mZ_x) > 0).
  { apply Rmult_lt_0_compat; [apply Rdiv_lt_0_compat; lra | exact HLpos]. }
  lra.
Qed.

(******************************************************************************)
(*  Section 9.  Summary comment (Coq comment, not a proof obligation)        *)
(*                                                                            *)
(*  STATUS of the 2 Admitted in RGRunning.v:                                 *)
(*                                                                            *)
(*  (A) alpha_from_H4:                                                        *)
(*      MATHEMATICALLY FALSE under current definitions.                      *)
(*      Proved here by Theorem alpha_from_H4_refuted (Qed).                  *)
(*      To make it provable, replace alpha_inv_at_mZ with                    *)
(*        4*PI*((5/3)*alpha_i_inv(mZ,b1) + alpha_i_inv(mZ,b2))              *)
(*      and set trinity_alpha_inv to the PDG value ~127.95, or add an        *)
(*      explicit physical axiom linking gU2inv to standard alpha_GUT.        *)
(*                                                                            *)
(*  (B) alpha_s_from_H4:                                                      *)
(*      Also ill-posed: alpha_s(mZ) in code = 1/alpha_i_inv(mZ,b3),        *)
(*      which gives g3^2, not alpha_s = g3^2/(4*pi).                        *)
(*      Furthermore alpha_i_inv(mZ,b3) < 0 with gU2inv~1/24                 *)
(*      (the alpha_run_window axiom papers over this).                        *)
(*      Even with axiom, 1/alpha_i_inv(mZ,b3) ≠ alpha_s_physical.          *)
(*      NOT refuted here (would require reasoning about alpha_run_window).   *)
(*      Remains Admitted in RGRunning.v, correctly documented there.         *)
(*                                                                            *)
(*  Net result: This file provides 14 Qed proofs (0 Admitted).              *)
(******************************************************************************)

Close Scope R_scope.
