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

Lemma anticomm_sum_step (n : nat) (a : R) (g A : Mat n) :
  mat_add (mat_mul g A) (mat_mul A g) = mat_zero n ->
  mat_add (mat_mul g (mat_smul a A)) (mat_mul (mat_smul a A) g) = mat_zero n.
Proof.
  intros H.
  rewrite (mat_smul_mul_r n a g A).
  rewrite (mat_smul_mul_l n a A g).
  replace (mat_add (mat_smul a (mat_mul g A)) (mat_smul a (mat_mul A g)))
    with (mat_smul a (mat_add (mat_mul g A) (mat_mul A g))).
  - rewrite H.
    unfold mat_smul, mat_zero. extensionality i. extensionality j. apply Rmult_0_r.
  - extensionality i. extensionality j.
    unfold mat_add, mat_smul.
    lra.
Qed.

Lemma cl_sq_sum (n : nat) (m : nat) (coeffs : nat -> R) (gens : nat -> Mat n) :
  (forall i, (i < m)%nat -> mat_mul (gens i) (gens i) = mat_opp (mat_one n)) ->
  (forall i j, (i < m)%nat -> (j < m)%nat -> i <> j ->
    mat_add (mat_mul (gens i) (gens j)) (mat_mul (gens j) (gens i)) = mat_zero n) ->
  mat_mul (sum_R m (fun i => mat_smul (coeffs i) (gens i)))
          (sum_R m (fun i => mat_smul (coeffs i) (gens i))) =
  mat_smul (- sum_R m (fun i => coeffs i * coeffs i)) (mat_one n).
Proof.
  induction m as [|m IH]; intros Hsq Hcomm.
  - simpl. unfold mat_mul. simpl.
    extensionality i. extensionality j.
    unfold mat_mul_aux, mat_smul, mat_zero. simpl.
    rewrite Rmult_0_l. reflexivity.
  - simpl sum_R at 1 3.
    rewrite (sq_expand_general n (coeffs m) (gens m) (sum_R m (fun i => mat_smul (coeffs i) (gens i)))).
    + rewrite IH.
      * rewrite (mat_smul_opp_r n (coeffs m * coeffs m) (mat_one n)).
        rewrite (mat_smul_mul n (coeffs m) (coeffs m) (mat_one n)).
        replace (mat_add (mat_smul (- (coeffs m * coeffs m)) (mat_one n))
                  (mat_smul (- sum_R m (fun i : nat => coeffs i * coeffs i)) (mat_one n)))
          with (mat_smul (- (coeffs m * coeffs m + sum_R m (fun i : nat => coeffs i * coeffs i))) (mat_one n)).
        -- reflexivity.
        -- extensionality i. extensionality j.
           unfold mat_add, mat_smul.
           rewrite Ropp_plus_distr.
           lra.
      * intros i Hi. apply Hsq. lia.
      * intros i j Hi Hj Hneq. apply Hcomm; lia.
    + apply Hsq. lia.
    + induction m as [|m' IHm'].
      * simpl. rewrite mat_mul_zero_l. rewrite mat_mul_zero_r. apply mat_add_0_l.
      * simpl sum_R at 1 3.
        rewrite (mat_distr_l n (gens (S m')) (mat_smul (coeffs m') (gens m')) (sum_R m' _)).
        rewrite (mat_distr_r n (mat_smul (coeffs m') (gens m')) (sum_R m' _) (gens (S m'))).
        rewrite (anticomm_sum_step n (coeffs m') (gens (S m')) (gens m')).
        -- replace (mat_add (mat_add (mat_mul (gens (S m')) (mat_smul (coeffs m') (gens m'))) (mat_mul (gens (S m')) (sum_R m' _)))
                      (mat_add (mat_mul (mat_smul (coeffs m') (gens m')) (gens (S m'))) (mat_mul (sum_R m' _) (gens (S m')))))
             with (mat_add (mat_mul (gens (S m')) (mat_smul (coeffs m') (gens m'))) (mat_add (mat_mul (mat_smul (coeffs m') (gens m')) (gens (S m')))
                      (mat_add (mat_mul (gens (S m')) (sum_R m' _)) (mat_mul (sum_R m' _) (gens (S m')))))).
           ++ rewrite IHm'.
              ** reflexivity.
              ** intros i Hi. apply Hcomm; lia.
              ** intros i j Hi Hj Hneq. apply Hcomm; lia.
           ++ extensionality i. extensionality j.
              unfold mat_add.
              lra.
        -- apply Hcomm; lia.
Qed.
