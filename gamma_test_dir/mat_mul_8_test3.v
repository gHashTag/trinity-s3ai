From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz Program.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

(* Explicit Fin 8 elements *)
Program Definition f0 : Fin 8 := mkFin 0 _.
Next Obligation. lia. Qed.
Program Definition f1 : Fin 8 := mkFin 1 _.
Next Obligation. lia. Qed.
Program Definition f2 : Fin 8 := mkFin 2 _.
Next Obligation. lia. Qed.
Program Definition f3 : Fin 8 := mkFin 3 _.
Next Obligation. lia. Qed.
Program Definition f4 : Fin 8 := mkFin 4 _.
Next Obligation. lia. Qed.
Program Definition f5 : Fin 8 := mkFin 5 _.
Next Obligation. lia. Qed.
Program Definition f6 : Fin 8 := mkFin 6 _.
Next Obligation. lia. Qed.
Program Definition f7 : Fin 8 := mkFin 7 _.
Next Obligation. lia. Qed.

Definition mat_mul_8 (A B : Mat 8) : Mat 8 := fun i j =>
  A i f0 * B f0 j +
  A i f1 * B f1 j +
  A i f2 * B f2 j +
  A i f3 * B f3 j +
  A i f4 * B f4 j +
  A i f5 * B f5 j +
  A i f6 * B f6 j +
  A i f7 * B f7 j.

Lemma mat_mul_8_eq : forall A B, mat_mul_8 A B = mat_mul A B.
Proof.
  intros A B.
  extensionality i. extensionality j.
  unfold mat_mul_8, mat_mul, mat_mul_aux, fin_nat.
  simpl. rewrite sum_R_S. rewrite sum_R_S. rewrite sum_R_S. rewrite sum_R_S.
  rewrite sum_R_S. rewrite sum_R_S. rewrite sum_R_S.
  simpl.
  ring.
Qed.

Definition gamma_1 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 1 => -1 | 1, 0 => 1 | 2, 3 => -1 | 3, 2 => 1
  | 4, 5 => -1 | 5, 4 => 1 | 6, 7 => -1 | 7, 6 => 1
  | _, _ => 0
  end.

Lemma gamma_1_sq_fast :
  mat_mul_8 gamma_1 gamma_1 = mat_opp (mat_one 8).
Proof.
  extensionality i. extensionality j.
  unfold mat_mul_8, gamma_1, mat_one, mat_opp.
  destruct (fin_val i) eqn:Hi;
    try (destruct n as [|n1]; try lia;
         destruct n1 as [|n2]; try lia;
         destruct n2 as [|n3]; try lia;
         destruct n3 as [|n4]; try lia;
         destruct n4 as [|n5]; try lia;
         destruct n5 as [|n6]; try lia;
         destruct n6 as [|n7]; try lia;
         destruct n7 as [|n8]; try lia);
  destruct (fin_val j) eqn:Hj;
    try (destruct n0 as [|n1]; try lia;
         destruct n1 as [|n2]; try lia;
         destruct n2 as [|n3]; try lia;
         destruct n3 as [|n4]; try lia;
         destruct n4 as [|n5]; try lia;
         destruct n5 as [|n6]; try lia;
         destruct n6 as [|n7]; try lia;
         destruct n7 as [|n8]; try lia);
  simpl; ring.
Qed.
