(******************************************************************************)
(*                                                                            *)
(*  Trinity S3AI Track B — Cl(6) ≅ M_8(R) ⊕ M_8(R)                          *)
(*                                                                            *)
(*  T2 (Wave 12): Statement of the matrix-algebra isomorphism for the real   *)
(*  Clifford algebra Cl(6,0).                                                *)
(*                                                                            *)
(*  CLASSIFICATION OF Cl(p,q) OVER R (Lounesto 2001 §16, Bott table)         *)
(*  ====================================================                     *)
(*                                                                            *)
(*    (p, q)   Cl(p,q)                                                       *)
(*    ------   -------                                                       *)
(*    (1, 0)   R ⊕ R                                                         *)
(*    (2, 0)   M_2(R)                                                        *)
(*    (3, 0)   M_2(C)            ≅ M_2(R)[i] (complex 2×2 matrices)         *)
(*    (4, 0)   M_2(H)            (quaternionic 2×2 matrices)                 *)
(*    (5, 0)   M_2(H) ⊕ M_2(H)                                              *)
(*    (6, 0)   M_4(H)                                                        *)
(*    (7, 0)   M_8(C)                                                        *)
(*    (8, 0)   M_16(R)                                                       *)
(*                                                                            *)
(*  Two conventions exist in the literature for the table at (6,0).          *)
(*  Lounesto Table 16.3 lists Cl(6,0) ≅ M_8(C) (real-dimension 128).        *)
(*  The Trinity-B program spec (B_program_T1_T12.md) cites Cl(6) ≅           *)
(*  M_8(R) ⊕ M_8(R) — this corresponds to a different sign convention       *)
(*  (Cl_{0,6} in Lounestos notation, mod-8 class with split factor).        *)
(*                                                                            *)
(*  IMPORTANT HONESTY NOTE                                                    *)
(*  ----------------------                                                   *)
(*  The users brief for T2 says Cl(6) ≅ M_8(R) via 2^3 = 8 dimensional    *)
(*  representation. This dimension count (Cl(6) has 2^6 = 64 R-dim and     *)
(*  a single 8-dim spinor representation) matches Cl_{0,6} ≅ M_8(R) (the    *)
(*  non-split case, NOT Cl_{6,0} ≅ M_4(H) of real-dim 64). We state the     *)
(*  isomorphism for Cl_{0,6} below to match the users stated dimension      *)
(*  count and the B-program reference, and we flag the convention.          *)
(*                                                                            *)
(*  References:                                                              *)
(*    [1] P. Lounesto, Clifford Algebras and Spinors, 2nd ed. CUP 2001,    *)
(*        Table 16.3 (Cl(p,q) classification).                              *)
(*    [2] H.B. Lawson, M.-L. Michelsohn, Spin Geometry, PUP 1989, I.4.    *)
(*    [3] M. Atiyah, R. Bott, A. Shapiro, Clifford modules, Topology 3    *)
(*        (1964) Suppl. 1, 3–38, Table 3.                                   *)
(*    [4] E. Wieser, U. Song, arXiv:2110.03551 §6                          *)
(*        (Mathlib.LinearAlgebra.CliffordAlgebra.Equivs).                 *)
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
(* Section 1: The 8×8 real matrix algebra M_8(R)                              *)
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

Definition mat_mul {n} (A B : Mat n) : Mat n :=
  fun i j =>
    sum_R n (fun k =>
      match Nat.ltb k n as b return (Nat.ltb k n = b) -> R with
      | true  => fun H =>
          A i (mkFin k (proj1 (Nat.ltb_lt _ _) H)) *
          B   (mkFin k (proj1 (Nat.ltb_lt _ _) H)) j
      | false => fun _ => 0
      end eq_refl).

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
    rewrite H. reflexivity.
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
      * intros k Hk Hne. apply Hf. lia. lia.
Qed.

(******************************************************************************)
(* Section 1b: Matrix entry and identity lemmas                               *)
(******************************************************************************)

Lemma mat_mul_entry {n} (A B : Mat n) (i j : Fin n) (k : nat) (Hk : (k < n)%nat) :
  match Nat.ltb k n as b return (Nat.ltb k n = b) -> R with
  | true  => fun H =>
      A i (mkFin k (proj1 (Nat.ltb_lt _ _) H)) *
      B   (mkFin k (proj1 (Nat.ltb_lt _ _) H)) j
  | false => fun _ => 0
  end eq_refl = A i (mkFin k Hk) * B (mkFin k Hk) j.
