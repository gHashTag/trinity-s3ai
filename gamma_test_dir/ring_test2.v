From Coq Require Import Reals Lia Lra.
From CliffordCl8 Require Import CliffordAlgebra.
Open Scope R_scope.

Local Lemma lt_0_6 : (0 < 6)%nat. Proof. lia. Qed.
Local Lemma lt_1_6 : (1 < 6)%nat. Proof. lia. Qed.

Definition e1 := mkFin 0 lt_0_6.
Definition e2 := mkFin 1 lt_1_6.

Lemma test_ring2 (v : Vec 6) :
  (v e1 * 1 + v e2 * 0) * (v e1 * 1 + v e2 * 0) + (v e1 * 0 + v e2 * 1) * (v e1 * 0 + v e2 * 1) =
  v e1 ^ 2 + v e2 ^ 2.
Proof.
  unfold Rsqr.
  ring.
Qed.
