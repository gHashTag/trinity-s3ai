From Coq Require Import Reals Lia Lra FunctionalExtensionality.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Lemma mat_add_rearrange_5 (A B C D E F G H I J : Mat 8) :
  mat_add (mat_add A (mat_add B (mat_add C (mat_add D E))))
          (mat_add F (mat_add G (mat_add H (mat_add I J))))
  = mat_add (mat_add A F) (mat_add (mat_add B G) (mat_add (mat_add C H) (mat_add (mat_add D I) (mat_add E J)))).
Proof.
  extensionality i. extensionality j.
  unfold mat_add.
  lra.
Qed.

Lemma mat_smul_add_l_sym (n : nat) (r : R) (A B : Mat n) :
  mat_add (mat_smul r A) (mat_smul r B) = mat_smul r (mat_add A B).
Proof.
  symmetry. apply mat_smul_add_l.
Qed.

Lemma test_anticomm (v : Vec 6) :
  mat_add (mat_smul (v (mkFin 0 (Nat.lt_0_succ 5))) (mat_one 8))
          (mat_smul (v (mkFin 0 (Nat.lt_0_succ 5))) (mat_one 8))
  = mat_smul (v (mkFin 0 (Nat.lt_0_succ 5))) (mat_add (mat_one 8) (mat_one 8)).
Proof.
  apply mat_smul_add_l_sym.
Qed.
