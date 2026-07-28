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
  unfold gamma_1, mat_mul, mat_mul_aux, mat_one, mat_opp.
  simpl.
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
