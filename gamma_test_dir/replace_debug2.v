From Coq Require Import Reals Lia Lra FunctionalExtensionality.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Lemma test (n : nat) (a : R) (X Y : Mat n) :
  mat_add X Y = mat_zero n ->
  mat_add (mat_smul a X) (mat_smul a Y) = mat_zero n.
Proof.
  intros H.
  replace (mat_add (mat_smul a X) (mat_smul a Y))
    with (mat_smul a (mat_add X Y)).
  - idtac "After replace:";
    match goal with [ |- ?G ] => idtac G end.
    rewrite H. apply mat_smul_zero_r.
  - extensionality i. extensionality j.
    unfold mat_add, mat_smul.
    lra.
Qed.
