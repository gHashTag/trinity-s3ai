From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Fixpoint mat_sum {n} (k : nat) (f : nat -> Mat n) : Mat n :=
  match k with
  | O => mat_zero n
  | S k' => mat_add (f k') (mat_sum k' f)
  end.

Lemma mat_sum_S {n} (m : nat) (f : nat -> Mat n) :
  mat_sum (S m) f = mat_add (f m) (mat_sum m f).
Proof. reflexivity. Qed.

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
    assert (Hscalar : mat_mul g A i j + mat_mul A g i j = 0).
    { assert (H : mat_add (mat_mul g A) (mat_mul A g) i j = mat_zero n i j).
      { rewrite Hcomm. reflexivity. }
      unfold mat_add, mat_zero in H.
      exact H. }
    unfold mat_add, mat_smul.
    assert (Hag : mat_mul A g i j = - mat_mul g A i j).
    { apply Rminus_diag_uniq_sym. lra. }
    rewrite Hag.
    field.
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

Lemma mat_sum_anticomm {n} (g : Mat n) (m : nat) (f : nat -> Mat n) :
  (forall i, (i < m)%nat -> mat_add (mat_mul g (f i)) (mat_mul (f i) g) = mat_zero n) ->
  mat_add (mat_mul g (mat_sum m f)) (mat_mul (mat_sum m f) g) = mat_zero n.
Proof.
  induction m as [|m IH]; intros Hf.
  - simpl. rewrite mat_mul_zero_l. rewrite mat_mul_zero_r. apply mat_add_0_l.
  - rewrite mat_sum_S.
    rewrite (mat_distr_l n g (f m) (mat_sum m f)).
    rewrite (mat_distr_r n (f m) (mat_sum m f) g).
    replace (mat_add (mat_add (mat_mul g (f m)) (mat_mul g (mat_sum m f)))
              (mat_add (mat_mul (f m) g) (mat_mul (mat_sum m f) g)))
      with (mat_add (mat_add (mat_mul g (f m)) (mat_mul (f m) g))
                (mat_add (mat_mul g (mat_sum m f)) (mat_mul (mat_sum m f) g))).
    + rewrite Hf. lia.
      rewrite IH.
      * rewrite (mat_add_0_l n (mat_zero n)). reflexivity.
      * intros i Hi. apply Hf. lia.
    + extensionality i. extensionality j.
      unfold mat_add.
      ring.
Qed.

Lemma mat_sum_sq {n} (m : nat) (coeffs : nat -> R) (gens : nat -> Mat n) :
  (forall i, (i < m)%nat -> mat_mul (gens i) (gens i) = mat_opp (mat_one n)) ->
  (forall i j, (i < m)%nat -> (j < m)%nat -> i <> j ->
    mat_add (mat_mul (gens i) (gens j)) (mat_mul (gens j) (gens i)) = mat_zero n) ->
  mat_mul (mat_sum m (fun i => mat_smul (coeffs i) (gens i)))
          (mat_sum m (fun i => mat_smul (coeffs i) (gens i))) =
  mat_smul (- sum_R m (fun i => coeffs i * coeffs i)) (mat_one n).
Proof.
  induction m as [|m IH]; intros Hsq Hcomm.
  - simpl. unfold mat_mul. simpl.
    extensionality i. extensionality j.
    unfold mat_mul_aux, mat_smul, mat_zero. simpl.
    rewrite Rmult_0_l. reflexivity.
  - rewrite mat_sum_S.
    rewrite (sq_expand_general n (coeffs m) (gens m) (mat_sum m (fun i => mat_smul (coeffs i) (gens i)))).
    + rewrite IH.
      replace (mat_add (mat_smul (- (coeffs m * coeffs m)) (mat_one n))
                (mat_smul (- sum_R m (fun i : nat => coeffs i * coeffs i)) (mat_one n)))
        with (mat_smul (- (coeffs m * coeffs m + sum_R m (fun i : nat => coeffs i * coeffs i))) (mat_one n)).
      * rewrite sum_R_S_eq. reflexivity.
      * extensionality i. extensionality j.
        unfold mat_add, mat_smul.
        ring.
    + apply Hsq. lia.
    + apply mat_sum_anticomm.
      intros i Hi.
      apply anticomm_sum_step.
      apply Hcomm; lia.
Qed.
