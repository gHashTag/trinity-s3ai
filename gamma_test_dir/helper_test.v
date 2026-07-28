From Coq Require Import Reals Lia Lra FunctionalExtensionality.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Lemma mat_smul_opp (n : nat) (a : R) (A : Mat n) :
  mat_smul a (mat_opp A) = mat_opp (mat_smul a A).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul, mat_opp. extensionality i. extensionality j.
    ring.
Qed.

Lemma mat_smul_opp_r (n : nat) (a : R) (A : Mat n) :
  mat_smul (- a) A = mat_opp (mat_smul a A).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul, mat_opp. extensionality i. extensionality j.
    ring.
Qed.

Lemma test_helper (n : nat) (a : R) :
  mat_smul a (mat_smul a (mat_opp (mat_one n))) = mat_smul (- (a * a)) (mat_one n).
Proof.
  rewrite (mat_smul_opp n a (mat_one n)).
  rewrite (mat_smul_opp n a (mat_smul a (mat_one n))).
  rewrite <- (mat_smul_mul n a a (mat_one n)).
  rewrite (mat_smul_opp_r n (a * a) (mat_one n)).
  reflexivity.
Qed.
