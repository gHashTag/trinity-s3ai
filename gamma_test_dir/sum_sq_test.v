From Coq Require Import Reals Lia Lra FunctionalExtensionality.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Lemma sum_R_S_eq : forall n f, sum_R (S n) f = f n + sum_R n f.
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

Lemma mat_smul_add_l_sym (n : nat) (r : R) (A B : Mat n) :
  mat_add (mat_smul r A) (mat_smul r B) = mat_smul r (mat_add A B).
Proof.
  symmetry. apply mat_smul_add_l.
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
  repeat rewrite (mat_add_assoc n).
  rewrite <- (mat_add_assoc n (mat_smul a (mat_mul g A)) (mat_smul a (mat_mul A g)) (mat_mul A A)).
  rewrite (mat_smul_add_l_sym n a (mat_mul g A) (mat_mul A g)).
  rewrite Hcomm.
  rewrite (mat_smul_zero_r n a).
  rewrite (mat_add_0_l n (mat_mul A A)).
  reflexivity.
Qed.

Lemma anticomm_sum_step (n : nat) (a : R) (g A : Mat n) :
  mat_add (mat_mul g A) (mat_mul A g) = mat_zero n ->
  mat_add (mat_mul g (mat_smul a A)) (mat_mul (mat_smul a A) g) = mat_zero n.
Proof.
  intros H.
  rewrite (mat_smul_mul_r n a A g).
  rewrite (mat_smul_mul_l n a g A).
  rewrite (mat_smul_add_l_sym n a (mat_mul g A) (mat_mul A g)).
  rewrite H.
  apply mat_smul_zero_r.
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
        rewrite (mat_smul_add_l_sym n (- (coeffs m * coeffs m)) (mat_one n) (mat_smul (- sum_R m (fun i : nat => coeffs i * coeffs i)) (mat_one n))).
        rewrite <- (mat_smul_add_distr n (- (coeffs m * coeffs m)) (- sum_R m (fun i : nat => coeffs i * coeffs i)) (mat_one n)).
        rewrite Ropp_mult_distr_l.
        rewrite <- Ropp_plus_distr.
        reflexivity.
      * intros i Hi. apply Hsq. lia.
      * intros i j Hi Hj Hneq. apply Hcomm; lia.
    + apply Hsq. lia.
    + induction m as [|m' IHm'].
      * simpl. rewrite mat_mul_zero_l. rewrite mat_mul_zero_r. apply mat_add_0_l.
      * simpl sum_R at 1 3.
        rewrite (mat_distr_l n (gens (S m')) (mat_smul (coeffs m') (gens m')) (sum_R m' _)).
        rewrite (mat_distr_r n (mat_smul (coeffs m') (gens m')) (sum_R m' _) (gens (S m'))).
        rewrite (anticomm_sum_step n (coeffs m') (gens (S m')) (gens m')).
        -- rewrite IHm'.
           ++ repeat rewrite (mat_add_assoc n).
              rewrite (mat_add_comm n (mat_mul (gens (S m')) (sum_R m' _)) (mat_mul (sum_R m' _) (gens (S m')))).
              repeat rewrite <- (mat_add_assoc n).
              reflexivity.
           ++ intros i Hi. apply Hcomm; lia.
           ++ intros i j Hi Hj Hneq. apply Hcomm; lia.
        -- apply Hcomm; lia.
Qed.
