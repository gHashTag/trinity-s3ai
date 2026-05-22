/-!
# KO-Dimension Signs for Real Spectral Triples

In Connes' noncommutative geometry, a real spectral triple is classified by
three signs ε, ε', ε'' ∈ {+1, −1} that determine the KO-dimension.

This module defines the sign structure and proves the basic algebraic
constraints they satisfy.
-/

namespace TrinityLean

/-- KO-dimension signs (ε, ε', ε'') for a real spectral triple.
    Each sign is either +1 or −1, and they satisfy ε·ε' = ε''. -/
structure KOSigns where
  epsilon   : Int
  epsilon'  : Int
  epsilon'' : Int
  hε        : epsilon = 1 ∨ epsilon = -1
  hε'       : epsilon' = 1 ∨ epsilon' = -1
  hε''      : epsilon'' = 1 ∨ epsilon'' = -1
  hmul      : epsilon * epsilon' = epsilon''

namespace KOSigns

/-- Each sign squares to 1. -/
theorem epsilon_sq_one (s : KOSigns) : s.epsilon * s.epsilon = 1 := by
  cases s.hε with
  | inl h => rw [h]; rfl
  | inr h => rw [h]; rfl

theorem epsilon'_sq_one (s : KOSigns) : s.epsilon' * s.epsilon' = 1 := by
  cases s.hε' with
  | inl h => rw [h]; rfl
  | inr h => rw [h]; rfl

theorem epsilon''_sq_one (s : KOSigns) : s.epsilon'' * s.epsilon'' = 1 := by
  cases s.hε'' with
  | inl h => rw [h]; rfl
  | inr h => rw [h]; rfl

/-- The defining relation ε·ε' = ε''. -/
theorem epsilon_epsilon'_eq_epsilon'' (s : KOSigns) :
    s.epsilon * s.epsilon' = s.epsilon'' := by
  exact s.hmul

/-- From the constraints one derives ε'·ε'' = ε. -/
theorem epsilon'_epsilon''_eq_epsilon (s : KOSigns) :
    s.epsilon' * s.epsilon'' = s.epsilon := by
  have h1 : s.epsilon'' = s.epsilon * s.epsilon' := by rw [s.hmul]
  rw [h1]
  have h2 : s.epsilon' * (s.epsilon * s.epsilon')
          = (s.epsilon' * s.epsilon) * s.epsilon' := by
    rw [← Int.mul_assoc]
  rw [h2]
  have h3 : s.epsilon' * s.epsilon = s.epsilon * s.epsilon' := by
    rw [Int.mul_comm]
  rw [h3]
  have h4 : s.epsilon * s.epsilon' * s.epsilon'
          = s.epsilon * (s.epsilon' * s.epsilon') := by
    rw [Int.mul_assoc]
  rw [h4]
  rw [s.epsilon'_sq_one]
  rw [Int.mul_one]

/-- And also ε''·ε = ε'. -/
theorem epsilon''_epsilon_eq_epsilon' (s : KOSigns) :
    s.epsilon'' * s.epsilon = s.epsilon' := by
  have h1 : s.epsilon'' = s.epsilon * s.epsilon' := by rw [s.hmul]
  rw [h1]
  have h2 : (s.epsilon * s.epsilon') * s.epsilon
          = s.epsilon * (s.epsilon' * s.epsilon) := by
    rw [Int.mul_assoc]
  rw [h2]
  have h3 : s.epsilon' * s.epsilon = s.epsilon * s.epsilon' := by
    rw [Int.mul_comm]
  rw [h3]
  have h4 : s.epsilon * (s.epsilon * s.epsilon')
          = s.epsilon * s.epsilon * s.epsilon' := by
    rw [Int.mul_assoc]
  rw [h4]
  rw [s.epsilon_sq_one]
  rw [Int.one_mul]

/-- The three signs are uniquely determined by any two of them. -/
theorem uniqueness (s t : KOSigns)
    (h1 : s.epsilon = t.epsilon) (h2 : s.epsilon' = t.epsilon') :
    s.epsilon'' = t.epsilon'' := by
  have hs : s.epsilon'' = s.epsilon * s.epsilon' := by rw [s.hmul]
  have ht : t.epsilon'' = t.epsilon * t.epsilon' := by rw [t.hmul]
  rw [hs, ht, h1, h2]

end KOSigns

end TrinityLean
