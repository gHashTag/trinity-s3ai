From Coq Require Import Reals Lra.
Open Scope R_scope.

Definition f (n : nat) : R := match n with | O => 0 | S _ => 1 end.

Lemma test_ring_match (n : nat) (a : R) :
  a * f n + a * f n = a * (f n + f n).
Proof.
  ring.
Qed.
