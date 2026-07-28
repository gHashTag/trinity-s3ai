From Coq Require Import Reals Lia.
Open Scope R_scope.

Lemma test_intro (n : nat) :
  n = n.
Proof.
  intros.
  reflexivity.
Qed.
