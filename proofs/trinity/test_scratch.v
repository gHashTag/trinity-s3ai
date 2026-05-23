Require Import Reals.
From Coq Require Import Lra.
Require Import Field.

Open Scope R_scope.

Definition phi : R := (1 + sqrt 5) / 2.

Section TestScratch.
#[local] Parameter e : R.
#[local] Axiom e_gt_0 : 0 < e.

Definition v_SM : R := 246.
Definition m_H_Trinity : R := 4 * phi ^ 3 * e ^ 2.
Definition lambda_corrected : R := m_H_Trinity ^ 2 / (2 * v_SM ^ 2).
Definition mu_sq_corrected : R := lambda_corrected * v_SM ^ 2.
Definition v_corrected : R := sqrt (mu_sq_corrected / lambda_corrected).
Definition m_H_corrected : R := sqrt (2 * lambda_corrected) * v_SM.

Lemma phi_pos : 0 < phi.
Proof. unfold phi. assert (0 < sqrt 5) by (apply sqrt_lt_R0; lra). lra. Qed.

Lemma phi3_pos : 0 < phi ^ 3.
Proof. apply pow_lt. apply phi_pos. Qed.

Lemma e2_pos : 0 < e ^ 2.
Proof. apply pow_lt. exact e_gt_0. Qed.

Lemma m_H_Trinity_pos : 0 < m_H_Trinity.
Proof.
  unfold m_H_Trinity.
  assert (0 < e ^ 2) by (apply pow_lt; exact e_gt_0).
  assert (0 < phi ^ 3) by (apply pow_lt; apply phi_pos).
  nra.
Qed.

Lemma m_H_Trinity_neq : m_H_Trinity <> 0.
Proof. assert (0 < m_H_Trinity) by apply m_H_Trinity_pos. lra. Qed.

Lemma lambda_corrected_pos : 0 < lambda_corrected.
Proof.
  unfold lambda_corrected. apply Rmult_lt_0_compat.
  - apply pow_lt. apply m_H_Trinity_pos.
  - apply Rinv_0_lt_compat. unfold v_SM. nra.
Qed.

Lemma v_SM_pos : 0 < v_SM.
Proof. unfold v_SM; lra. Qed.

Lemma v_SM_neq : v_SM <> 0.
Proof. unfold v_SM; lra. Qed.

Lemma v_SM_pos' : 0 < v_SM ^ 2.
Proof. unfold v_SM. nra. Qed.

(* Test VEV_corrected_matches_SM *)
Theorem VEV_corrected_matches_SM :
  v_corrected = v_SM.
Proof.
  unfold v_corrected, mu_sq_corrected, lambda_corrected.
  assert (H1: m_H_Trinity ^ 2 / (2 * v_SM ^ 2) * v_SM ^ 2 / (m_H_Trinity ^ 2 / (2 * v_SM ^ 2)) = v_SM ^ 2).
  { field. repeat split; try (unfold v_SM; lra); try (apply Rgt_not_eq; apply m_H_Trinity_pos). }
  rewrite H1.
  rewrite sqrt_pow2.
  reflexivity.
  unfold v_SM; lra.
Qed.

(* Test m_H_corrected_matches_Trinity *)
Theorem m_H_corrected_matches_Trinity :
  m_H_corrected = m_H_Trinity.
Proof.
  unfold m_H_corrected, lambda_corrected.
  assert (H2: 2 * (m_H_Trinity ^ 2 / (2 * v_SM ^ 2)) = m_H_Trinity ^ 2 / v_SM ^ 2).
  { field. repeat split; try (unfold v_SM; lra); try (apply Rgt_not_eq; apply m_H_Trinity_pos). }
  rewrite H2.
  assert (H3: sqrt (m_H_Trinity ^ 2 / v_SM ^ 2) = m_H_Trinity / v_SM).
  { rewrite sqrt_div_alt.
    2: { unfold v_SM; lra. }
    rewrite sqrt_pow2.
    2: { apply Rlt_le. apply m_H_Trinity_pos. }
    rewrite sqrt_pow2.
    2: { unfold v_SM; lra. }
    reflexivity. }
  rewrite H3.
  field. repeat split; try (unfold v_SM; lra); try (apply Rgt_not_eq; apply m_H_Trinity_pos).
Qed.

(* Test Higgs_mass_from_curvature *)
Theorem Higgs_mass_from_curvature :
  sqrt (2 * mu_sq_corrected) = m_H_Trinity.
Proof.
  unfold mu_sq_corrected, lambda_corrected.
  assert (H1: 2 * (m_H_Trinity ^ 2 / (2 * v_SM ^ 2) * v_SM ^ 2) = m_H_Trinity ^ 2).
  { field. repeat split; try (unfold v_SM; lra); try (apply Rgt_not_eq; apply m_H_Trinity_pos). }
  rewrite H1.
  rewrite sqrt_pow2.
  reflexivity.
  apply Rlt_le, m_H_Trinity_pos.
Qed.

End TestScratch.
Close Scope R_scope.
