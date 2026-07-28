From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Lemma test_ring (a : R) (m : nat) (coeffs : nat -> R) :
  (- a) * 1 + (- sum_R m (fun i => coeffs i * coeffs i)) * 1 = (- (a + sum_R m (fun i => coeffs i * coeffs i))) * 1.
Proof.
  ring.
Qed.
