Require Import Reals.
Require Import Interval.Tactic.
Open Scope R_scope.

Definition phi : R := (1 + sqrt 5) / 2.

Goal Rabs (4 * phi^3 * (exp 1)^2 - 125.20) / 125.20 < 0.01.
Proof.
  unfold phi.
  interval with (i_prec 60).
Qed.
