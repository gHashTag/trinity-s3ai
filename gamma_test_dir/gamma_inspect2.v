From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Definition f0 : Fin 8. refine (mkFin 0 _). lia. Defined.

Definition mat_mul_8 (A B : Mat 8) : Mat 8 := fun i j =>
  A i f0 * B f0 j +
  A i (mkFin 1 _) * B (mkFin 1 _) j +
  A i (mkFin 2 _) * B (mkFin 2 _) j +
  A i (mkFin 3 _) * B (mkFin 3 _) j +
  A i (mkFin 4 _) * B (mkFin 4 _) j +
  A i (mkFin 5 _) * B (mkFin 5 _) j +
  A i (mkFin 6 _) * B (mkFin 6 _) j +
  A i (mkFin 7 _) * B (mkFin 7 _) j.

Definition gamma_1 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 1 => -1 | 1, 0 => 1 | 2, 3 => -1 | 3, 2 => 1
  | 4, 5 => -1 | 5, 4 => 1 | 6, 7 => -1 | 7, 6 => 1
  | _, _ => 0
  end.

Lemma inspect :
  mat_mul_8 gamma_1 gamma_1 f0 f0 = mat_opp (mat_one 8) f0 f0.
Proof.
  unfold mat_mul_8, gamma_1, mat_opp, mat_one.
  vm_compute.
  Show Goal.
Abort.
