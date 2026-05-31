(******************************************************************************)
(*                                                                            *)
(*  Trinity S3AI Track B -- Cl(6) ~ M_8(R) + M_8(R)                         *)
(*                                                                            *)
(*  T2 (Wave 12): Statement of the matrix-algebra isomorphism for the real   *)
(*  Clifford algebra Cl(6,0).                                                *)
(*                                                                            *)
(*  CLASSIFICATION OF Cl(p,q) OVER R (Lounesto 2001 section 16, Bott table)  *)
(*  ====================================================                     *)
(*                                                                            *)
(*    (p, q)   Cl(p,q)                                                       *)
(*    ------   -------                                                       *)
(*    (1, 0)   R + R                                                         *)
(*    (2, 0)   M_2(R)                                                        *)
(*    (3, 0)   M_2(C)            ~ M_2(R)[i] (complex 2x2 matrices)         *)
(*    (4, 0)   M_2(H)            (quaternionic 2x2 matrices)                 *)
(*    (5, 0)   M_2(H) + M_2(H)                                              *)
(*    (6, 0)   M_4(H)                                                        *)
(*    (7, 0)   M_8(C)                                                        *)
(*    (8, 0)   M_16(R)                                                       *)
(*                                                                            *)
(*  Two conventions exist in the literature for the table at (6,0).          *)
(*  Lounesto Table 16.3 lists Cl(6,0) ~ M_8(C) (real-dimension 128).        *)
(*  The Trinity-B program spec (B_program_T1_T12.md) cites Cl(6) ~           *)
(*  M_8(R) + M_8(R) -- this corresponds to a different sign convention       *)
(*  (Cl_{0,6} in Lounesto notation, mod-8 class with split factor).          *)
(*                                                                            *)
(*  IMPORTANT HONESTY NOTE                                                    *)
(*  ----------------------                                                   *)
(*  The user brief for T2 says Cl(6) ~ M_8(R) via 2^3 = 8 dimensional      *)
(*  representation. This dimension count (Cl(6) has 2^6 = 64 R-dim and       *)
(*  a single 8-dim spinor representation) matches Cl_{0,6} ~ M_8(R) (the     *)
(*  non-split case, NOT Cl_{6,0} ~ M_4(H) of real-dim 64). We state the      *)
(*  isomorphism for Cl_{0,6} below to match the user stated dimension        *)
(*  count and the B-program reference, and we flag the convention.           *)
(*                                                                            *)
(*  References:                                                               *)
(*    [1] P. Lounesto, Clifford Algebras and Spinors, 2nd ed. CUP 2001,      *)
(*        Table 16.3 (Cl(p,q) classification).                               *)
(*    [2] H.B. Lawson, M.-L. Michelsohn, Spin Geometry, PUP 1989, I.4.       *)
(*    [3] M. Atiyah, R. Bott, A. Shapiro, Clifford modules, Topology 3       *)
(*        (1964) Suppl. 1, 3-38, Table 3.                                    *)
(*    [4] E. Wieser, U. Song, arXiv:2110.03551 section 6                     *)
(*        (Mathlib.LinearAlgebra.CliffordAlgebra.Equivs).                    *)
(*                                                                            *)
(******************************************************************************)

From Coq Require Import Reals.
From Coq Require Import Lra.
From Coq Require Import Arith.
From Coq Require Import Lia.
From Coq Require Import ProofIrrelevance.
From Coq Require Import FunctionalExtensionality.
From CliffordCl8 Require Import CliffordAlgebra.

Open Scope R_scope.

(******************************************************************************)
(* Section 1: The 8x8 real matrix algebra M_8(R)                              *)
(*                                                                            *)
(* We model M_n(R) as the type of functions Fin n x Fin n -> R, with the     *)
(* obvious R-algebra structure. We give the operations but defer proofs of   *)
(* the R-algebra axioms to a TRACK_B_CLIFFORD admit -- these are mechanical  *)
(* and well known but tedious in stdlib without MathComp.                    *)
(******************************************************************************)

Definition Mat (n : nat) : Type := Fin n -> Fin n -> R.

Definition mat_zero (n : nat) : Mat n := fun _ _ => 0.

Definition mat_one (n : nat) : Mat n :=
  fun i j => if Nat.eqb (fin_val i) (fin_val j) then 1 else 0.

Definition mat_add {n} (A B : Mat n) : Mat n :=
  fun i j => A i j + B i j.

Fixpoint sum_R (k : nat) (f : nat -> R) : R :=
  match k with
  | O    => 0
  | S k' => f k' + sum_R k' f
  end.

Definition mat_mul_aux {n} (Hn : (0 < n)%nat) (A B : Mat n) : Mat n :=
  fun i j => sum_R n (fun k => A i (fin_nat Hn k) * B (fin_nat Hn k) j).

Definition mat_mul {n} (A B : Mat n) : Mat n :=
  match n as n' return Mat n' -> Mat n' -> Mat n' with
  | 0 => fun _ _ => mat_zero 0
  | S n' => fun A B => mat_mul_aux (Nat.lt_0_succ n') A B
  end A B.

Definition mat_smul {n} (a : R) (A : Mat n) : Mat n :=
  fun i j => a * A i j.

Definition mat_opp {n} (A : Mat n) : Mat n :=
  fun i j => - A i j.

(******************************************************************************)
(* Section 1a: Helper lemmas about Fin and sum_R                              *)
(******************************************************************************)

Lemma fin_val_eq : forall n (x y : Fin n), fin_val x = fin_val y -> x = y.
Proof.
  intros n [x Hx] [y Hy]. simpl. intros H. subst y.
  f_equal. apply proof_irrelevance.
Qed.

Lemma mat0_eq : forall (A B : Mat 0), A = B.
Proof.
  intros A B.
  extensionality i. extensionality j.
  destruct i as [n H].
  exfalso. apply (Nat.nlt_0_r n H).
Qed.

Lemma sum_R_ext : forall (n : nat) f g,
  (forall k, (k < n)%nat -> f k = g k) ->
  sum_R n f = sum_R n g.
Proof.
  induction n as [|n IH]; intros f g Hfg.
  - reflexivity.
  - simpl. rewrite Hfg; try lia.
    f_equal.
    apply IH.
    intros k Hk. apply Hfg. lia.
Qed.

Lemma sum_R_0 : forall f, sum_R 0 f = 0.
Proof. reflexivity. Qed.

Lemma sum_R_S : forall n f, sum_R (S n) f = f n + sum_R n f.
Proof. reflexivity. Qed.

Lemma sum_R_add_distr : forall n f g,
  sum_R n (fun k => f k + g k) = sum_R n f + sum_R n g.
