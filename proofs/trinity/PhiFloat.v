(** PHI-IDENTITY — Flocq IEEE 754 binary64 bridge.
    Source: t27/coq/Kernel/PhiFloat.v (commit from t27 repo).
    Requires [coq-flocq] on COQPATH.
    See docs/hardware/HARDWARE_ATTESTATION.md §1 for status.

    This file proves that for the binary64 literal of φ,
    [fl(phi*phi)] and [fl(phi+1)] are bit-identical.
    The equality is verified by [vm_compute] (bit-exact check).

    A future extension can add [Bmult_correct] / [Bplus_correct] + error
    bounds for GF16 (see docs/hardware/gf16_mathematics.md §6).
*)

From Coq Require Import Reals ZArith.

From Flocq Require Import IEEE754.Binary.
From Flocq Require Import IEEE754.Bits.
From Flocq Require Import IEEE754.BinarySingleNaN.

(** NOTE: Original file requires T27.Kernel.Phi for [phi_tolerance].
    In this standalone copy we inline the required definition.
    For full build, install coq-flocq and restore the original import:
    [Require Import T27.Kernel.Phi.] *)

Definition phi_tolerance : R := 5 * powerRZ 2 (-53) * ((1 + sqrt 5) / 2) * ((1 + sqrt 5) / 2).

Open Scope R_scope.
Open Scope Z_scope.

Import Binary Bits BinarySingleNaN.

Notation b64 := binary64 (only parsing).

Definition B2R64 : binary64 -> R := @B2R 53 1024.

(** Nearest-round φ as [B754_finite] (see validation script). *)
Definition phi_mantissa : positive := 7286977268806824%positive.
Definition phi_exponent : Z := (-52)%Z.

Lemma phi_f64_bounded : bounded 53 1024 phi_mantissa phi_exponent = true.
Proof. vm_compute. reflexivity. Qed.

Definition phi_f64 : binary64 :=
  B754_finite false phi_mantissa phi_exponent phi_f64_bounded.

(** [1.0] in binary64. *)
Definition one_mantissa : positive := 4503599627370496%positive.
Definition one_exponent : Z := (-52)%Z.

Lemma one_f64_bounded : bounded 53 1024 one_mantissa one_exponent = true.
Proof. vm_compute. reflexivity. Qed.

Definition one_f64 : binary64 :=
  B754_finite false one_mantissa one_exponent one_f64_bounded.

Definition phi_sq_f64 : binary64 := b64_mult mode_NE phi_f64 phi_f64.

Definition phi_plus_one_f64 : binary64 := b64_plus mode_NE phi_f64 one_f64.

Lemma phi_sq_f64_eq_phi_plus_one_f64 : phi_sq_f64 = phi_plus_one_f64.
Proof. vm_compute. reflexivity. Qed.

(** Engineering bound (Layer A SSOT): [5 * 2^-53 * phi^2] on [R]. *)
Definition PHI_F64_TOLERANCE : R := phi_tolerance.

Theorem phi_identity_contract :
  Rabs (B2R64 phi_sq_f64 - B2R64 phi_plus_one_f64) < PHI_F64_TOLERANCE.
Proof.
  assert (Hbr : B2R64 phi_sq_f64 = B2R64 phi_plus_one_f64).
  {
    apply f_equal.
    exact phi_sq_f64_eq_phi_plus_one_f64.
  }
  unfold PHI_F64_TOLERANCE.
  replace (B2R64 phi_sq_f64 - B2R64 phi_plus_one_f64) with 0.
  - rewrite Rabs_R0.
    unfold phi_tolerance.
    lra.
  - rewrite Hbr.
    ring.
Qed.

Lemma phi_tolerance_positive : 0 < phi_tolerance.
Proof. unfold phi_tolerance; lra. Qed.

Lemma PHI_F64_TOLERANCE_pos : 0 < PHI_F64_TOLERANCE.
Proof. unfold PHI_F64_TOLERANCE; apply phi_tolerance_positive. Qed.