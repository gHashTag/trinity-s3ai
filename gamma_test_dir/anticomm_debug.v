From Coq Require Import Reals Lia Lra FunctionalExtensionality.
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
  replace (mat_add (mat_smul a (mat_mul g A)) (mat_smul a (mat_mul A g)))
    with (mat_smul a (mat_add (mat_mul g A) (mat_mul A g))).
  - rewrite H.
    unfold mat_smul, mat_zero. extensionality i. extensionality j. apply Rmult_0_r.
  - extensionality i. extensionality j.
    unfold mat_add, mat_smul.
    lra.
Qed.
