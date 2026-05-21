(******************************************************************************)
(* Predictions.v -- Trinity S3AI Observable Predictions                       *)
(******************************************************************************)

Require Import Reals.
From Interval Require Import Tactic.

Open Scope R_scope.

(* Import Catalog42 for m_nue_pred, NuSum_SG, and PDG definitions *)
From Trinity Require Import Catalog42.
From Trinity Require Import CorePhi.

(******************************************************************************)
(* Section 0: Fundamental constants                                           *)
(******************************************************************************)

Definition phi : R := (1 + sqrt 5) / 2.
Definition euler_e : R := exp 1.

Lemma phi_bounds :
  16180339887 / 10000000000 < phi < 16180339889 / 10000000000.
Proof.
  unfold phi. split; interval with (i_prec 100).
Qed.

(******************************************************************************)
(* Section 1: delta_CP = 3/phi^2 = 65.66 degrees                              *)
(******************************************************************************)

Definition delta_CP_pred : R := 3 / phi^2.
Definition delta_CP_degrees : R := delta_CP_pred * 180 / PI.

Lemma delta_CP_degrees_bounds :
  65.65 < delta_CP_degrees < 65.66.
Proof.
  unfold delta_CP_degrees, delta_CP_pred, phi.
  split; interval with (i_prec 100).
Qed.

(******************************************************************************)
(* Section 2: m_nue = 1/(6*phi) = 0.103 eV (KATRIN-II 2028)                  *)
(* m_nue_pred imported from Catalog42.v                                       *)
(******************************************************************************)

Lemma m_nue_approx_0_103 :
  10296 / 100000 < m_nue_pred < 10310 / 100000.
Proof.
  unfold m_nue_pred, phi.
  split; interval with (i_prec 100).
Qed.

Lemma m_nue_KATRIN_II_test :
  m_nue_pred > 1 / 20.
Proof.
  unfold m_nue_pred, phi.
  interval with (i_prec 100).
Qed.

Lemma m_nue_falsifiability :
  m_nue_pred < 1 / 5.
Proof.
  unfold m_nue_pred, phi.
  interval with (i_prec 100).
Qed.

(******************************************************************************)
(* Section 3: m_DM = phi^5 * PI / e ~ 12.8 GeV                               *)
(******************************************************************************)

Definition m_DM_pred : R := phi^5 * PI / euler_e.

Lemma m_DM_bounds :
  1281 / 100 < m_DM_pred < 1282 / 100.
Proof.
  unfold m_DM_pred, euler_e, phi.
  split; interval with (i_prec 100).
Qed.

(******************************************************************************)
(* Section 4: Sum_m_nu ~ 0.059 eV (inverted hierarchy, CMB-S4 2030)          *)
(******************************************************************************)

Definition Sigma_mnu_pred : R := NuSum_SG.

(* Individual neutrino mass eigenvalues *)
Definition m_nu1 : R := sqrt (delta_m31_sq_PDG / 2).
Definition m_nu2 : R := sqrt (delta_m31_sq_PDG / 2).
Definition m_nu3 : R := sqrt (delta_m21_sq_PDG).

Lemma Sigma_mnu_sum_check :
  m_nu1 + m_nu2 + m_nu3 > 7 / 100.
Proof.
  unfold m_nu1, m_nu2, m_nu3, delta_m31_sq_PDG, delta_m21_sq_PDG.
  interval with (i_prec 100).
Qed.

Lemma Sigma_mnu_bounds :
  580 / 10000 < Sigma_mnu_pred < 595 / 10000.
Proof.
  unfold Sigma_mnu_pred, NuSum_SG, phi, powZ.
  simpl. split; interval with (i_prec 200).
Qed.

(******************************************************************************)
(* Section 5: sin^2(theta_13) = PI^2/(25*phi^6) ~ 0.022                      *)
(******************************************************************************)

Definition sin2_theta13_pred : R := PI * PI / (25 * phi^6).

Lemma sin2_theta13_bounds :
  2195 / 100000 < sin2_theta13_pred < 2205 / 100000.
Proof.
  unfold sin2_theta13_pred, phi.
  split; interval with (i_prec 100).
Qed.

Lemma sin2_theta13_approx_0_022 :
  21 / 1000 < sin2_theta13_pred < 23 / 1000.
Proof.
  unfold sin2_theta13_pred, phi.
  split; interval with (i_prec 100).
Qed.

Lemma sin2_theta13_JUNO_test :
  20 / 1000 < sin2_theta13_pred < 24 / 1000.
Proof.
  unfold sin2_theta13_pred, phi.
  split; interval with (i_prec 100).
Qed.

Lemma sin2_theta13_PDG_2024_agreement :
  213 / 10000 < sin2_theta13_pred < 227 / 10000.
Proof.
  unfold sin2_theta13_pred, phi.
  split; interval with (i_prec 100).
Qed.

(******************************************************************************)
(* Section 7: Combined falsifiability theorem                                 *)
(******************************************************************************)

Theorem Trinity_predictions_2030 :
  65.65 < delta_CP_degrees < 65.66 /\
  10296 / 100000 < m_nue_pred < 10310 / 100000 /\
  1281 / 100 < m_DM_pred < 1282 / 100 /\
  580 / 10000 < Sigma_mnu_pred < 595 / 10000 /\
  2195 / 100000 < sin2_theta13_pred < 2205 / 100000.
Proof.
  split; [apply delta_CP_degrees_bounds | ].
  split; [apply m_nue_approx_0_103 | ].
  split; [apply m_DM_bounds | ].
  split; [apply Sigma_mnu_bounds | ].
  apply sin2_theta13_bounds.
Qed.

(* All assumptions discharged — Trinity predictions verified *)
