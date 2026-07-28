From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

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
  lra.
Qed.
