From Coq Require Import Reals Lia Lra FunctionalExtensionality.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Definition gamma_1 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 1 => -1 | 1, 0 => 1 | 2, 3 => -1 | 3, 2 => 1
  | 4, 5 => -1 | 5, 4 => 1 | 6, 7 => -1 | 7, 6 => 1
  | _, _ => 0 end.

Definition gamma_2 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 3 => -1 | 1, 2 => -1 | 2, 1 => 1 | 3, 0 => 1
  | 4, 7 => -1 | 5, 6 => -1 | 6, 5 => 1 | 7, 4 => 1
  | _, _ => 0 end.

Lemma gamma_1_gamma_2_anticomm :
  mat_add (mat_mul gamma_1 gamma_2) (mat_mul gamma_2 gamma_1) = mat_zero 8.
Proof.
  extensionality i. extensionality j.
  destruct i as [vi Hi]. destruct j as [vj Hj].
  destruct vi; try lia;
    destruct vj; try lia;
    compute;
    idtac "GOAL:";
    match goal with [ |- ?G ] => idtac G end.
Abort.
