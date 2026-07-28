From Coq Require Import Reals.
Open Scope R_scope.

Definition g (n : nat) : R := if Nat.eqb n 0 then 1 else 0.

Lemma test_ring_if (n : nat) (a b : R) :
  a * g n + b * g n = (a + b) * g n.
Proof.
  ring.
Qed.