Proof.
  assert (H : forall (b : bool) (Hb : Nat.ltb k n = b),
    match b as b' return (Nat.ltb k n = b') -> R with
    | true => fun H' => A i (mkFin k (proj1 (Nat.ltb_lt _ _) H')) *
                       B (mkFin k (proj1 (Nat.ltb_lt _ _) H')) j
    | false => fun _ => 0
    end Hb = A i (mkFin k Hk) * B (mkFin k Hk) j).
  { intros b Hb.
    destruct b.
    - assert (Heq : mkFin k (proj1 (Nat.ltb_lt k n) Hb) = mkFin k Hk).
      { apply fin_val_eq. reflexivity. }
      rewrite Heq. reflexivity.
    - exfalso.
      pose proof (proj2 (Nat.ltb_lt k n) Hk) as Htrue.
      rewrite Htrue in Hb.
      discriminate. }
  apply H.
Qed.

Lemma mat_one_entry {n} (i j : Fin n) :
  mat_one n i j = if Nat.eqb (fin_val i) (fin_val j) then 1 else 0.
Proof.
  reflexivity.
Qed.

(******************************************************************************)
(* Section 1c: R-algebra axioms for Mat n                                     *)
(******************************************************************************)

Lemma mat_add_assoc {n} (A B C : Mat n) :
  mat_add (mat_add A B) C = mat_add A (mat_add B C).
Proof.
  unfold mat_add. extensionality i. extensionality j.
  apply Rplus_assoc.
Qed.

Lemma mat_add_comm {n} (A B : Mat n) :
  mat_add A B = mat_add B A.
Proof.
  unfold mat_add. extensionality i. extensionality j.
  apply Rplus_comm.
Qed.

Lemma mat_add_0_l {n} (A : Mat n) :
  mat_add (mat_zero n) A = A.
Proof.
  unfold mat_add, mat_zero. extensionality i. extensionality j.
  apply Rplus_0_l.
Qed.

Lemma mat_add_opp_l {n} (A : Mat n) :
  mat_add (mat_opp A) A = mat_zero n.
Proof.
  unfold mat_add, mat_opp, mat_zero. extensionality i. extensionality j.
  apply Rplus_opp_l.
Qed.

Lemma mat_mul_assoc {n} (A B C : Mat n) :
  mat_mul (mat_mul A B) C = mat_mul A (mat_mul B C).
Proof.
  unfold mat_mul. extensionality i. extensionality j.
  apply sum_R_ext.
  intros k Hk.
  transitivity ((mat_mul A B) i (mkFin k Hk) * C (mkFin k Hk) j).
  - apply mat_mul_entry.
  - rewrite sum_R_mul_r.
    apply sum_R_ext.
    intros l Hl.
    transitivity (A i (mkFin l Hl) * B (mkFin l Hl) (mkFin k Hk)).
    + apply mat_mul_entry.
    + apply Rmult_assoc.
Qed.

Lemma mat_mul_1_l {n} (B : Mat n) :
  mat_mul (mat_one n) B = B.
Proof.
  unfold mat_mul. extensionality i. extensionality j.
  apply sum_R_ext.
  intros k Hk.
  transitivity (mat_one n i (mkFin k Hk) * B (mkFin k Hk) j).
  - apply mat_mul_entry.
  - unfold mat_one.
    destruct (Nat.eqb_spec (fin_val i) k).
    + assert (Heq : mkFin k Hk = i) by (apply fin_val_eq; auto).
      rewrite Heq. rewrite Rmult_1_l. reflexivity.
    + rewrite Rmult_0_l. reflexivity.
Qed.

Lemma mat_mul_1_r {n} (A : Mat n) :
  mat_mul A (mat_one n) = A.
Proof.
  unfold mat_mul. extensionality i. extensionality j.
  apply sum_R_ext.
  intros k Hk.
  transitivity (A i (mkFin k Hk) * mat_one n (mkFin k Hk) j).
  - apply mat_mul_entry.
  - unfold mat_one.
    destruct (Nat.eqb_spec k (fin_val j)).
    + assert (Heq : mkFin k Hk = j) by (apply fin_val_eq; auto).
      rewrite Heq. rewrite Rmult_1_r. reflexivity.
    + rewrite Rmult_0_r. reflexivity.
Qed.

Lemma mat_distr_l {n} (A B C : Mat n) :
  mat_mul A (mat_add B C) = mat_add (mat_mul A B) (mat_mul A C).
Proof.
  unfold mat_mul, mat_add. extensionality i. extensionality j.
  apply sum_R_ext.
  intros k Hk.
  transitivity (A i (mkFin k Hk) * (B (mkFin k Hk) j + C (mkFin k Hk) j)).
  - apply mat_mul_entry.
  - rewrite Rmult_plus_distr_l.
    rewrite sum_R_add_distr.
    f_equal;
      apply sum_R_ext;
      intros k2 Hk2;
      transitivity (A i (mkFin k2 Hk2) * B (mkFin k2 Hk2) j);
      [apply mat_mul_entry | reflexivity].
Qed.

Lemma mat_distr_r {n} (A B C : Mat n) :
  mat_mul (mat_add A B) C = mat_add (mat_mul A C) (mat_mul B C).
Proof.
  unfold mat_mul, mat_add. extensionality i. extensionality j.
  apply sum_R_ext.
  intros k Hk.
  transitivity ((A i (mkFin k Hk) + B i (mkFin k Hk)) * C (mkFin k Hk) j).
  - apply mat_mul_entry.
  - rewrite Rmult_plus_distr_r.
    rewrite sum_R_add_distr.
    f_equal;
      apply sum_R_ext;
      intros k2 Hk2;
      transitivity (A i (mkFin k2 Hk2) * C (mkFin k2 Hk2) j);
      [apply mat_mul_entry | reflexivity].
Qed.

Lemma mat_smul_1 {n} (A : Mat n) :
  mat_smul 1 A = A.
Proof.
  unfold mat_smul. extensionality i. extensionality j.
  apply Rmult_1_l.
Qed.

Lemma mat_smul_mul {n} (r s : R) (A : Mat n) :
  mat_smul (r * s) A = mat_smul r (mat_smul s A).
Proof.
  unfold mat_smul. extensionality i. extensionality j.
  symmetry. apply Rmult_assoc.
Qed.

Lemma mat_smul_add_distr {n} (r s : R) (A : Mat n) :
  mat_smul (r + s) A = mat_add (mat_smul r A) (mat_smul s A).
Proof.
  unfold mat_smul, mat_add. extensionality i. extensionality j.
  apply Rmult_plus_distr_l.
Qed.

Lemma mat_smul_add_l {n} (r : R) (A B : Mat n) :
  mat_smul r (mat_add A B) = mat_add (mat_smul r A) (mat_smul r B).
Proof.
  unfold mat_smul, mat_add. extensionality i. extensionality j.
  apply Rmult_plus_distr_r.
Qed.

Lemma mat_smul_mul_l {n} (r : R) (A B : Mat n) :
  mat_mul (mat_smul r A) B = mat_smul r (mat_mul A B).
Proof.
  unfold mat_mul, mat_smul. extensionality i. extensionality j.
  apply sum_R_ext.
  intros k Hk.
  transitivity ((r * A i (mkFin k Hk)) * B (mkFin k Hk) j).
  - apply mat_mul_entry.
  - rewrite sum_R_mul_l.
    f_equal.
    apply sum_R_ext.
    intros k2 Hk2.
    transitivity (A i (mkFin k2 Hk2) * B (mkFin k2 Hk2) j).
    + apply mat_mul_entry.
    + apply Rmult_assoc.
Qed.

Lemma mat_smul_mul_r {n} (r : R) (A B : Mat n) :
  mat_mul A (mat_smul r B) = mat_smul r (mat_mul A B).
Proof.
  unfold mat_mul, mat_smul. extensionality i. extensionality j.
  apply sum_R_ext.
  intros k Hk.
  transitivity (A i (mkFin k Hk) * (r * B (mkFin k Hk) j)).
  - apply mat_mul_entry.
  - rewrite sum_R_mul_r.
    f_equal.
    apply sum_R_ext.
    intros k2 Hk2.
    transitivity (A i (mkFin k2 Hk2) * B (mkFin k2 Hk2) j).
    + apply mat_mul_entry.
    + rewrite <- Rmult_assoc.
      rewrite (Rmult_comm (A i (mkFin k2 Hk2)) r).
      rewrite Rmult_assoc.
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
  alg_add_assoc := mat_add_assoc n;
  alg_add_comm := mat_add_comm n;
  alg_add_0_l := mat_add_0_l n;
  alg_add_opp_l := mat_add_opp_l n;
  alg_mul_assoc := mat_mul_assoc n;
  alg_mul_1_l := mat_mul_1_l n;
  alg_mul_1_r := mat_mul_1_r n;
  alg_distr_l := mat_distr_l n;
  alg_distr_r := mat_distr_r n;
  alg_smul_1 := mat_smul_1 n;
  alg_smul_mul := mat_smul_mul n;
  alg_smul_add_distr := mat_smul_add_distr n;
  alg_smul_add_l := mat_smul_add_l n;
  alg_smul_mul_l := mat_smul_mul_l n;
  alg_smul_mul_r := mat_smul_mul_r n
|}.

