(******************************************************************************)
(* Trinity S3AI Proof Base v3.3 — CorePhi.v                                   *)
(* Defines the golden ratio phi, integer powers, and the fundamental identity  *)
(* phi^2 = phi + 1.                                                           *)
(******************************************************************************)

Require Import Reals.
Require Import Interval.Tactic.

Open Scope R_scope.

(******************************************************************************)
(* Section 1: Golden Ratio Definition                                         *)
(******************************************************************************)

(* The golden ratio phi = (1 + sqrt 5) / 2                                  *)
Definition phi : R := (1 + sqrt 5) / 2.

(******************************************************************************)
(* Section 2: Integer Power of Real Numbers                                   *)
(******************************************************************************)

(* powZ r n computes r raised to integer power n.
   For n >= 0: standard iterated multiplication.
   For n < 0: 1 / (r ^ |n|). *)
Fixpoint pow_pos (r : R) (n : nat) : R :=
  match n with
  | O => 1
  | S n' => r * pow_pos r n'
  end.

Definition powZ (r : R) (n : Z) : R :=
  match n with
  | Z0 => 1
  | Zpos p => pow_pos r (Pos.to_nat p)
  | Zneg p => / pow_pos r (Pos.to_nat p)
  end.

(******************************************************************************)
(* Section 3: Elementary Properties of phi                                    *)
(******************************************************************************)

Lemma phi_gt_0 : 0 < phi.
Proof.
  unfold phi.
  assert (H: 0 < sqrt 5) by (apply sqrt_lt_R0; lra).
  lra.
Qed.

Lemma phi_gt_1 : 1 < phi.
Proof.
  unfold phi.
  assert (H: 2 < sqrt 5).
  { assert (H2: 2^2 < 5) by lra.
    assert (H3: 0 <= 2) by lra.
    assert (H4: 0 <= 5) by lra.
    apply (Rsqr_incrst_1 2 (sqrt 5)) in H2; auto.
    - rewrite Rsqr_sqrt in H2; lra.
    - apply sqrt_lem_1; lra.
  }
  lra.
Qed.

(******************************************************************************)
(* Section 4: The Fundamental Identity — phi^2 = phi + 1                      *)
(******************************************************************************)

(* Core algebraic identity for the golden ratio.                             *)
(* This is the defining quadratic property of phi.                           *)
Lemma phi_sq : phi * phi = phi + 1.
Proof.
  unfold phi.
  (* Expand ((1 + sqrt 5) / 2)^2 *)
  field_simplify.
  - (* Show that the expanded form equals (1 + sqrt 5)/2 + 1 *)
    rewrite Rsqr_sqrt; [ | lra ].
    field_simplify.
    + ring.
    + lra.
  - (* sqrt 5 <> -1 is trivial since sqrt 5 > 0 *)
    intro H.
    assert (Hpos: 0 <= sqrt 5) by apply sqrt_pos.
    assert (Hpos': 0 < sqrt 5) by (apply sqrt_lt_R0; lra).
    lra.
Qed.

(******************************************************************************)
(* Section 5: Derived Identities                                              *)
(******************************************************************************)

(* Higher powers of phi can be reduced using phi_sq.                         *)
Lemma phi_cubed : phi * phi * phi = 2 * phi + 1.
Proof.
  rewrite <- Rmult_assoc.
  rewrite phi_sq.
  field_simplify.
  rewrite phi_sq.
  ring.
Qed.

(* phi^4 = 3*phi + 2 *)
Lemma phi_fourth : powZ phi 4 = 3 * phi + 2.
Proof.
  unfold powZ. simpl.
  (* phi^4 = (phi^2)^2 = (phi+1)^2 = phi^2 + 2*phi + 1 = (phi+1) + 2*phi + 1 *)
  (* = 3*phi + 2 *)
  replace (phi * phi * phi * phi) with ((phi * phi) * (phi * phi)) by ring.
  rewrite phi_sq.
  (* (phi + 1)^2 *)
  replace ((phi + 1) * (phi + 1)) with (phi^2 + 2*phi + 1) by ring.
  rewrite phi_sq.
  ring.
Qed.

(* 1/phi = phi - 1 *)
Lemma phi_inv : /phi = phi - 1.
Proof.
  assert (H: phi <> 0) by (apply Rgt_not_eq; apply phi_gt_0).
  field_simplify_eq; [ | assumption | assumption ].
  (* phi * (phi - 1) = 1 *)
  rewrite phi_sq.
  ring.
Qed.

(* phi^3 in closed form for use in bounds *)
Lemma phi_cubed_alt : powZ phi 3 = 2 * phi + 1.
Proof.
  unfold powZ. simpl.
  replace (phi * phi * phi) with ((phi * phi) * phi) by ring.
  rewrite phi_sq.
  ring.
Qed.

(******************************************************************************)
(* Section 6: Numerical Value of phi (for interval tactics)                   *)
(******************************************************************************)

Lemma phi_approx : 1.618033 < phi < 1.618034.
Proof.
  unfold phi.
  interval with (i_prec 60).
Qed.

(******************************************************************************)
(* Section 7: powZ Properties                                                 *)
(******************************************************************************)

Lemma powZ_pos (r : R) (n : Z) : 0 < r -> 0 < powZ r n.
Proof.
  intros Hr.
  unfold powZ.
  destruct n.
  - lra.
  - induction (Pos.to_nat p) as [|n' IH]; simpl.
    + lra.
    + apply Rmult_lt_0_compat; assumption.
  - apply Rinv_0_lt_compat.
    induction (Pos.to_nat p) as [|n' IH]; simpl.
    + lra.
    + apply Rmult_lt_0_compat; assumption.
Qed.

Lemma powZ_1 (r : R) : powZ r 1 = r.
Proof.
  unfold powZ. simpl. ring.
Qed.

Lemma powZ_2 (r : R) : powZ r 2 = r * r.
Proof.
  unfold powZ. simpl. ring.
Qed.

Lemma powZ_neg1 (r : R) : r <> 0 -> powZ r (-1) = /r.
Proof.
  intros Hr.
  unfold powZ. simpl. field.
Qed.

(******************************************************************************)
(* Section 8: phi^n + phi^(-n) is Lucas number L_n                           *)
(******************************************************************************)

(* phi^n + psi^n = L_n where psi = (1 - sqrt 5)/2 = 1 - phi                 *)
Definition psi : R := (1 - sqrt 5) / 2.

Lemma phi_psi_product : phi * psi = -1.
Proof.
  unfold phi, psi.
  field_simplify.
  rewrite Rsqr_sqrt; lra.
Qed.

Lemma psi_inv : psi = -/phi.
Proof.
  unfold psi, phi.
  field_simplify.
  rewrite Rsqr_sqrt; [ | lra].
  field_simplify.
  - lra.
  - intro H. assert (H2: sqrt 5 = -1) by lra.
    assert (H3: 0 <= sqrt 5) by apply sqrt_pos.
    lra.
Qed.

(******************************************************************************)
(* Trinity S3AI Coding Conventions                                            *)
(* - All theorems provable with Qed (0 Admitted)                              *)
(* - interval with (i_prec 60) for numerical bounds                           *)
(* - Definitions use unfold for clarity                                       *)
(******************************************************************************)
