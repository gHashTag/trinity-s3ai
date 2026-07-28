From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Definition gamma_1 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 1 => -1 | 1, 0 => 1 | 2, 3 => -1 | 3, 2 => 1
  | 4, 5 => -1 | 5, 4 => 1 | 6, 7 => -1 | 7, 6 => 1
  | _, _ => 0
  end.

Lemma gamma_1_sq_fast :
  mat_mul gamma_1 gamma_1 = mat_opp (mat_one 8).
Proof.
  extensionality i. extensionality j.
  unfold gamma_1, mat_mul, mat_mul_aux, mat_one, mat_opp, fin_nat.
  simpl.
  destruct (fin_val i) eqn:Hi; try lia.
  destruct (fin_val j) eqn:Hj; try lia.
  simpl.
  ring.
Qed.