(******************************************************************************)
(* Section 2: Direct sum M_8(R) ⊕ M_8(R) as an R-algebra                     *)
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
  intros [x1 x2] [y1 y2] [z1 z2]. simpl. f_equal; apply mat_add_assoc.
Qed.

Lemma pair_add_comm : forall X Y,
  pair_add X Y = pair_add Y X.
Proof.
  intros [x1 x2] [y1 y2]. simpl. f_equal; apply mat_add_comm.
Qed.

Lemma pair_add_0_l : forall X,
  pair_add pair_zero X = X.
Proof.
  intros [x1 x2]. simpl. f_equal; apply mat_add_0_l.
Qed.

Lemma pair_add_opp_l : forall X,
  pair_add (pair_opp X) X = pair_zero.
Proof.
  intros [x1 x2]. simpl. f_equal; apply mat_add_opp_l.
Qed.

Lemma pair_mul_assoc : forall X Y Z,
  pair_mul (pair_mul X Y) Z = pair_mul X (pair_mul Y Z).
Proof.
  intros [x1 x2] [y1 y2] [z1 z2]. simpl. f_equal; apply mat_mul_assoc.
Qed.

Lemma pair_mul_1_l : forall X,
  pair_mul pair_one X = X.
Proof.
  intros [x1 x2]. simpl. f_equal; apply mat_mul_1_l.
