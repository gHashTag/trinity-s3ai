From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Lemma test_ring (a : R) (m : nat) (coeffs : nat -> R) (n : nat) (i j : Fin n) :
  (-(a * a)) * mat_one n i j + (-(sum_R m (fun k => coeffs k * coeffs k))) * mat_one n i j =
  (-(a * a + sum_R m (fun k => coeffs k * coeffs k))) * mat_one n i j.
Proof.
  ring.
Qed.
