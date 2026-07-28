From Coq Require Import Reals Lia Lra FunctionalExtensionality.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Lemma test_replace (n : nat) (a : R) (g A : Mat n) :
  mat_add (mat_smul a (mat_mul g A)) (mat_add (mat_smul a (mat_mul A g)) (mat_mul A A)) =
  mat_add (mat_smul a (mat_add (mat_mul g A) (mat_mul A g))) (mat_mul A A).
Proof.
  extensionality i. extensionality j.
  unfold mat_add, mat_smul.
  lra.
Qed.
