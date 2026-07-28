From Coq Require Import Reals Lia.
Open Scope R_scope.

Lemma test_destruct (n : nat) :
  n = n.
Proof.
  destruct n as [|n1].
  - reflexivity.
  - reflexivity.
Qed.
