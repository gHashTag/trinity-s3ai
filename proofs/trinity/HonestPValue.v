(******************************************************************************)
(* HonestPValue.v - Trinity V33                                               *)
(******************************************************************************)

Require Import Reals.
Require Import Lra.
Require Import Psatz.
Require Import Interval.Tactic.

Open Scope R_scope.

(* ========================================================================== *)
(* SECTION 1: Search Space Parameters                                         *)
(* ========================================================================== *)

Definition N_search_space : nat := 600.
Definition n_groups_tested : nat := 5.
Definition n_coefficients : nat := 17.

(* ========================================================================== *)
(* SECTION 2: Probability Model                                               *)
(* ========================================================================== *)

Fixpoint factorial (n : nat) : nat :=
  match n with
  | 0 => 1
  | S n' => n * factorial n'
  end.

Definition factorial_17 : nat := factorial 17.

Fixpoint nat_pow (base exp : nat) : nat :=
  match exp with
  | 0 => 1
  | S e' => base * nat_pow base e'
  end.

Definition N_to_17 : nat := nat_pow 600 17.

(* ========================================================================== *)
(* SECTION 3: Real number definitions                                          *)
(* ========================================================================== *)

(* 17! as real *)
Definition fact17_R : R := 355687428096000%R.

(* 600^17 = 169266594447360 * 10^33 as real.
   We write it as a product to enable algebraic cancellation of 10^33. *)
Definition N600_to_17_R : R := 169266594447360%R * 10 ^ 33.

(* Raw p-value: generous upper bound *)
Definition p_raw_generous : R := fact17_R / N600_to_17_R.

(* Bonferroni correction *)
Definition p_corrected : R := p_raw_generous * INR 5.

(* ========================================================================== *)
(* SECTION 4: Helper lemmas                                                   *)
(* ========================================================================== *)

(** Cross-multiplication for INR fractions.
    Avoids stack overflow from computing huge %R constants. *)
Lemma INR_lt_cross_mult : forall a b c d : nat,
  (0 < b)%nat -> (0 < d)%nat -> (a * d < c * b)%nat ->
  INR a / INR b < INR c / INR d.
Proof.
  intros a b c d Hb Hd H.
  apply lt_INR in H. repeat rewrite mult_INR in H.
  apply Rmult_lt_reg_r with (r := INR d).
  { apply lt_0_INR. auto with arith. }
  apply Rmult_lt_reg_r with (r := INR b).
  { apply lt_0_INR. auto with arith. }
  field_simplify; try (apply Rgt_not_eq; apply lt_0_INR; auto with arith).
  lra.
Qed.

(** 15 * 10^6 < 10^33, proved algebraically without computing huge powers.
    Strategy: 15 * 10^6 < 10^2 * 10^6 = 10^(2+6) = 10^8 < 10^33. *)
Lemma fifteen_times_ten_6_lt_ten_33 : (15 * 10 ^ 6 < 10 ^ 33)%nat.
Proof.
  (* Use transitivity through 10^8 (all in nat scope) *)
  apply Nat.lt_trans with (m := (10 ^ 8)%nat).
  - (* Show 15 * 10^6 < 10^8 = 10^2 * 10^6 *)
    replace ((10 ^ 8)%nat) with ((10 ^ 2)%nat * (10 ^ 6)%nat)%nat.
    2: { replace 8%nat with (2 + 6)%nat by reflexivity.
         rewrite Nat.pow_add_r. reflexivity. }
    apply Nat.mul_lt_mono_pos_r.
    + (* Show 0 < 10^6 *)
      apply Nat.neq_0_lt_0. intro Heq.
      assert (H10: (10 <> 0)%nat) by (intro H; discriminate H).
      assert (Hpow: ((10 ^ 6)%nat <> 0)%nat).
      { apply Nat.pow_nonzero. exact H10. }
      contradiction.
    + (* Show 15 < 10^2 = 100 *)
      repeat constructor.
  - (* Show 10^8 < 10^33 *)
    apply Nat.pow_lt_mono_r.
    + lia. (* 1 < 10 *)
    + lia. (* 8 < 33 *)
