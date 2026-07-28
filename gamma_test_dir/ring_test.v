From Coq Require Import Reals Lia Lra.
From CliffordCl8 Require Import CliffordAlgebra.
Open Scope R_scope.

Local Lemma lt_0_6 : (0 < 6)%nat. Proof. lia. Qed.

Definition e1 := mkFin 0 lt_0_6.

Lemma test_ring (v : Vec 6) :
  v e1 * v e1 = v e1 ^ 2.
Proof.
  unfold Rsqr.
  ring.
Qed.
