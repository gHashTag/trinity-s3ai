From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Definition f0 : Fin 8. refine (mkFin 0 _). lia. Defined.
Definition f1 : Fin 8. refine (mkFin 1 _). lia. Defined.

Definition gamma_1 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 1 => -1 | 1, 0 => 1 | 2, 3 => -1 | 3, 2 => 1
  | 4, 5 => -1 | 5, 4 => 1 | 6, 7 => -1 | 7, 6 => 1
  | _, _ => 0
  end.

Lemma test_ring :
  gamma_1 f0 f1 = -1.
Proof.
  unfold gamma_1.
  ring.
Qed.
