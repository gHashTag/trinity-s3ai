From Coq Require Import Reals.
Open Scope R_scope.

Lemma test_ring_neg (a b : R) (x : R) :
  (-(a * a)) * x + (-(b)) * x = (-(a * a + b)) * x.
Proof.
  ring.
Qed.
