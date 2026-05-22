/-
  Trinity S3AI — TrinityLean/CorePhi.lean
  Stage 0 port of proofs/trinity/CorePhi.v

  STATUS: Scaffold only — NOT yet compiled. Requires elan + lake on host.
  See derivations/lean_port/README.md for build instructions.
-/

import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

open Real

/-!
## Section 1: Golden Ratio Definition

φ = (1 + √5) / 2
-/

/-- The golden ratio. -/
noncomputable def phi : ℝ := (1 + Real.sqrt 5) / 2

/-- The conjugate root ψ = (1 − √5) / 2. -/
noncomputable def psi : ℝ := (1 - Real.sqrt 5) / 2

/-!
## Section 2: Elementary Positivity Lemmas
-/

/-- √5 > 0 -/
lemma sqrt5_pos : 0 < Real.sqrt 5 := by
  apply Real.sqrt_pos_of_pos; norm_num

/-- √5 > 2 — needed for φ > 1 -/
lemma sqrt5_gt_two : 2 < Real.sqrt 5 := by
  rw [show (2 : ℝ) = Real.sqrt 4 by
    rw [Real.sqrt_eq_iff_sq_eq (by norm_num) (by norm_num)]
    norm_num]
  apply Real.sqrt_lt_sqrt <;> norm_num

/-- √5 < 3 -/
lemma sqrt5_lt_three : Real.sqrt 5 < 3 := by
  rw [show (3 : ℝ) = Real.sqrt 9 by
    rw [Real.sqrt_eq_iff_sq_eq (by norm_num) (by norm_num)]
    norm_num]
  apply Real.sqrt_lt_sqrt <;> norm_num

/-- φ > 0 -/
lemma phi_pos : 0 < phi := by
  unfold phi
  have h := sqrt5_pos
  linarith

/-- φ > 1 -/
lemma phi_gt_one : 1 < phi := by
  unfold phi
  have h := sqrt5_gt_two
  linarith

/-- φ < 2 -/
lemma phi_lt_two : phi < 2 := by
  unfold phi
  have h := sqrt5_lt_three
  linarith

/-!
## Section 3: The Fundamental Identity — φ² = φ + 1
-/

/-- (√5)² = 5 -/
lemma sqrt5_sq : Real.sqrt 5 * Real.sqrt 5 = 5 := by
  rw [← Real.sq_sqrt (by norm_num : (5 : ℝ) ≥ 0)]
  ring

/-- The defining quadratic identity of the golden ratio: φ * φ = φ + 1 -/
theorem phi_sq : phi * phi = phi + 1 := by
  unfold phi
  have h5 := sqrt5_sq
  field_simp
  nlinarith [h5]

/-!
## Section 4: Derived Identities
-/

/-- φ³ = 2φ + 1 -/
theorem phi_cubed : phi * phi * phi = 2 * phi + 1 := by
  have h := phi_sq
  calc phi * phi * phi
      = (phi * phi) * phi := by ring
    _ = (phi + 1) * phi   := by rw [h]
    _ = phi * phi + phi   := by ring
    _ = (phi + 1) + phi   := by rw [h]
    _ = 2 * phi + 1       := by ring

/-- φ⁻¹ = φ − 1 -/
theorem phi_inv : phi⁻¹ = phi - 1 := by
  have hne : phi ≠ 0 := ne_of_gt phi_pos
  field_simp
  linarith [phi_sq]

/-- φ · ψ = −1 -/
theorem phi_psi_product : phi * psi = -1 := by
  unfold phi psi
  have h5 := sqrt5_sq
  field_simp
  nlinarith [h5]

/-!
## Section 5: Numerical Bounds
-/

/-- A coarse two-sided bound: 1.618 < φ < 1.619 -/
theorem phi_bounds : 1.618 < phi ∧ phi < 1.619 := by
  constructor
  · unfold phi
    have h : 2.236 < Real.sqrt 5 := by
      have : (2.236 : ℝ)^2 < 5 := by norm_num
      calc 2.236 = Real.sqrt (2.236^2) := by
              rw [Real.sqrt_sq (by norm_num : (2.236 : ℝ) ≥ 0)]
        _ < Real.sqrt 5 := Real.sqrt_lt_sqrt (by norm_num) this
    linarith
  · unfold phi
    have h : Real.sqrt 5 < 2.238 := by
      have : (5 : ℝ) < 2.238^2 := by norm_num
      calc Real.sqrt 5 < Real.sqrt (2.238^2) :=
              Real.sqrt_lt_sqrt (by norm_num) this
        _ = 2.238 := Real.sqrt_sq (by norm_num : (2.238 : ℝ) ≥ 0)
    linarith

/-!
## Section 6: powZ stub (integer powers)

In Lean 4 / Mathlib we use zpow from the Mathlib library instead of the
hand-rolled powZ from CorePhi.v. The equivalences below note the correspondence.
-/

/-- φ^(2 : ℤ) = φ + 1  (using Mathlib zpow) -/
theorem phi_zpow_two : phi ^ (2 : ℤ) = phi + 1 := by
  simp [zpow_two]
  exact phi_sq

/-- φ^(3 : ℤ) = 2φ + 1 -/
theorem phi_zpow_three : phi ^ (3 : ℤ) = 2 * phi + 1 := by
  have h : phi ^ (3 : ℤ) = phi * phi * phi := by
    simp [zpow_ofNat]; ring
  rw [h]
  exact phi_cubed

/-
  End of CorePhi.lean — Stage 0 scaffold
  Total: 10 lemmas/theorems ported from CorePhi.v
-/

/-!
## Section 7: Helper lemmas for Stage 1 (KODimension.lean, QuaternionicLinearity.lean)

These lemmas were added in Wave 10.3 to support the Stage 1 port.
-/

/-- φ² = φ + 1  in the ℤ-power (^ : ℝ → ℕ → ℝ) form, for nlinarith. -/
lemma phi_sq_nat : phi ^ 2 = phi + 1 := by
  have h := phi_sq
  nlinarith [sq_nonneg phi]

/-- (φ − 1)² = 2 − φ  (derived from φ² = φ + 1). -/
lemma phi_minus_one_sq : (phi - 1) ^ 2 = 2 - phi := by
  have h := phi_sq
  nlinarith [sq_nonneg phi]

/-- φ · (φ − 1) = 1  (product of consecutive Fibonacci-type terms). -/
lemma phi_times_phi_minus_one : phi * (phi - 1) = 1 := by
  have h := phi_sq
  nlinarith

/-- (1/2)² + (φ/2)² + ((φ−1)/2)² = 1  (icosian Pythagorean identity, scaled). -/
lemma icosian_norm_sq :
    (1/2 : ℝ)^2 + (phi/2)^2 + ((phi-1)/2)^2 = 1 := by
  have h := phi_sq
  nlinarith [sq_nonneg phi, sq_nonneg (phi - 1)]

/-
  End of CorePhi.lean — Stage 0 + Stage 1 helpers
  Total: 10 (Stage 0) + 4 (Stage 1 helpers) = 14 lemmas/theorems
-/