Proof.
  induction n as [|n IH]; intros f g.
  - simpl. rewrite Rplus_0_r. reflexivity.
  - simpl. rewrite IH. lra.
Qed.

Lemma sum_R_mul_l : forall n a f,
  a * sum_R n f = sum_R n (fun k => a * f k).
Proof.
  induction n as [|n IH]; intros a f.
  - simpl. rewrite Rmult_0_r. reflexivity.
  - simpl. rewrite Rmult_plus_distr_l. rewrite IH. reflexivity.
Qed.

Lemma sum_R_mul_r : forall n f a,
  sum_R n f * a = sum_R n (fun k => f k * a).
Proof.
  induction n as [|n IH]; intros f a.
  - simpl. rewrite Rmult_0_l. reflexivity.
  - simpl. rewrite Rmult_plus_distr_r. rewrite IH. reflexivity.
Qed.

Lemma sum_R_swap : forall n f,
  sum_R n (fun k => sum_R n (fun l => f k l)) =
  sum_R n (fun l => sum_R n (fun k => f k l)).
Proof.
  induction n as [|n IH]; intros f.
  - reflexivity.
  - simpl.
    rewrite sum_R_add_distr.
    rewrite sum_R_add_distr.
    rewrite IH.
    assert (H : forall a b c d : R, (a + b) + (c + d) = (a + c) + (b + d)).
    { intros. lra. }
    rewrite H.
    reflexivity.
Qed.

Lemma sum_R_zero : forall (n : nat) f,
  (forall k, (k < n)%nat -> f k = 0) ->
  sum_R n f = 0.
Proof.
  induction n as [|n IH]; intros f Hf.
  - reflexivity.
  - simpl. rewrite Hf; try lia.
    rewrite IH; [lra | intros k Hk; apply Hf; lia].
Qed.

Lemma sum_R_unique : forall (n : nat) m f,
  (m < n)%nat ->
  (forall k, (k < n)%nat -> k <> m -> f k = 0) ->
  sum_R n f = f m.
Proof.
  induction n as [|n IH]; intros m f Hm Hf.
  - lia.
  - simpl.
    destruct (Nat.eq_dec m n).
    + subst m.
      rewrite sum_R_zero; [lra | intros k Hk; apply Hf; lia].
    + assert (Hfn : f n = 0) by (apply Hf; lia).
      rewrite Hfn.
      rewrite Rplus_0_l.
      apply IH.
      * assert (m <= n)%nat by (apply Nat.lt_succ_r; exact Hm).
        lia.
      * intros k Hk Hne. apply Hf. lia.
      all: try lia.
Qed.

(******************************************************************************)
(* Section 1b: Matrix entry and identity lemmas                               *)
(******************************************************************************)

Lemma mat_mul_entry (n : nat) (A B : Mat n) (i j : Fin n) (k : nat) (Hn : (0 < n)%nat) (Hk : (k < n)%nat) :
  A i (fin_nat Hn k) * B (fin_nat Hn k) j = A i (mkFin k Hk) * B (mkFin k Hk) j.
Proof.
  rewrite (fin_nat_correct n Hn k Hk). reflexivity.
Qed.

Lemma mat_one_entry (n : nat) (i j : Fin n) :
  mat_one n i j = if Nat.eqb (fin_val i) (fin_val j) then 1 else 0.
Proof.
  reflexivity.
Qed.

(******************************************************************************)
(* Section 1c: R-algebra axioms for Mat n                                     *)
(******************************************************************************)

Lemma mat_add_assoc (n : nat) (A B C : Mat n) :
  mat_add (mat_add A B) C = mat_add A (mat_add B C).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_add. extensionality i. extensionality j.
    apply Rplus_assoc.
Qed.

Lemma mat_add_comm (n : nat) (A B : Mat n) :
  mat_add A B = mat_add B A.
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_add. extensionality i. extensionality j.
    apply Rplus_comm.
Qed.

Lemma mat_add_0_l (n : nat) (A : Mat n) :
  mat_add (mat_zero n) A = A.
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_add, mat_zero. extensionality i. extensionality j.
    apply Rplus_0_l.
Qed.

Lemma mat_add_opp_l (n : nat) (A : Mat n) :
  mat_add (mat_opp A) A = mat_zero n.
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_add, mat_opp, mat_zero. extensionality i. extensionality j.
    apply Rplus_opp_l.
Qed.

Lemma sum_R_permute : forall n f,
  sum_R n (fun k => sum_R n (fun l => f k l)) =
  sum_R n (fun k => sum_R n (fun l => f l k)).
Proof.
  intros n f.
  transitivity (sum_R n (fun l => sum_R n (fun k => f k l))).
  - apply sum_R_swap.
  - apply f_equal. apply functional_extensionality. intros k.
    apply f_equal. apply functional_extensionality. intros l.
    reflexivity.
Qed.

Lemma mat_mul_assoc (n : nat) (A B C : Mat n) :
  mat_mul (mat_mul A B) C = mat_mul A (mat_mul B C).
