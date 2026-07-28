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

Definition gamma_2 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 3 => -1 | 1, 2 => -1 | 2, 1 => 1 | 3, 0 => 1
  | 4, 7 => -1 | 5, 6 => -1 | 6, 5 => 1 | 7, 4 => 1
  | _, _ => 0
  end.

Lemma gamma_1_sq :
  mat_mul gamma_1 gamma_1 = mat_opp (mat_one 8).
Proof.
  apply functional_extensionality; intros i.
  apply functional_extensionality; intros j.
  unfold mat_mul, mat_mul_aux, gamma_1, mat_opp, mat_one, fin_nat.
  vm_compute.
Qed.

Lemma gamma_1_anticomm_gamma_2 :
  mat_add (mat_mul gamma_1 gamma_2) (mat_mul gamma_2 gamma_1) = mat_zero 8.
Proof.
  apply functional_extensionality; intros i.
  apply functional_extensionality; intros j.
  unfold mat_mul, mat_mul_aux, gamma_1, gamma_2, mat_add, mat_zero, fin_nat.
  vm_compute.
Qed.
