From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Lemma test_ring (a b c : R) :
  (- (a * a)) * b + (- c) * b = (- (a * a + c)) * b.
Proof.
  ring.
Qed.
