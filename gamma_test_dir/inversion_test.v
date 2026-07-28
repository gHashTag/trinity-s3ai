From Coq Require Import Reals Lia.
From CliffordCl8 Require Import CliffordAlgebra.

Lemma test_inversion (x : nat) (H : (x < 1)%nat) :
  x = 0.
Proof.
  destruct x.
  - reflexivity.
  - inversion H.
Qed.