Qed.

(* ========================================================================== *)
(* SECTION 5: p_raw_bound via algebraic cancellation                          *)
(* ========================================================================== *)

(** p_raw_generous < 3/10^33
    
    Proof: p_raw = 355687428096000 / (169266594447360 * 10^33)
           We show 355687428096000 / (169266594447360 * 10^33) < 3 / 10^33
           Multiply by 10^33: 355687428096000 / 169266594447360 < 3
           Cross multiply: 355687428096000 < 3 * 169266594447360
           = 355687428096000 < 507799783342080  (true by compute) *)
Lemma p_raw_bound : p_raw_generous < 3 / (10 ^ 33).
Proof.
  unfold p_raw_generous, fact17_R, N600_to_17_R.
  (* Goal: 355687428096000 / (169266594447360 * 10^33) < 3 / 10^33 *)
  (* Multiply both sides by 10^33 (positive) *)
  apply Rmult_lt_reg_r with (r := 10 ^ 33).
  { apply pow_lt. lra. }
  (* Cancel 10^33 on left: a/(b*c)*c = a/b *)
  assert (Hcancel: 355687428096000%R / (169266594447360%R * 10^33) * 10^33
            = 355687428096000%R / 169266594447360%R).
  { unfold Rdiv.
    (* Replace Rinv_mult with explicit algebraic steps to avoid subgoal issues *)
    assert (H10: (10 ^ 33 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
    assert (H169: (169266594447360 : R) <> 0) by lra.
    field_simplify. lra. }
  rewrite Hcancel.
  (* Goal: 355687428096000 / 169266594447360 < 3 *)
  apply Rmult_lt_reg_r with (r := 169266594447360%R).
  { lra. }
  unfold Rdiv. repeat rewrite Rmult_assoc. rewrite Rinv_l.
  2: { apply Rgt_not_eq. lra. }
  rewrite Rmult_1_r.
  (* Goal: 355687428096000 < 3 * 169266594447360 = 507799783342080
     Use explicit replace to avoid computing large nats with 'compute' *)
  replace (3 * 169266594447360)%R with 507799783342080%R.
  2: { ring. }
  lra.
Qed.

(* ========================================================================== *)
(* SECTION 6: Key inequality 15/10^33 < 1/10^6                                *)
(* ========================================================================== *)

(** 3/10^33 * 5 = 15/10^33 < 1/10^6
    
    Proof: Cross multiply: 15 * 10^6 < 10^33
           Proved via fifteen_times_ten_6_lt_ten_33 (algebraic, no compute) *)
Lemma fifteen_over_ten_33_lt_one_over_ten_6 :
  3 / (10 ^ 33) * INR 5 < / (10 ^ 6).
Proof.
  (* 3/10^33 * 5 = 15/10^33 via field_simplify *)
  assert (H15: 3 / (10 ^ 33) * INR 5 = 15 / (10 ^ 33)).
  { assert (H10: (10 ^ 33 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
    field_simplify. simpl. lra. }
  rewrite H15.
  (* Need: 15/10^33 < 1/10^6, prove directly via cross-multiplication in R *)
  (* Both denominators are positive *)
  assert (H10_33: (10 ^ 33 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
  assert (H10_6: (10 ^ 6 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
  (* Rewrite 1/(10^6) as 10^33 / (10^33 * 10^6) *)
  assert (H1: / (10 ^ 6) = (10 ^ 33) / ((10 ^ 33) * (10 ^ 6))).
  { unfold Rdiv. rewrite Rinv_mult.
    assert (H33: (10 ^ 33 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
    assert (H6: (10 ^ 6 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
    field. all: assumption. }
  rewrite H1.
  (* Now: 15/10^33 < 10^33/(10^33*10^6)
     Multiply both sides by 10^33 (positive) *)
  assert (Hcancel: 15 / (10 ^ 33) * (10 ^ 33) = 15).
  { unfold Rdiv. rewrite Rmult_assoc. rewrite Rinv_l. 2: assumption.
    lra. }
  apply Rmult_lt_reg_r with (r := 10 ^ 33).
  { apply pow_lt. lra. }
  rewrite Hcancel.
  (* Right side: 10^33/(10^33*10^6) * 10^33 = 10^33/10^6 *)
  assert (Hcancel2: (10 ^ 33) / ((10 ^ 33) * (10 ^ 6)) * (10 ^ 33) = (10 ^ 33) / (10 ^ 6)).
  { unfold Rdiv. repeat rewrite Rmult_assoc.
    rewrite (Rmult_comm (/ ((10 ^ 33) * (10 ^ 6))) (10 ^ 33)).
    rewrite Rinv_mult.
    assert (H33: (10 ^ 33 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
    assert (H6: (10 ^ 6 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
    field. all: assumption. }
  rewrite Hcancel2.
  (* Now: 15 < 10^33/10^6, i.e. 15 * 10^6 < 10^33 *)
  apply Rmult_lt_reg_r with (r := 10 ^ 6).
  { apply pow_lt. lra. }
  assert (Hcancel3: (10 ^ 33) / (10 ^ 6) * (10 ^ 6) = 10 ^ 33).
  { unfold Rdiv. rewrite Rmult_assoc. rewrite Rinv_l. 2: assumption.
    lra. }
  rewrite Hcancel3.
  (* Goal: 15 * 10^6 < 10^33 as reals
     Strategy: 15 * 10^6 = 15 * 10^6 and 10^33 = 10^27 * 10^6
     So need 15 < 10^27, which is trivial. *)
  replace (10 ^ 33 : R) with (10 ^ 27 * 10 ^ 6 : R).
  2: { assert (H27: (33 = 27 + 6)%nat) by reflexivity.
       rewrite H27 at 1. rewrite Rdef_pow_add. reflexivity. }
  apply Rmult_lt_compat_r.
  { apply pow_lt. lra. }
  (* Goal: 15 < 10^27. Use transitivity: 15 < 100 = 10^2 < 10^27 *)
  apply Rlt_trans with (r2 := 10 ^ 2).
  + lra. (* 15 < 100 *)
  + apply Rlt_pow. lra. lia.
Qed.

(* ========================================================================== *)
(* SECTION 7: Main Theorem                                                    *)
(* ========================================================================== *)

Theorem honest_pvalue_bound : p_corrected < / (10 ^ 6).
Proof.
  unfold p_corrected.
  (* Step 1: p_raw * 5 < (3/10^33) * 5 using p_raw_bound *)
  apply Rlt_trans with (r2 := 3 / (10 ^ 33) * INR 5).
  - apply Rmult_lt_compat_r.
    + apply lt_0_INR; lia.
    + apply p_raw_bound.
  - (* Step 2: 15/10^33 < 1/10^6 *)
    apply fifteen_over_ten_33_lt_one_over_ten_6.
Qed.

(* ========================================================================== *)
(* SECTION 8: Alternative Monte Carlo bound                                   *)
(* ========================================================================== *)

Definition p_MC_95upper : R := 3 / (10 ^ 6).
Definition p_corrected_MC : R := p_MC_95upper * INR 5.

(** 15 * 10^4 < 10^6, i.e. 150000 < 1000000 *)
Lemma fifteen_times_ten_4_lt_ten_6 : (15 * 10 ^ 4 < 10 ^ 6)%nat.
Proof.
  (* 15 * 10^4 < 10^2 * 10^4 = 10^6 *)
  assert (Hmid: (10 ^ 2 * 10 ^ 4 = 10 ^ 6)%nat).
  { replace (6%nat) with ((2 + 4)%nat) by reflexivity.
    rewrite Nat.pow_add_r. reflexivity. }
  apply Nat.lt_le_trans with (m := (10 ^ 2 * 10 ^ 4)%nat).
  - apply Nat.mul_lt_mono_pos_r.
    + apply Nat.neq_0_lt_0. intro Heq.
      assert (H10: (10 <> 0)%nat) by (intro H; discriminate H).
      assert (Hpow: ((10 ^ 4)%nat <> 0)%nat).
      { apply Nat.pow_nonzero. exact H10. }
      contradiction.
    + repeat constructor. (* 15 < 100 *)
  - rewrite Hmid. apply Nat.le_refl.
Qed.

Lemma p_corrected_MC_bound : p_corrected_MC < / (10 ^ 4).
Proof.
  unfold p_corrected_MC, p_MC_95upper.
  (* 3/10^6 * 5 = 15/10^6 via field_simplify *)
  assert (H15: 3 / (10 ^ 6) * INR 5 = 15 / (10 ^ 6)).
  { assert (H10: (10 ^ 6 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
    field_simplify. simpl. lra. }
  rewrite H15.
  (* Need: 15/10^6 < 1/10^4, prove directly via cross-multiplication in R *)
  assert (H10_6: (10 ^ 6 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
  assert (H10_4: (10 ^ 4 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
  (* Rewrite 1/(10^4) as 10^6 / (10^6 * 10^4) *)
  assert (H1: / (10 ^ 4) = (10 ^ 6) / ((10 ^ 6) * (10 ^ 4))).
  { unfold Rdiv. rewrite Rinv_mult.
    assert (H6: (10 ^ 6 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
    assert (H4: (10 ^ 4 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
    field. all: assumption. }
  rewrite H1.
  (* Multiply both sides by 10^6 (positive) *)
  assert (Hcancel: 15 / (10 ^ 6) * (10 ^ 6) = 15).
  { unfold Rdiv. rewrite Rmult_assoc. rewrite Rinv_l. 2: assumption.
    lra. }
  apply Rmult_lt_reg_r with (r := 10 ^ 6).
  { apply pow_lt. lra. }
  rewrite Hcancel.
  (* Right side: 10^6/(10^6*10^4) * 10^6 = 10^6/10^4 *)
  assert (Hcancel2: (10 ^ 6) / ((10 ^ 6) * (10 ^ 4)) * (10 ^ 6) = (10 ^ 6) / (10 ^ 4)).
  { unfold Rdiv. repeat rewrite Rmult_assoc.
    rewrite (Rmult_comm (/ ((10 ^ 6) * (10 ^ 4))) (10 ^ 6)).
    rewrite Rinv_mult.
    assert (H6: (10 ^ 6 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
    assert (H4: (10 ^ 4 : R) <> 0) by (apply Rgt_not_eq; apply pow_lt; lra).
    field. all: assumption. }
  rewrite Hcancel2.
  (* Now: 15 < 10^6/10^4, i.e. 15 * 10^4 < 10^6 *)
  apply Rmult_lt_reg_r with (r := 10 ^ 4).
  { apply pow_lt. lra. }
  assert (Hcancel3: (10 ^ 6) / (10 ^ 4) * (10 ^ 4) = 10 ^ 6).
  { unfold Rdiv. rewrite Rmult_assoc. rewrite Rinv_l. 2: assumption.
    lra. }
  rewrite Hcancel3.
  (* Goal: 15 * 10^4 < 10^6 as reals
     Strategy: 15 * 10^4 = 15 * 10^4 and 10^6 = 10^2 * 10^4
     So need 15 < 10^2 = 100 *)
  replace (10 ^ 6 : R) with (10 ^ 2 * 10 ^ 4 : R).
  2: { assert (H24: (6 = 2 + 4)%nat) by reflexivity.
       rewrite H24 at 1. rewrite Rdef_pow_add. reflexivity. }
  apply Rmult_lt_compat_r.
  { apply pow_lt. lra. }
  (* Goal: 15 < 100 = 10^2 *)
  lra.
Qed.

(******************************************************************************)
(* End of HonestPValue.v                                                      *)
(******************************************************************************)