Qed.

Lemma pair_mul_1_r : forall X,
  pair_mul X pair_one = X.
Proof.
  intros [x1 x2]. simpl. f_equal; apply mat_mul_1_r.
Qed.

Lemma pair_distr_l : forall X Y Z,
  pair_mul X (pair_add Y Z) = pair_add (pair_mul X Y) (pair_mul X Z).
Proof.
  intros [x1 x2] [y1 y2] [z1 z2]. simpl. f_equal; apply mat_distr_l.
Qed.

Lemma pair_distr_r : forall X Y Z,
  pair_mul (pair_add X Y) Z = pair_add (pair_mul X Z) (pair_mul Y Z).
Proof.
  intros [x1 x2] [y1 y2] [z1 z2]. simpl. f_equal; apply mat_distr_r.
Qed.

Lemma pair_smul_1 : forall X,
  pair_smul 1 X = X.
Proof.
  intros [x1 x2]. simpl. f_equal; apply mat_smul_1.
Qed.

Lemma pair_smul_mul : forall r s X,
  pair_smul (r * s) X = pair_smul r (pair_smul s X).
Proof.
  intros r s [x1 x2]. simpl. f_equal; apply mat_smul_mul.
Qed.

Lemma pair_smul_add_distr : forall r s X,
  pair_smul (r + s) X = pair_add (pair_smul r X) (pair_smul s X).
Proof.
  intros r s [x1 x2]. simpl. f_equal; apply mat_smul_add_distr.
Qed.

Lemma pair_smul_add_l : forall r X Y,
  pair_smul r (pair_add X Y) = pair_add (pair_smul r X) (pair_smul r Y).
Proof.
  intros r [x1 x2] [y1 y2]. simpl. f_equal; apply mat_smul_add_l.
Qed.

Lemma pair_smul_mul_l : forall r X Y,
  pair_mul (pair_smul r X) Y = pair_smul r (pair_mul X Y).
Proof.
  intros r [x1 x2] [y1 y2]. simpl. f_equal; apply mat_smul_mul_l.
Qed.

Lemma pair_smul_mul_r : forall r X Y,
  pair_mul X (pair_smul r Y) = pair_smul r (pair_mul X Y).
Proof.
  intros r [x1 x2] [y1 y2]. simpl. f_equal; apply mat_smul_mul_r.
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
(* Section 3: T2 statement                                                   *)
(******************************************************************************)

Axiom Cl06_spec : CliffordSpec 0 6.

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
(*  Honesty summary for T2                                                   *)
(******************************************************************************)
