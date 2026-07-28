From Coq Require Import Reals Lia Lra FunctionalExtensionality.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Local Lemma lt_0_6 : (0 < 6)%nat. Proof. lia. Qed.
Local Lemma lt_1_6 : (1 < 6)%nat. Proof. lia. Qed.
Local Lemma lt_2_6 : (2 < 6)%nat. Proof. lia. Qed.
Local Lemma lt_3_6 : (3 < 6)%nat. Proof. lia. Qed.
Local Lemma lt_4_6 : (4 < 6)%nat. Proof. lia. Qed.
Local Lemma lt_5_6 : (5 < 6)%nat. Proof. lia. Qed.

Definition e1 := mkFin 0 lt_0_6.
Definition e2 := mkFin 1 lt_1_6.
Definition e3 := mkFin 2 lt_2_6.
Definition e4 := mkFin 3 lt_3_6.
Definition e5 := mkFin 4 lt_4_6.
Definition e6 := mkFin 5 lt_5_6.

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
Definition gamma_3 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 6 => -1 | 1, 7 => 1 | 2, 4 => 1 | 3, 5 => -1
  | 4, 2 => -1 | 5, 3 => 1 | 6, 0 => 1 | 7, 1 => -1
  | _, _ => 0 end.
Definition gamma_4 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 4 => -1 | 1, 5 => 1 | 2, 6 => -1 | 3, 7 => 1
  | 4, 0 => 1 | 5, 1 => -1 | 6, 2 => 1 | 7, 3 => -1
  | _, _ => 0 end.
Definition gamma_5 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 7 => -1 | 1, 6 => -1 | 2, 5 => -1 | 3, 4 => -1
  | 4, 3 => 1 | 5, 2 => 1 | 6, 1 => 1 | 7, 0 => 1
  | _, _ => 0 end.
Definition gamma_6 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 5 => -1 | 1, 4 => -1 | 2, 7 => 1 | 3, 6 => 1
  | 4, 1 => 1 | 5, 0 => 1 | 6, 3 => -1 | 7, 2 => -1
  | _, _ => 0 end.

Definition i_06 (v : Vec 6) : Mat 8 :=
  mat_add (mat_smul (v e1) gamma_1)
    (mat_add (mat_smul (v e2) gamma_2)
      (mat_add (mat_smul (v e3) gamma_3)
        (mat_add (mat_smul (v e4) gamma_4)
          (mat_add (mat_smul (v e5) gamma_5)
            (mat_smul (v e6) gamma_6))))).

Lemma test_goal (v : Vec 6) :
  mat_mul (i_06 v) (i_06 v) = mat_smul (-(v e1^2 + v e2^2 + v e3^2 + v e4^2 + v e5^2 + v e6^2)) (mat_one 8).
Proof.
  extensionality i. extensionality j.
  destruct i as [vi Hi]. destruct j as [vj Hj].
  destruct vi; try lia;
    destruct vj; try lia;
    unfold i_06, e1, e2, e3, e4, e5, e6, mat_mul, mat_mul_aux, sum_R, mat_smul, mat_one, mat_add, Rsqr;
    vm_compute;
    lra.
Qed.
