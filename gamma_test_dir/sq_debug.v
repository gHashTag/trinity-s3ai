From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Lemma mat_smul_opp_r (n : nat) (a : R) (A : Mat n) :
  mat_smul (- a) A = mat_opp (mat_smul a A).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul, mat_opp. extensionality i. extensionality j.
    ring.
Qed.

Lemma mat_smul_opp (n : nat) (a : R) (A : Mat n) :
  mat_smul a (mat_opp A) = mat_opp (mat_smul a A).
Proof.
  destruct n as [|n'].
  - apply mat0_eq.
  - unfold mat_smul, mat_opp. extensionality i. extensionality j.
    ring.
Qed.

Lemma mat_smul_smul_opp_one (n : nat) (a : R) :
  mat_smul a (mat_smul a (mat_opp (mat_one n))) = mat_smul (- (a * a)) (mat_one n).
Proof.
  rewrite (mat_smul_opp n a (mat_one n)).
  rewrite (mat_smul_opp n a (mat_smul a (mat_one n))).
  rewrite <- (mat_smul_mul n a a (mat_one n)).
  rewrite (mat_smul_opp_r n (a * a) (mat_one n)).
  reflexivity.
Qed.

Lemma sq_expand_general (n : nat) (a : R) (g A : Mat n) :
  mat_mul g g = mat_opp (mat_one n) ->
  mat_add (mat_mul g A) (mat_mul A g) = mat_zero n ->
  mat_mul (mat_add (mat_smul a g) A) (mat_add (mat_smul a g) A) =
  mat_add (mat_smul (- (a * a)) (mat_one n)) (mat_mul A A).
Proof.
  intros Hg2 Hcomm.
  rewrite (mat_distr_l n (mat_add (mat_smul a g) A) (mat_smul a g) A).
  rewrite (mat_distr_r n (mat_smul a g) A (mat_smul a g)).
  rewrite (mat_distr_r n (mat_smul a g) A A).
  rewrite (mat_smul_mul_l n a g (mat_smul a g)).
  rewrite (mat_smul_mul_r n a g g).
  rewrite Hg2.
  rewrite (mat_smul_smul_opp_one n a).
  rewrite (mat_smul_mul_l n a g A).
  rewrite (mat_smul_mul_r n a A g).
  replace (mat_add (mat_add (mat_smul (- (a * a)) (mat_one n)) (mat_smul a (mat_mul A g)))
            (mat_add (mat_smul a (mat_mul g A)) (mat_mul A A)))
    with (mat_add (mat_smul (- (a * a)) (mat_one n)) (mat_mul A A)).
  - reflexivity.
  - extensionality i. extensionality j.
    assert (Hscalar : forall i0 j0, mat_mul g A i0 j0 + mat_mul A g i0 j0 = 0).
    { intros i0 j0.
      assert (H : mat_add (mat_mul g A) (mat_mul A g) i0 j0 = mat_zero n i0 j0).
      { rewrite Hcomm. reflexivity. }
      unfold mat_add, mat_zero in H.
      exact H. }
    unfold mat_add, mat_smul.
    specialize (Hscalar i j).
    nra.
Qed.
