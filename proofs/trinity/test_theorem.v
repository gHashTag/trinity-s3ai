Require Import Reals.
Open Scope R_scope.
Require Import Interval.Tactic.
From Trinity Require Import CorePhi.

Definition m_s_PDG : R := 93.4.
Definition m_d_PDG : R := 4.67.
Definition SG_bound : R := /10000.
Definition Q07_SG : R := 24 * phi * phi / PI.

Theorem Q07_is_m_s_over_m_d :
  Rabs (Q07_SG - (m_s_PDG / m_d_PDG)) / (m_s_PDG / m_d_PDG) < SG_bound.
Proof.
  unfold Q07_SG, m_s_PDG, m_d_PDG, SG_bound.
  interval with (i_prec 60).
Qed.