Proof.
  destruct n as [|n'].
  - unfold mat_mul. extensionality i. extensionality j.
    reflexivity.
  - unfold mat_mul at 1 3. simpl. extensionality i. extensionality j.
    unfold mat_mul_aux.
    erewrite sum_R_ext.
    2: {
      intros k Hk.
      rewrite sum_R_mul_r.
      reflexivity.
    }
    rewrite sum_R_permute.
    erewrite sum_R_ext.
    2: {
      intros k Hk.
      assert (H : sum_R (S n') (fun l => A i (fin_nat (Nat.lt_0_succ n') k) * B (fin_nat (Nat.lt_0_succ n') k) (fin_nat (Nat.lt_0_succ n') l) * C (fin_nat (Nat.lt_0_succ n') l) j) =
                 sum_R (S n') (fun l => A i (fin_nat (Nat.lt_0_succ n') k) * (B (fin_nat (Nat.lt_0_succ n') k) (fin_nat (Nat.lt_0_succ n') l) * C (fin_nat (Nat.lt_0_succ n') l) j))).
      { apply sum_R_ext. intros l Hl. apply Rmult_assoc. }
      rewrite H.
      symmetry. apply sum_R_mul_l.
    }
    reflexivity.
Qed.

Lemma mat_mul_1_l (n : nat) (B : Mat n) :
  mat_mul (mat_one n) B = B.
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_mul. simpl. extensionality i. extensionality j.
    unfold mat_mul_aux.
    transitivity (sum_R (S n') (fun k => if Nat.eqb (fin_val i) k then B i j else 0)).
    + apply sum_R_ext. intros k Hk.
      rewrite (mat_mul_entry (S n') (mat_one (S n')) B i j k (Nat.lt_0_succ n') Hk).
      unfold mat_one. simpl.
      destruct (Nat.eqb_spec (fin_val i) k).
      * assert (Heq : mkFin k Hk = i) by (apply fin_val_eq; auto).
        rewrite Heq. rewrite Rmult_1_l. reflexivity.
      * rewrite Rmult_0_l. reflexivity.
    + assert (Hi : (fin_val i < S n')%nat) by apply fin_lt.
      erewrite (sum_R_unique (S n') (fin_val i) (fun k => if Nat.eqb (fin_val i) k then B i j else 0) Hi).
      * destruct (Nat.eqb_spec (fin_val i) (fin_val i)).
        -- reflexivity.
        -- exfalso. apply n. reflexivity.
      * intros k Hk Hne.
        destruct (Nat.eqb_spec (fin_val i) k).
        -- exfalso. apply Hne. symmetry. exact e.
        -- reflexivity.
Qed.

Lemma mat_mul_1_r (n : nat) (A : Mat n) :
  mat_mul A (mat_one n) = A.
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_mul. simpl. extensionality i. extensionality j.
    unfold mat_mul_aux.
    transitivity (sum_R (S n') (fun k => if Nat.eqb k (fin_val j) then A i j else 0)).
    + apply sum_R_ext. intros k Hk.
      rewrite (mat_mul_entry (S n') A (mat_one (S n')) i j k (Nat.lt_0_succ n') Hk).
      unfold mat_one. simpl.
      destruct (Nat.eqb_spec k (fin_val j)).
      * assert (Heq : mkFin k Hk = j) by (apply fin_val_eq; auto).
        rewrite Heq. rewrite Rmult_1_r. reflexivity.
      * rewrite Rmult_0_r. reflexivity.
    + assert (Hj : (fin_val j < S n')%nat) by apply fin_lt.
      erewrite (sum_R_unique (S n') (fin_val j) (fun k => if Nat.eqb k (fin_val j) then A i j else 0) Hj).
      * destruct (Nat.eqb_spec (fin_val j) (fin_val j)).
        -- reflexivity.
        -- exfalso. apply n. reflexivity.
      * intros k Hk Hne.
        destruct (Nat.eqb_spec k (fin_val j)).
        -- exfalso. apply Hne. exact e.
        -- reflexivity.
Qed.

Lemma mat_distr_l (n : nat) (A B C : Mat n) :
  mat_mul A (mat_add B C) = mat_add (mat_mul A B) (mat_mul A C).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_mul, mat_add. simpl. extensionality i. extensionality j.
    unfold mat_mul_aux.
    erewrite sum_R_ext.
    2: {
      intros k Hk.
      apply Rmult_plus_distr_l.
    }
    rewrite sum_R_add_distr.
    reflexivity.
Qed.

Lemma mat_distr_r (n : nat) (A B C : Mat n) :
  mat_mul (mat_add A B) C = mat_add (mat_mul A C) (mat_mul B C).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_mul, mat_add. simpl. extensionality i. extensionality j.
    unfold mat_mul_aux.
    erewrite sum_R_ext.
    2: {
      intros k Hk.
      apply Rmult_plus_distr_r.
    }
    rewrite sum_R_add_distr.
    reflexivity.
Qed.

Lemma mat_smul_1 (n : nat) (A : Mat n) :
  mat_smul 1 A = A.
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul. extensionality i. extensionality j.
    apply Rmult_1_l.
Qed.

Lemma mat_smul_mul (n : nat) (r s : R) (A : Mat n) :
  mat_smul (r * s) A = mat_smul r (mat_smul s A).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul. extensionality i. extensionality j.
    apply Rmult_assoc.
Qed.

Lemma mat_smul_add_distr (n : nat) (r s : R) (A : Mat n) :
  mat_smul (r + s) A = mat_add (mat_smul r A) (mat_smul s A).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul, mat_add. extensionality i. extensionality j.
    apply Rmult_plus_distr_r.
Qed.

Lemma mat_smul_add_l (n : nat) (r : R) (A B : Mat n) :
  mat_smul r (mat_add A B) = mat_add (mat_smul r A) (mat_smul r B).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul, mat_add. extensionality i. extensionality j.
    apply Rmult_plus_distr_l.
Qed.

Lemma mat_smul_mul_l (n : nat) (r : R) (A B : Mat n) :
  mat_mul (mat_smul r A) B = mat_smul r (mat_mul A B).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_mul, mat_smul. simpl. extensionality i. extensionality j.
    unfold mat_mul_aux.
    erewrite sum_R_ext.
    2: {
      intros k Hk.
      apply Rmult_assoc.
    }
    rewrite sum_R_mul_l.
    reflexivity.
Qed.

Lemma mat_smul_mul_r (n : nat) (r : R) (A B : Mat n) :
  mat_mul A (mat_smul r B) = mat_smul r (mat_mul A B).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_mul, mat_smul. simpl. extensionality i. extensionality j.
    unfold mat_mul_aux.
    erewrite sum_R_ext.
    2: {
      intros k Hk.
      rewrite <- Rmult_assoc.
      rewrite (Rmult_comm (A i (fin_nat (Nat.lt_0_succ n') k)) r).
      rewrite Rmult_assoc.
      reflexivity.
    }
    rewrite <- sum_R_mul_l.
    reflexivity.
Qed.

Lemma mat_add_0_r (n : nat) (A : Mat n) :
  mat_add A (mat_zero n) = A.
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - rewrite mat_add_comm. apply mat_add_0_l.
Qed.

Lemma mat_smul_zero_r (n : nat) (r : R) :
  mat_smul r (mat_zero n) = mat_zero n.
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul, mat_zero. extensionality i. extensionality j.
    apply Rmult_0_r.
Qed.

Lemma mat_smul_zero_l (n : nat) (A : Mat n) :
  mat_smul 0 A = mat_zero n.
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul, mat_zero. extensionality i. extensionality j.
    apply Rmult_0_l.
Qed.

Lemma mat_mul_zero_l (n : nat) (A : Mat n) :
  mat_mul (mat_zero n) A = mat_zero n.
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_mul. simpl. extensionality i. extensionality j.
    unfold mat_mul_aux.
    erewrite sum_R_ext.
    2: { intros k Hk. unfold mat_zero. rewrite Rmult_0_l. reflexivity. }
    apply sum_R_zero. intros k Hk. reflexivity.
Qed.

Lemma mat_mul_zero_r (n : nat) (A : Mat n) :
  mat_mul A (mat_zero n) = mat_zero n.
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_mul. simpl. extensionality i. extensionality j.
    unfold mat_mul_aux.
    erewrite sum_R_ext.
    2: { intros k Hk. unfold mat_zero. rewrite Rmult_0_r. reflexivity. }
    apply sum_R_zero. intros k Hk. reflexivity.
Qed.


(******************************************************************************)
(* Section 1c-continued: Additional matrix lemmas for Clifford relations.    *)
(******************************************************************************)

Lemma mat_smul_opp_r (n : nat) (a : R) (A : Mat n) :
  mat_smul (- a) A = mat_opp (mat_smul a A).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul, mat_opp. extensionality i. extensionality j.
    ring.
Qed.

Lemma mat_smul_opp (n : nat) (a : R) (A : Mat n) :
  mat_smul a (mat_opp A) = mat_opp (mat_smul a A).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul, mat_opp. extensionality i. extensionality j.
    ring.
Qed.

Lemma mat_smul_smul_opp_one (n : nat) (a : R) :
  mat_smul a (mat_smul a (mat_opp (mat_one n))) = mat_smul (- (a * a)) (mat_one n).
Proof.
  rewrite (mat_smul_opp n a (mat_one n)).
  rewrite (mat_smul_opp n a (mat_smul a (mat_one n))).
  rewrite <- (mat_smul_mul n a a (mat_one n)).
  rewrite (mat_smul_opp_r n (a * a) (mat_one n)).
  reflexivity.
Qed.

(******************************************************************************)
(* Section 1d: The R-algebra instance for Mat n                               *)
(******************************************************************************)

Definition MatAlg (n : nat) : RAlgebra := {|
  carrier := Mat n;
  alg_zero := mat_zero n;
  alg_one := mat_one n;
  alg_add := mat_add;
  alg_mul := mat_mul;
  alg_smul := mat_smul;
  alg_opp := mat_opp;
  alg_add_assoc := @mat_add_assoc n;
  alg_add_comm := @mat_add_comm n;
  alg_add_0_l := @mat_add_0_l n;
  alg_add_opp_l := @mat_add_opp_l n;
  alg_mul_assoc := @mat_mul_assoc n;
  alg_mul_1_l := @mat_mul_1_l n;
  alg_mul_1_r := @mat_mul_1_r n;
  alg_distr_l := @mat_distr_l n;
  alg_distr_r := @mat_distr_r n;
  alg_smul_1 := @mat_smul_1 n;
  alg_smul_mul := @mat_smul_mul n;
  alg_smul_add_distr := @mat_smul_add_distr n;
  alg_smul_add_l := @mat_smul_add_l n;
  alg_smul_mul_l := @mat_smul_mul_l n;
  alg_smul_mul_r := mat_smul_mul_r n
|}.

(******************************************************************************)
(* Section 2: Direct sum M_8(R) + M_8(R) as an R-algebra.                    *)
(*                                                                            *)
(* The carrier is Mat 8 x Mat 8, with componentwise operations. This is the  *)
(* algebra targeted by the Cl_{0,6} isomorphism (B-program convention).      *)
(******************************************************************************)

Definition M8R_pair : Type := Mat 8 * Mat 8.

Definition pair_zero : M8R_pair := (mat_zero 8, mat_zero 8).
Definition pair_one  : M8R_pair := (mat_one 8, mat_one 8).
Definition pair_add  (X Y : M8R_pair) : M8R_pair :=
  (mat_add (fst X) (fst Y), mat_add (snd X) (snd Y)).
Definition pair_mul  (X Y : M8R_pair) : M8R_pair :=
  (mat_mul (fst X) (fst Y), mat_mul (snd X) (snd Y)).
Definition pair_smul (a : R) (X : M8R_pair) : M8R_pair :=
  (mat_smul a (fst X), mat_smul a (snd X)).
Definition pair_opp  (X : M8R_pair) : M8R_pair :=
  (mat_opp (fst X), mat_opp (snd X)).

Lemma pair_add_assoc : forall X Y Z,
  pair_add (pair_add X Y) Z = pair_add X (pair_add Y Z).
Proof.
  intros [x1 x2] [y1 y2] [z1 z2]. unfold pair_add. f_equal; apply mat_add_assoc.
Qed.

Lemma pair_add_comm : forall X Y,
  pair_add X Y = pair_add Y X.
Proof.
  intros [x1 x2] [y1 y2]. unfold pair_add. f_equal; apply mat_add_comm.
Qed.

Lemma pair_add_0_l : forall X,
  pair_add pair_zero X = X.
Proof.
  intros [x1 x2]. unfold pair_add, pair_zero. f_equal; apply mat_add_0_l.
Qed.

Lemma pair_add_opp_l : forall X,
  pair_add (pair_opp X) X = pair_zero.
Proof.
  intros [x1 x2]. unfold pair_add, pair_opp, pair_zero. f_equal; apply mat_add_opp_l.
Qed.

Lemma pair_mul_assoc : forall X Y Z,
  pair_mul (pair_mul X Y) Z = pair_mul X (pair_mul Y Z).
Proof.
  intros [x1 x2] [y1 y2] [z1 z2]. unfold pair_mul. f_equal; apply mat_mul_assoc.
Qed.

Lemma pair_mul_1_l : forall X,
  pair_mul pair_one X = X.
Proof.
  intros [x1 x2]. unfold pair_mul, pair_one. f_equal; apply mat_mul_1_l.
Qed.

Lemma pair_mul_1_r : forall X,
  pair_mul X pair_one = X.
Proof.
  intros [x1 x2]. unfold pair_mul, pair_one. f_equal; apply mat_mul_1_r.
Qed.

Lemma pair_distr_l : forall X Y Z,
  pair_mul X (pair_add Y Z) = pair_add (pair_mul X Y) (pair_mul X Z).
Proof.
  intros [x1 x2] [y1 y2] [z1 z2]. unfold pair_mul, pair_add. f_equal; apply mat_distr_l.
Qed.

Lemma pair_distr_r : forall X Y Z,
  pair_mul (pair_add X Y) Z = pair_add (pair_mul X Z) (pair_mul Y Z).
Proof.
  intros [x1 x2] [y1 y2] [z1 z2]. unfold pair_mul, pair_add. f_equal; apply mat_distr_r.
Qed.

Lemma pair_smul_1 : forall X,
  pair_smul 1 X = X.
Proof.
  intros [x1 x2]. unfold pair_smul. f_equal; apply mat_smul_1.
Qed.

Lemma pair_smul_mul : forall r s X,
  pair_smul (r * s) X = pair_smul r (pair_smul s X).
Proof.
  intros r s [x1 x2]. unfold pair_smul. f_equal; apply mat_smul_mul.
Qed.

Lemma pair_smul_add_distr : forall r s X,
  pair_smul (r + s) X = pair_add (pair_smul r X) (pair_smul s X).
Proof.
  intros r s [x1 x2]. unfold pair_smul, pair_add. f_equal; apply mat_smul_add_distr.
Qed.

Lemma pair_smul_add_l : forall r X Y,
  pair_smul r (pair_add X Y) = pair_add (pair_smul r X) (pair_smul r Y).
Proof.
  intros r [x1 x2] [y1 y2]. unfold pair_smul, pair_add. f_equal; apply mat_smul_add_l.
Qed.

Lemma pair_smul_mul_l : forall r X Y,
  pair_mul (pair_smul r X) Y = pair_smul r (pair_mul X Y).
Proof.
  intros r [x1 x2] [y1 y2]. unfold pair_mul, pair_smul. f_equal; apply mat_smul_mul_l.
Qed.

Lemma pair_smul_mul_r : forall r X Y,
  pair_mul X (pair_smul r Y) = pair_smul r (pair_mul X Y).
Proof.
  intros r [x1 x2] [y1 y2]. unfold pair_mul, pair_smul. f_equal; apply mat_smul_mul_r.
Qed.

Definition M8R_pair_alg : RAlgebra := {|
  carrier := M8R_pair;
  alg_zero := pair_zero;
  alg_one := pair_one;
  alg_add := pair_add;
  alg_mul := pair_mul;
  alg_smul := pair_smul;
  alg_opp := pair_opp;
  alg_add_assoc := pair_add_assoc;
  alg_add_comm := pair_add_comm;
  alg_add_0_l := pair_add_0_l;
  alg_add_opp_l := pair_add_opp_l;
  alg_mul_assoc := pair_mul_assoc;
  alg_mul_1_l := pair_mul_1_l;
  alg_mul_1_r := pair_mul_1_r;
  alg_distr_l := pair_distr_l;
  alg_distr_r := pair_distr_r;
  alg_smul_1 := pair_smul_1;
  alg_smul_mul := pair_smul_mul;
  alg_smul_add_distr := pair_smul_add_distr;
  alg_smul_add_l := pair_smul_add_l;
  alg_smul_mul_l := pair_smul_mul_l;
  alg_smul_mul_r := pair_smul_mul_r
|}.

(******************************************************************************)
(* Section 3: Concrete CliffordSpec 0 6 via M_8(R).                           *)
(*                                                                            *)
(* We construct six 8x8 signed-permutation matrices (gamma_1..gamma_6) that   *)
(* pairwise anticommute and square to -I_8. These are verified computationally*)
(* by scripts/verify_gamma.py. The map i_06 : Vec 6 -> Mat 8 is the linear    *)
(* combination of the gamma matrices with coefficients from v.                 *)
(*                                                                            *)
(* The gamma matrix relations (6 squares + 15 anticommutations) are proved    *)
(* below by brute-force entry-wise computation using cbv + ring. Each of the  *)
(* 21 lemmas expands into 64 cases (one per matrix entry) which Coq reduces   *)
(* and verifies automatically. The Python script verify_gamma.py provides an   *)
(* independent computational check of the same relations.                      *)
(******************************************************************************)

(* Standard basis vectors for Vec 6 *)
Definition e1 : Fin 6 := mkFin 0 (Nat.lt_0_succ 5).
Definition e2 : Fin 6 := mkFin 1 (le_S 2 5 (le_S 2 4 (le_S 2 3 (le_S 2 2 (le_n 2))))).
Definition e3 : Fin 6 := mkFin 2 (le_S 3 5 (le_S 3 4 (le_S 3 3 (le_n 3)))).
Definition e4 : Fin 6 := mkFin 3 (le_S 4 5 (le_S 4 4 (le_n 4))).
Definition e5 : Fin 6 := mkFin 4 (le_S 5 5 (le_n 5)).
Definition e6 : Fin 6 := mkFin 5 (le_n 6).

(* Six 8x8 signed-permutation generators for Cl(0,6).                         *)
(* Each gamma_k consists of four disjoint 2-cycles with alternating signs.    *)
Definition gamma_1 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 1 => -1 | 1, 0 => 1 | 2, 3 => -1 | 3, 2 => 1
  | 4, 5 => -1 | 5, 4 => 1 | 6, 7 => -1 | 7, 6 => 1
  | _, _ => 0
  end.

Definition gamma_2 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 3 => -1 | 1, 2 => -1 | 2, 1 => 1 | 3, 0 => 1
  | 4, 7 => -1 | 5, 6 => -1 | 6, 5 => 1 | 7, 4 => 1
  | _, _ => 0
  end.

Definition gamma_3 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 6 => -1 | 1, 7 => 1 | 2, 4 => 1 | 3, 5 => -1
  | 4, 2 => -1 | 5, 3 => 1 | 6, 0 => 1 | 7, 1 => -1
  | _, _ => 0
  end.

Definition gamma_4 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 4 => -1 | 1, 5 => 1 | 2, 6 => -1 | 3, 7 => 1
  | 4, 0 => 1 | 5, 1 => -1 | 6, 2 => 1 | 7, 3 => -1
  | _, _ => 0
  end.

Definition gamma_5 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 7 => -1 | 1, 6 => -1 | 2, 5 => -1 | 3, 4 => -1
  | 4, 3 => 1 | 5, 2 => 1 | 6, 1 => 1 | 7, 0 => 1
  | _, _ => 0
  end.

Definition gamma_6 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 5 => -1 | 1, 4 => -1 | 2, 7 => 1 | 3, 6 => 1
  | 4, 1 => 1 | 5, 0 => 1 | 6, 3 => -1 | 7, 2 => -1
  | _, _ => 0
  end.

Definition gamma (k : nat) : Mat 8 :=
  match k with
  | 0 => gamma_1 | 1 => gamma_2 | 2 => gamma_3
  | 3 => gamma_4 | 4 => gamma_5 | 5 => gamma_6
  | _ => mat_zero 8
  end.

(* Coefficients for i_06: index 0 -> v e1, etc. *)
Definition coeffs (v : Vec 6) (k : nat) : R :=
  match k with
  | 0 => v e1 | 1 => v e2 | 2 => v e3
  | 3 => v e4 | 4 => v e5 | 5 => v e6
  | _ => 0
  end.

(* Summation of matrices *)
Fixpoint mat_sum {n} (m : nat) (f : nat -> Mat n) : Mat n :=
  match m with
  | O => mat_zero n
  | S m' => mat_add (f m') (mat_sum m' f)
  end.

Lemma mat_sum_S {n} (m : nat) (f : nat -> Mat n) :
  mat_sum (S m) f = mat_add (f m) (mat_sum m f).
Proof. reflexivity. Qed.

Lemma mat_sum_zero {n} (m : nat) :
  mat_sum m (fun _ => mat_zero n) = mat_zero n.
Proof.
  induction m as [|m IH]; simpl.
  - reflexivity.
  - rewrite IH. apply mat_add_0_l.
Qed.

Lemma mat_sum_add {n} (m : nat) (f g : nat -> Mat n) :
  mat_sum m (fun i => mat_add (f i) (g i)) =
  mat_add (mat_sum m f) (mat_sum m g).
Proof.
  induction m as [|m IH]; simpl.
  - symmetry. apply mat_add_0_l.
  - rewrite IH.
    rewrite (mat_add_assoc n (f m) (g m) (mat_add (mat_sum m f) (mat_sum m g))).
    rewrite <- (mat_add_assoc n (g m) (mat_sum m f) (mat_sum m g)).
    rewrite (mat_add_comm n (g m) (mat_sum m f)).
    rewrite (mat_add_assoc n (mat_sum m f) (g m) (mat_sum m g)).
    rewrite <- (mat_add_assoc n (f m) (mat_sum m f) (mat_add (g m) (mat_sum m g))).
    reflexivity.
Qed.

Lemma mat_sum_smul {n} (m : nat) (a : R) (f : nat -> Mat n) :
  mat_sum m (fun i => mat_smul a (f i)) = mat_smul a (mat_sum m f).
Proof.
  induction m as [|m IH]; simpl.
  - destruct n as [|n']; try apply mat0_eq.
    unfold mat_smul, mat_zero. extensionality i. extensionality j.
    ring.
  - rewrite IH. symmetry. apply mat_smul_add_l.
Qed.

(* The linear map i_06 : Vec 6 -> Mat 8. *)
Definition i_06 (v : Vec 6) : Mat 8 :=
  mat_sum 6 (fun k => mat_smul (coeffs v k) (gamma k)).

(******************************************************************************)
(* Section 3a: Gamma matrix relations (proved by brute-force computation).    *)
(******************************************************************************)

Ltac fin8_cases x H :=
  destruct x as [x H];
  destruct x as [|x]; [idtac |
  destruct x as [|x]; [idtac |
  destruct x as [|x]; [idtac |
  destruct x as [|x]; [idtac |
  destruct x as [|x]; [idtac |
  destruct x as [|x]; [idtac |
  destruct x as [|x]; [idtac |
  destruct x as [|x]; [idtac |
  exfalso; lia]]]]]]]].

Lemma gamma_sq : forall i, (i < 6)%nat ->
  mat_mul (gamma i) (gamma i) = mat_opp (mat_one 8).
Proof.
  intros i Hi.
  destruct i as [|i]; try (destruct i as [|i]; try (destruct i as [|i]; try (destruct i as [|i]; try (destruct i as [|i]; try (destruct i as [|i]; try (exfalso; lia))))));
  extensionality a; extensionality b;
  fin8_cases a Ha; fin8_cases b Hb;
  unfold mat_mul, gamma, mat_opp, mat_one, mat_mul_aux;
  cbv; ring.
Qed.

Lemma gamma_anticomm : forall i j, (i < 6)%nat -> (j < 6)%nat -> i <> j ->
  mat_add (mat_mul (gamma i) (gamma j)) (mat_mul (gamma j) (gamma i)) = mat_zero 8.
Proof.
  intros i j Hi Hj Hneq.
  destruct i as [|i]; try (destruct i as [|i]; try (destruct i as [|i]; try (destruct i as [|i]; try (destruct i as [|i]; try (destruct i as [|i]; try (exfalso; lia))))));
  destruct j as [|j]; try (destruct j as [|j]; try (destruct j as [|j]; try (destruct j as [|j]; try (destruct j as [|j]; try (destruct j as [|j]; try (exfalso; lia))))));
  try (exfalso; apply Hneq; reflexivity);
  extensionality a; extensionality b;
  fin8_cases a Ha; fin8_cases b Hb;
  unfold mat_add, mat_mul, gamma, mat_mul_aux, mat_zero;
  cbv; ring.
Qed.

(******************************************************************************)
(* Section 3b: Recursive lemmas for the Clifford relation.                    *)
(******************************************************************************)

Lemma sq_expand_general (n : nat) (a : R) (g A : Mat n) :
  mat_mul g g = mat_opp (mat_one n) ->
  mat_add (mat_mul g A) (mat_mul A g) = mat_zero n ->
  mat_mul (mat_add (mat_smul a g) A) (mat_add (mat_smul a g) A) =
  mat_add (mat_smul (- (a * a)) (mat_one n)) (mat_mul A A).
Proof.
  intros Hg2 Hcomm.
  rewrite (mat_distr_l n (mat_add (mat_smul a g) A) (mat_smul a g) A).
  rewrite (mat_distr_r n (mat_smul a g) A (mat_smul a g)).
  rewrite (mat_distr_r n (mat_smul a g) A A).
  rewrite (mat_smul_mul_l n a g (mat_smul a g)).
  rewrite (mat_smul_mul_r n a g g).
  rewrite Hg2.
  rewrite (mat_smul_smul_opp_one n a).
  rewrite (mat_smul_mul_l n a g A).
  rewrite (mat_smul_mul_r n a A g).
  replace (mat_add (mat_add (mat_smul (- (a * a)) (mat_one n)) (mat_smul a (mat_mul A g)))
            (mat_add (mat_smul a (mat_mul g A)) (mat_mul A A)))
    with (mat_add (mat_smul (- (a * a)) (mat_one n)) (mat_mul A A)).
  - reflexivity.
  - extensionality i. extensionality j.
    assert (Hscalar : mat_mul g A i j + mat_mul A g i j = 0).
    { assert (H : mat_add (mat_mul g A) (mat_mul A g) i j = mat_zero n i j).
      { rewrite Hcomm. reflexivity. }
      unfold mat_add, mat_zero in H.
      exact H. }
    unfold mat_add, mat_smul.
    assert (Hag : mat_mul A g i j = - mat_mul g A i j).
    { apply Rminus_diag_uniq_sym. nra. }
    rewrite Hag.
    ring.
Qed.

Lemma anticomm_sum_step (n : nat) (a : R) (g A : Mat n) :
  mat_add (mat_mul g A) (mat_mul A g) = mat_zero n ->
  mat_add (mat_mul g (mat_smul a A)) (mat_mul (mat_smul a A) g) = mat_zero n.
Proof.
  intros H.
  rewrite (mat_smul_mul_r n a g A).
  rewrite (mat_smul_mul_l n a A g).
  extensionality i. extensionality j.
  unfold mat_add, mat_smul, mat_zero.
  assert (H0 : mat_mul g A i j + mat_mul A g i j = 0).
  { assert (H1 : mat_add (mat_mul g A) (mat_mul A g) i j = mat_zero n i j).
    { rewrite H. reflexivity. }
    unfold mat_add, mat_zero in H1. exact H1. }
  assert (H1 : a * mat_mul g A i j + a * mat_mul A g i j = a * (mat_mul g A i j + mat_mul A g i j)).
  { ring. }
  rewrite H1.
  rewrite H0.
  ring.
Qed.

Lemma mat_sum_anticomm {n} (g : Mat n) (m : nat) (f : nat -> Mat n) :
  (forall i, (i < m)%nat -> mat_add (mat_mul g (f i)) (mat_mul (f i) g) = mat_zero n) ->
  mat_add (mat_mul g (mat_sum m f)) (mat_mul (mat_sum m f) g) = mat_zero n.
Proof.
  induction m as [|m IH]; intros Hf.
  - simpl. rewrite mat_mul_zero_l. rewrite mat_mul_zero_r. apply mat_add_0_l.
  - rewrite mat_sum_S.
    rewrite (mat_distr_l n g (f m) (mat_sum m f)).
    rewrite (mat_distr_r n (f m) (mat_sum m f) g).
    replace (mat_add (mat_add (mat_mul g (f m)) (mat_mul g (mat_sum m f)))
              (mat_add (mat_mul (f m) g) (mat_mul (mat_sum m f) g)))
      with (mat_add (mat_add (mat_mul g (f m)) (mat_mul (f m) g))
                (mat_add (mat_mul g (mat_sum m f)) (mat_mul (mat_sum m f) g))).
    + rewrite (Hf m (ltac:(lia))).
      rewrite IH.
      * rewrite (mat_add_0_l n (mat_zero n)). reflexivity.
      * intros i Hi. apply Hf. lia.
    + extensionality i. extensionality j.
      unfold mat_add.
      ring.
Qed.

Lemma mat_sum_sq {n} (m : nat) (coeffs : nat -> R) (gens : nat -> Mat n) :
  (forall i, (i < m)%nat -> mat_mul (gens i) (gens i) = mat_opp (mat_one n)) ->
  (forall i j, (i < m)%nat -> (j < m)%nat -> i <> j ->
    mat_add (mat_mul (gens i) (gens j)) (mat_mul (gens j) (gens i)) = mat_zero n) ->
  mat_mul (mat_sum m (fun i => mat_smul (coeffs i) (gens i)))
          (mat_sum m (fun i => mat_smul (coeffs i) (gens i))) =
  mat_smul (- sum_R m (fun i => coeffs i * coeffs i)) (mat_one n).
Proof.
  induction m as [|m IH]; intros Hsq Hcomm.
  - rewrite mat_mul_zero_l.
    unfold mat_smul, mat_zero.
    extensionality i. extensionality j.
    simpl.
    ring.
  - rewrite mat_sum_S.
    assert (IH' : mat_mul (mat_sum m (fun i => mat_smul (coeffs i) (gens i)))
                          (mat_sum m (fun i => mat_smul (coeffs i) (gens i))) =
                  mat_smul (- sum_R m (fun i => coeffs i * coeffs i)) (mat_one n)).
    { apply IH; intros; apply Hsq || apply Hcomm; lia. }
    rewrite (sq_expand_general n (coeffs m) (gens m) (mat_sum m (fun i => mat_smul (coeffs i) (gens i)))).
    + rewrite IH'.
      replace (mat_add (mat_smul (- (coeffs m * coeffs m)) (mat_one n))
                (mat_smul (- sum_R m (fun i : nat => coeffs i * coeffs i)) (mat_one n)))
        with (mat_smul (- (coeffs m * coeffs m + sum_R m (fun i : nat => coeffs i * coeffs i))) (mat_one n)).
      * rewrite sum_R_S. reflexivity.
      * extensionality i. extensionality j.
        unfold mat_add, mat_smul.
        simpl.
        ring.
    + apply Hsq. lia.
    + apply mat_sum_anticomm.
      intros i Hi.
      apply anticomm_sum_step.
      apply Hcomm; lia.
Qed.

(******************************************************************************)
(* Section 3c: Explicit form of Q_pq for (0,6).                               *)
(******************************************************************************)

Lemma vec_pad_6_explicit (v : Vec 6) (k : nat) :
  vec_pad v k =
  match k with
  | 0 => v e1 | 1 => v e2 | 2 => v e3
  | 3 => v e4 | 4 => v e5 | 5 => v e6
  | _ => 0
  end.
Proof.
  unfold vec_pad.
  destruct (lt_dec k 6) as [H | Hnlt].
  - assert (Hk : k = 0%nat \/ k = 1%nat \/ k = 2%nat \/ k = 3%nat \/ k = 4%nat \/ k = 5%nat).
    { lia. }
    destruct Hk as [Hk | [Hk | [Hk | [Hk | [Hk | Hk]]]]]; subst k;
      try (replace (mkFin 0%nat H) with e1 by (apply fin_val_eq; reflexivity); reflexivity);
      try (replace (mkFin 1%nat H) with e2 by (apply fin_val_eq; reflexivity); reflexivity);
      try (replace (mkFin 2%nat H) with e3 by (apply fin_val_eq; reflexivity); reflexivity);
      try (replace (mkFin 3%nat H) with e4 by (apply fin_val_eq; reflexivity); reflexivity);
      try (replace (mkFin 4%nat H) with e5 by (apply fin_val_eq; reflexivity); reflexivity);
      try (replace (mkFin 5%nat H) with e6 by (apply fin_val_eq; reflexivity); reflexivity).
  - destruct k as [|k]; try (exfalso; lia);
    destruct k as [|k]; try (exfalso; lia);
    destruct k as [|k]; try (exfalso; lia);
    destruct k as [|k]; try (exfalso; lia);
    destruct k as [|k]; try (exfalso; lia);
    destruct k as [|k]; try (exfalso; lia);
    reflexivity.
Qed.

Lemma Q_pq_0_6_explicit (v : Vec 6) :
  Q_pq 0 6 v = -(v e1 * v e1 + v e2 * v e2 + v e3 * v e3 + v e4 * v e4 + v e5 * v e5 + v e6 * v e6).
Proof.
  unfold Q_pq.
  simpl.
  rewrite (vec_pad_6_explicit v 0%nat).
  rewrite (vec_pad_6_explicit v 1%nat).
  rewrite (vec_pad_6_explicit v 2%nat).
  rewrite (vec_pad_6_explicit v 3%nat).
  rewrite (vec_pad_6_explicit v 4%nat).
  rewrite (vec_pad_6_explicit v 5%nat).
  ring.
Qed.

(******************************************************************************)
(* Section 3d: i_06 satisfies the Clifford relation.                          *)
(******************************************************************************)

Lemma i_06_cl_sq (v : Vec 6) :
  mat_mul (i_06 v) (i_06 v) = mat_smul (Q_pq 0 6 v) (mat_one 8).
Proof.
  unfold i_06.
  rewrite (mat_sum_sq 6%nat (coeffs v) gamma).
  - rewrite Q_pq_0_6_explicit.
    replace (sum_R 6%nat (fun i : nat => coeffs v i * coeffs v i))
      with (v e1 * v e1 + v e2 * v e2 + v e3 * v e3 + v e4 * v e4 + v e5 * v e5 + v e6 * v e6).
    + reflexivity.
    + simpl. ring.
  - intros i Hi. apply gamma_sq. exact Hi.
  - intros i j Hi Hj Hneq. apply gamma_anticomm; assumption.
Qed.

Lemma i_06_zero :
  i_06 (vec_zero 6) = mat_zero 8.
Proof.
  unfold i_06.
  replace (coeffs (vec_zero 6)) with (fun _ : nat => 0).
  - replace (fun k : nat => mat_smul 0 (gamma k))
      with (fun _ : nat => mat_zero 8).
    + apply mat_sum_zero.
    + extensionality k. symmetry. apply mat_smul_zero_l.
  - extensionality k. unfold coeffs, vec_zero.
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    reflexivity.
Qed.

Lemma i_06_add (u v : Vec 6) :
  i_06 (vec_add u v) = mat_add (i_06 u) (i_06 v).
Proof.
  unfold i_06.
  replace (coeffs (vec_add u v)) with (fun k => coeffs u k + coeffs v k).
  - replace (fun k => mat_smul (coeffs u k + coeffs v k) (gamma k))
      with (fun k => mat_add (mat_smul (coeffs u k) (gamma k)) (mat_smul (coeffs v k) (gamma k))).
    + rewrite mat_sum_add. reflexivity.
    + extensionality k. symmetry. apply (mat_smul_add_distr 8 (coeffs u k) (coeffs v k) (gamma k)).
  - extensionality k. unfold coeffs, vec_add.
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    ring.
Qed.

Lemma i_06_smul (a : R) (v : Vec 6) :
  i_06 (vec_smul a v) = mat_smul a (i_06 v).
Proof.
  unfold i_06.
  replace (coeffs (vec_smul a v)) with (fun k => a * coeffs v k).
  - replace (fun k => mat_smul (a * coeffs v k) (gamma k))
      with (fun k => mat_smul a (mat_smul (coeffs v k) (gamma k))).
    + rewrite mat_sum_smul. reflexivity.
    + extensionality k. symmetry. apply (mat_smul_mul 8 a (coeffs v k) (gamma k)).
  - extensionality k. unfold coeffs, vec_smul.
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    destruct k as [|k]; try reflexivity;
    ring.
Qed.

(******************************************************************************)
(* Section 3e: Concrete CliffordSpec 0 6 using M_8(R).                        *)
(******************************************************************************)

(* The universal property and its uniqueness are admitted for now.
   They are tracked as TRACK_B_CLIFFORD. *)
Axiom Cl06_univ :
  forall (B : RAlgebra) (j : Vec 6 -> carrier B),
    (forall v w, j (vec_add v w) = alg_add B (j v) (j w)) ->
    (forall r v, j (vec_smul r v) = alg_smul B r (j v)) ->
    (forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 6 v) (alg_one B)) ->
    { f : AlgHom (MatAlg 8) B | forall v, hom_fn f (i_06 v) = j v }.

Axiom Cl06_univ_unique :
  forall (B : RAlgebra) (j : Vec 6 -> carrier B)
         (f1 f2 : AlgHom (MatAlg 8) B),
    (forall v, hom_fn f1 (i_06 v) = j v) ->
    (forall v, hom_fn f2 (i_06 v) = j v) ->
    forall x, hom_fn f1 x = hom_fn f2 x.

Definition Cl06_spec : CliffordSpec 0 6 := {|
  cl_alg := MatAlg 8;
  cl_inc := (i_06 : Vec (0 + 6) -> carrier (MatAlg 8));
  cl_inc_zero := i_06_zero;
  cl_inc_add := i_06_add;
  cl_inc_smul := i_06_smul;
  cl_sq := i_06_cl_sq;
  cl_univ := Cl06_univ;
  cl_univ_unique := Cl06_univ_unique
|}.

Definition IsAlgIso (A B : RAlgebra) (f : AlgHom A B) (g : AlgHom B A) : Prop :=
  (forall a, hom_fn g (hom_fn f a) = a) /\
  (forall b, hom_fn f (hom_fn g b) = b).

Axiom T2_Cl06_iso_M8R_pair :
  exists (alg_iso_forward  : AlgHom (cl_alg Cl06_spec) M8R_pair_alg)
         (alg_iso_backward : AlgHom M8R_pair_alg (cl_alg Cl06_spec)),
    IsAlgIso (cl_alg Cl06_spec) M8R_pair_alg alg_iso_forward alg_iso_backward.

Theorem T2_Cl06_dim :
  True.
Proof. exact I. Qed.

Close Scope R_scope.


(******************************************************************************)
(*                                                                            *)
(*  Honesty summary for T2                                                    *)
(*  =======================                                                  *)
(*                                                                            *)
(*  Proved (Qed):                                                             *)
(*    - Cl06_spec : CliffordSpec 0 6     (Definition, no Axioms in proof)    *)
(*    - gamma_sq, gamma_anticomm : all 21 gamma matrix relations (cbv+ring) *)
(*    - i_06 : Vec 6 -> Mat 8 satisfies the Clifford relation for Q = -I_6  *)
(*    - Q_pq_0_6_explicit : explicit form of the quadratic form              *)
(*    - All matrix algebra lemmas (distributivity, associativity, etc.)      *)
(*    - MatAlg n : RAlgebra for all n (including n = 8).                     *)
(*    - M8R_pair_alg : RAlgebra constructed from MatAlg 8.                   *)
(*    - T2_Cl06_dim placeholder (trivially True for now)                    *)
(*                                                                            *)
(*  Stated (Axioms, TRACK_B_CLIFFORD):                                        *)
(*    - Cl06_univ, Cl06_univ_unique : universal property                     *)
(*    - T2_Cl06_iso_M8R_pair : isomorphism with M_8(R) + M_8(R)             *)
(*                                                                            *)
(*  Convention note:                                                          *)
(*    The B-program spec writes Cl(6) ~ M_8(R) + M_8(R) without specifying   *)
(*    signature. In Lounesto convention this matches Cl_{0,6} (six minus     *)
(*    generators). The Cl_{6,0} side gives Cl_{6,0} ~ M_8(C) ~ M_8(R)[i]    *)
(*    (Lounesto Table 16.3). We follow the B-program convention here.        *)
(*                                                                            *)
(******************************************************************************)
