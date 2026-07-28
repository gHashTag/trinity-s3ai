From Coq Require Import Reals Lia Lra FunctionalExtensionality.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Lemma anticomm_sum_step (n : nat) (a : R) (g A : Mat n) :
  mat_add (mat_mul g A) (mat_mul A g) = mat_zero n ->
  mat_add (mat_mul g (mat_smul a A)) (mat_mul (mat_smul a A) g) = mat_zero n.
Proof.
  intros H.
  rewrite (mat_smul_mul_r n a A g).
  rewrite (mat_smul_mul_l n a g A).
  idtac "Before replace:";
  match goal with [ |- ?G ] => idtac G end.
  replace (mat_add (mat_smul a (mat_mul g A)) (mat_smul a (mat_mul A g)))
    with (mat_smul a (mat_add (mat_mul g A) (mat_mul A g))).
  - idtac "After replace:";
    match goal with [ |- ?G ] => idtac G end.
    rewrite H. apply mat_smul_zero_r.
  - extensionality i. extensionality j.
    unfold mat_add, mat_smul.
    lra.
Qed.
