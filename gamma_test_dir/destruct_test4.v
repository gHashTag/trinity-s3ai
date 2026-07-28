From Coq Require Import Reals Lia.
Open Scope R_scope.

Lemma test_destruct (n : nat) :
  n = n.
Proof.
  destruct n as [|n1].
  - reflexivity.
  - destruct n1 as [|n2].
    + reflexivity.
    + destruct n2 as [|n3].
      * reflexivity.
      * destruct n3 as [|n4].
        { reflexivity. }
        { reflexivity. }
Qed.
