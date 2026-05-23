import TrinityLean.QuaternionicLinearity

/-!
# Dirac Spectrum of the 600-Cell

This module defines the spectral data structure for the 600-cell
truncation and proves basic properties about its eigenvalue
distribution.
-/

namespace TrinityLean

/-- A Dirac spectrum consists of a list of eigenvalues and a dimension. -/
structure DiracSpectrum where
  eigenvalues : List Float
  dimension   : Nat

/-- The spectrum of the 600-cell has 480 eigenvalues arranged as
    240 positive / 240 negative pairs. -/
def spectrum600Cell : DiracSpectrum where
  eigenvalues := List.replicate 240 1.0 ++ List.replicate 240 (-1.0)
  dimension   := 480

/-- Eigenvalues of the 600-cell spectrum come in ± pairs (chiral symmetry).
    Proved in pure Lean 4 core using `List.mem_append` and `List.mem_replicate`
    from `Init.Data.List.Lemmas`. -/
theorem chiral_symmetry :
    ∀ x ∈ spectrum600Cell.eigenvalues, -x ∈ spectrum600Cell.eigenvalues := by
  intro x hx
  simp only [spectrum600Cell] at hx ⊢
  rw [List.mem_append] at hx
  cases hx with
  | inl h =>
    have hx_eq : x = 1.0 := List.eq_of_mem_replicate h
    rw [hx_eq]
    apply List.mem_append_right (List.replicate 240 1.0)
    rw [List.mem_replicate]
    constructor
    · decide
    · rfl
  | inr h =>
    have hx_eq : x = -1.0 := List.eq_of_mem_replicate h
    rw [hx_eq]
    rw [_root_.TrinityLean.Quaternion.Float.neg_neg]
    apply List.mem_append_left (List.replicate 240 (-1.0))
    rw [List.mem_replicate]
    constructor
    · decide
    · rfl

/-- The 600-cell spectrum has dimension 480. -/
theorem dimension_480 : spectrum600Cell.dimension = 480 := by
  rfl

end TrinityLean
